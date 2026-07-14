# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# .env에서 DB 경로를 읽어오고 없으면 로컬 sqlite 파일 사용
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./community.db")

# 1. Engine 생성: DB와의 물리적 연결 통로
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # SQLite 필수 옵션
)

# 2. Session 관리자: 실시간 DB 작업(Tranaction)을 처리하는 단위
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base 클래스: 이 클래스를 상속받아 데이터베이스 테이블(Model)을 정의함
Base = declarative_base()

# 4. Dependency Injection (의존성 주입)용 함수
# API 요청이 들어오면 세션을 열고, 처리가 끝나면 자동으로 닫아줌 (결합도 분리)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()