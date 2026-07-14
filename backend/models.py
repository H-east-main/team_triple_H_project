# backend/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True, nullable=False)  # 선정한 1개 권역 카테고리
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    password = Column(String, nullable=False)               # 교육 목적의 평문 비밀번호
    created_at = Column(DateTime, default=datetime.utcnow)  # 서버 기준 등록 시간
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)