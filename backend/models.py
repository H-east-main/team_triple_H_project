# backend/models.py

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    category = Column(
        String(50),
        index=True,
        nullable=False,
    )

    title = Column(
        String(100),
        index=True,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    # 교육 목적의 평문 비밀번호
    password = Column(
        String(50),
        nullable=False,
    )

    # 이미지 미입력 시 프론트엔드에서 기본 이미지 표시
    image_url = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    modified_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )