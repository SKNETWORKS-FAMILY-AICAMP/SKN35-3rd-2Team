"""pytest 설정 (비어 있는 것이 정상).

이 파일이 프로젝트 루트에 있으면 pytest가 루트 폴더를 import 경로에 넣어 준다.
덕분에 PYTHONPATH를 따로 지정하지 않아도 tests/ 안에서 `from src... import ...`가 된다.
    uv run pytest tests -q
"""
