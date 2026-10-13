from src.app.browser_auth import SessionStore


def test_refresh_token_resolves_and_logout_revokes():
    store = SessionStore()
    token = store.issue(17, 'password-hash')
    assert store.resolve(token)[:2] == (17, 'password-hash')
    assert store.resolve('forged-token') is None
    store.revoke(token)
    assert store.resolve(token) is None


def test_expiry_and_cleanup(monkeypatch):
    monkeypatch.setattr('src.app.browser_auth.time.time', lambda: 100)
    store = SessionStore()
    token = store.issue(17, 'hash')
    monkeypatch.setattr('src.app.browser_auth.time.time', lambda: 100000)
    assert store.resolve(token) is None
    assert token not in store.sessions
    assert store.resolve(None) is None
    assert store.resolve({'id': 17}) is None


def test_restore_into_fresh_session_and_reject_disabled_account(monkeypatch):
    from contextlib import nullcontext
    from types import SimpleNamespace
    from src.app import browser_auth as auth

    class State(dict):
        __getattr__ = dict.__getitem__
        __setattr__ = dict.__setitem__

    class Rerun(Exception):
        pass

    store = SessionStore()
    token = store.issue(17, 'hash')
    state = State(browser_revision='refresh')
    user = SimpleNamespace(id=17, username='member', password_hash='hash', is_active=True)
    monkeypatch.setattr(auth.st, 'session_state', state)
    monkeypatch.setattr(auth, 'session_store', lambda: store)
    monkeypatch.setattr(auth, '_storage', lambda **kw: SimpleNamespace(value={'token': token, 'revision': 'refresh'}))
    monkeypatch.setattr(auth.db, 'db_session', lambda: nullcontext(SimpleNamespace(get=lambda *args: user)))
    monkeypatch.setattr(auth.st, 'rerun', lambda: (_ for _ in ()).throw(Rerun()))
    auth.restore_login()
    assert state.user_id == 17
    assert state.username == 'member'
    user.is_active = False
    import pytest
    with pytest.raises(Rerun):
        auth.restore_login()
    assert 'user_id' not in state
    assert store.resolve(token) is None
    assert state.browser_write is True


def test_logout_revokes_browser_token(monkeypatch):
    from src.app import browser_auth as auth
    class State(dict):
        __setattr__ = dict.__setitem__
    store = SessionStore()
    token = store.issue(17, 'hash')
    state = State(browser_token=token)
    monkeypatch.setattr(auth.st, 'session_state', state)
    monkeypatch.setattr(auth, 'session_store', lambda: store)
    auth.forget_login()
    assert store.resolve(token) is None
    assert 'browser_token' not in state
    assert state['browser_write'] is True
