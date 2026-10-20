"""pytest 설정.

이 파일이 프로젝트 루트에 있으면 pytest가 루트 폴더를 import 경로에 넣어 준다.
덕분에 PYTHONPATH를 따로 지정하지 않아도 tests/ 안에서 `from src... import ...`가 된다.
    uv run pytest tests -q

시험이 이미지 파일을 프로젝트의 uploads/ 에 남기지 않도록, 시험마다 임시 폴더를 저장 폴더로 쓴다 (src/db/storage.py).
"""

import os

import pytest

# 시험 중에는 앱을 켤 때 하는 미리 불러오기(웜업)를 하지 않는다. (AppTest가 main.py를 실행해도 백그라운드에서 큰 모델을 불러오지 않게)
os.environ.setdefault("CODECLUE_NO_WARMUP", "1")


@pytest.fixture(autouse=True)
def _image_storage_in_tmp(tmp_path_factory, monkeypatch):
    monkeypatch.setenv("IMAGE_STORAGE_DIR", str(tmp_path_factory.mktemp("uploads")))
