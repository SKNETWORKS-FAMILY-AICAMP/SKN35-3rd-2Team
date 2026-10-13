"""Restore tab-scoped login using opaque, expiring server-side sessions."""
import secrets
import threading
import time

import streamlit as st

from src import db

SESSION_SECONDS = 24 * 60 * 60


class SessionStore:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.RLock()

    def issue(self, user_id, password_hash):
        token = secrets.token_urlsafe(32)
        with self.lock:
            now = time.time()
            self.sessions = {k: v for k, v in self.sessions.items() if v[2] > now}
            self.sessions[token] = (user_id, password_hash, now + SESSION_SECONDS)
        return token

    def resolve(self, token):
        if not isinstance(token, str):
            return None
        with self.lock:
            entry = self.sessions.get(token)
            if entry and entry[2] > time.time():
                return entry
            self.sessions.pop(token, None)
        return None

    def revoke(self, token):
        if isinstance(token, str):
            with self.lock:
                self.sessions.pop(token, None)


@st.cache_resource
def session_store():
    return SessionStore()


_storage = st.components.v2.component(
    "account_session_storage",
    html="<span id='storage-sync' hidden></span>",
    js="""
export default function ({data, parentElement, setStateValue}) {
  const marker = JSON.stringify(data);
  const sync = parentElement.querySelector('#storage-sync');
  if (!sync || sync.dataset.synced === marker) return;
  sync.dataset.synced = marker;
  try {
    const key = 'skn.account.session';
    if (data.write) {
      if (data.token) sessionStorage.setItem(key, data.token);
      else sessionStorage.removeItem(key);
    }
    setStateValue('value', {token: sessionStorage.getItem(key), revision: data.revision});
  } catch (_) {
    setStateValue('value', {token: null, revision: data.revision, unavailable: true});
  }
}
""",
)


def remember_login(identity):
    with db.db_session() as session:
        user = session.get(db.User, identity['id'])
        if user is None or not user.is_active:
            raise ValueError('Account unavailable')
        token = session_store().issue(user.id, user.password_hash)
    session_store().revoke(st.session_state.get('browser_token'))
    st.session_state.browser_token = token
    st.session_state.browser_write = True
    st.session_state.browser_revision = secrets.token_hex(8)


def forget_login():
    session_store().revoke(st.session_state.pop('browser_token', None))
    st.session_state.browser_write = True
    st.session_state.browser_revision = secrets.token_hex(8)


def restore_login():
    """Wait for storage hydration/acknowledgement before rendering account UI."""
    revision = st.session_state.setdefault('browser_revision', secrets.token_hex(8))
    result = _storage(
        key='browser_storage',
        data={'write': st.session_state.get('browser_write', False),
              'token': st.session_state.get('browser_token'), 'revision': revision},
        on_value_change=lambda: None,
    )
    value = result.value
    if not value or value.get('revision') != revision:
        st.stop()
    if value.get('unavailable'):
        st.caption('브라우저 저장소를 사용할 수 없어 새로고침 시 다시 로그인해야 합니다.')
        return
    token = value.get('token')
    entry = session_store().resolve(token)
    if entry:
        try:
            with db.db_session() as session:
                user = session.get(db.User, entry[0])
                valid = user is not None and user.is_active and user.password_hash == entry[1]
                identity = {'id': user.id, 'username': user.username} if valid else None
        except Exception:
            st.warning('로그인 상태를 확인하지 못했습니다. 잠시 후 새로고침해 주세요.')
            st.stop()
        if identity:
            st.session_state.browser_token = token
            st.session_state.user_id = identity['id']
            st.session_state.username = identity['username']
            return
        session_store().revoke(token)
    if token:
        forget_login()
        st.session_state.pop('user_id', None)
        st.session_state.pop('username', None)
        st.rerun()
