# backend/database.py

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# backend 폴더의 절대 경로
BASE_DIR = Path(__file__).resolve().parent

# 프로젝트 루트의 .env 로드
ENV_PATH = BASE_DIR.parent / ".env"
load_dotenv(ENV_PATH)

# 환경변수가 없으면 backend/community.db 사용
DEFAULT_DB_PATH = BASE_DIR / "community.db"
DEFAULT_DATABASE_URL = f"sqlite:///{DEFAULT_DB_PATH.as_posix()}"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    DEFAULT_DATABASE_URL,
)

# SQLite에서만 필요한 옵션
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# DB Engine 생성
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

# 요청별 DB 세션 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# SQLAlchemy 모델의 부모 클래스
Base = declarative_base()


# FastAPI Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()