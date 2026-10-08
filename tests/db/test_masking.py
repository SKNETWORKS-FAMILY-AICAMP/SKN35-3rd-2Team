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


def test_masking_is_idempotent():
    once = mask_secrets(f"key={NV} password=hunter2abc")
    assert mask_secrets(once) == once
