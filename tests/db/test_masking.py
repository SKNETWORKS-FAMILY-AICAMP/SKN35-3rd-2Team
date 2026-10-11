"""비밀 마스킹 확인. 키처럼 보이는 가짜 값은 실행할 때 조립한다
(저장소에 키 모양 문자열이 그대로 있으면 GitHub 비밀 검사에 걸릴 수 있어서)."""

import pytest

from src.db.masking import mask_secrets

NV = "nvapi" + "-" + "A1b2C3d4" * 4
GH = "gh" + "p_" + "x9Y8" * 10
SK = "s" + "k-" + "Q" * 30
AWS = "AK" + "IA" + "ABCDEFGH12345678"


@pytest.mark.parametrize("secret", [NV, GH, SK, AWS])
def test_known_key_formats_are_masked(secret):
    out = mask_secrets(f"에러 로그: key={secret} 로 호출했는데 실패")
    assert secret not in out and "[MASKED" in out
    assert "에러 로그" in out and "호출했는데 실패" in out  # 주변 문장은 그대로


def test_assignment_style_secrets():
    assert "hunter2abc" not in mask_secrets("password=hunter2abc")
    assert "abcd1234efgh" not in mask_secrets('{"api_key": "abcd1234efgh"}')
    assert "S3cretValue" not in mask_secrets("DB_PASSWORD = S3cretValue")
    assert mask_secrets("DB_PASSWORD=S3cretValue").startswith("DB_PASSWORD=")  # 이름은 남는다


def test_url_password_masked_but_user_and_host_kept():
    out = mask_secrets("mysql+pymysql://app_user:p4ssw0rd!@host.example.com:4000/db")
    assert "p4ssw0rd" not in out
    assert "app_user" in out and "host.example.com:4000/db" in out


def test_bearer_and_private_key():
    tok = "abc.def." + "Z" * 30
    assert tok not in mask_secrets(f"Authorization: Bearer {tok}")
    # 비밀키 블록 모양도 저장소에 그대로 두지 않고 실행할 때 조립한다 (키 검사 도구에 걸리지 않게)
    begin, end = "-----BEGIN RSA " + "PRIVATE KEY-----", "-----END RSA " + "PRIVATE KEY-----"
    pem = f"{begin}\nMIIEow\nxyz\n{end}"
    out = mask_secrets("키: " + pem + " 끝")
    assert "MIIEow" not in out and "끝" in out


@pytest.mark.parametrize(
    "text",
    [
        "ModuleNotFoundError: No module named 'langgraph.prebuilt'",
        "LangGraph에서 State를 업데이트했는데 다음 Node에 전달되지 않습니다.",
        "llm = ChatNVIDIA(max_tokens=1500, temperature=0)",   # token이 들어가지만 비밀이 아님
        "HISTORY_MAX_TOKENS=1500",
        "tokenizer=cl100k_base",
        "token_count: 120",
        'password = os.getenv("DB_PASSWORD")',                # 코드 표현
        "api_key=${NVIDIA_API_KEY}",                          # 환경변수 자리표시자
        "api_key=None",
        "api_key=<your-key-here>",
        "",
    ],
)
def test_normal_text_and_code_are_left_alone(text):
    assert mask_secrets(text) == text


@pytest.mark.parametrize("prefix_len", [10, 59, 61, 200])
def test_very_long_key_name_prefix_is_still_masked(prefix_len):
    out = mask_secrets("A" * prefix_len + "_PASSWORD=hunter2abc")
    assert "hunter2abc" not in out and out.startswith("A" * prefix_len + "_PASSWORD=")


@pytest.mark.parametrize("suffix_len", [10, 99])  # 단어(PASSWORD) 뒤 이름 글자는 "_"를 포함해 100자까지 본다
def test_long_key_name_suffix_is_masked_up_to_limit(suffix_len):
    out = mask_secrets("PASSWORD_" + "B" * suffix_len + "=hunter2abc")
    assert "hunter2abc" not in out


LONG = 200_000  # MESSAGE_MAX_CHARS 상한과 같은 길이
PEM_BEGIN = "-----BEGIN RSA " + "PRIVATE KEY-----"


@pytest.mark.parametrize(
    "text",
    [
        "x" * LONG,                          # 공백 없이 이어진 글자 (base64, 압축된 코드 등)
        "0123456789" * (LONG // 10),
        "a-b_" * (LONG // 4),
        "token " * (LONG // 6),              # 키워드가 계속 반복되는 글
        "password" * (LONG // 8),
        "api_key=" * (LONG // 8),
        "DB_PASSWORD" + "_" * LONG,
        "://" + "a:" * (LONG // 2),
        PEM_BEGIN * (LONG // len(PEM_BEGIN)),  # 시작 표시만 있고 끝 표시가 없는 경우
    ],
    ids=["letters", "digits", "dashes", "token-words", "password-run", "api_key-run", "long-name", "url-colons", "pem-begin"],
)
def test_masking_stays_fast_on_long_adversarial_text(text):
    """예전 정규식은 이런 글에서 길이의 제곱만큼 느려졌다 (16,000자에 7초, 20만 자는 사실상 멈춤).

    정규식 계산은 같은 프로세스 안에서는 중간에 끊을 수 없어서, 별도 프로세스에서 시간 제한을 두고 돌린다.
    이렇게 하면 수정이 다시 사라져도 전체 시험이 멈추지 않고 이 시험만 실패한다 (실제로 한 번 병합 중에 수정이 되돌려져 시험이 4분 넘게 멈췄다).
    """
    import subprocess
    import sys
    from pathlib import Path

    module = Path(__file__).resolve().parents[2] / "src" / "db" / "masking.py"
    code = (
        "import importlib.util, sys; "
        f"spec = importlib.util.spec_from_file_location('masking', {str(module)!r}); "
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "  # src.db 패키지 전체(sqlalchemy 등)를 불러오지 않으려고 파일을 직접 읽는다
        "m.mask_secrets(sys.stdin.read())"
    )
    try:
        done = subprocess.run([sys.executable, "-c", code], input=text, text=True, capture_output=True, timeout=15)
    except subprocess.TimeoutExpired:
        pytest.fail("mask_secrets가 15초 안에 끝나지 않았습니다 (정규식이 글 길이의 제곱으로 느려졌을 가능성이 큽니다).")
    assert done.returncode == 0, done.stderr[-300:]


def test_secret_deep_inside_long_text_is_still_masked():
    filler = "정상적인 문장입니다. " * 20_000
    out = mask_secrets(filler + "password=hunter2abc " + filler)
    assert "hunter2abc" not in out
    assert out.count("정상적인 문장입니다.") == 40_000  # 주변 문장은 그대로


def test_masking_is_idempotent():
    once = mask_secrets(f"key={NV} password=hunter2abc")
    assert mask_secrets(once) == once
