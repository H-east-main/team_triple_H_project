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
    

class TravelProfile(Base):
    __tablename__ = "travel_profiles"

    id = Column(Integer, primary_key=True, index=True)

    # 로그인 대신 브라우저를 구분하기 위한 익명 ID
    client_id = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    # 메인 여행 성향
    main_type = Column(
        String(30),
        nullable=False,
    )

    main_title = Column(
        String(100),
        nullable=False,
    )

    # 세부 성향 점수
    hotplace_score = Column(Integer, nullable=False, default=0)
    waiting_score = Column(Integer, nullable=False, default=0)
    crowd_score = Column(Integer, nullable=False, default=0)
    planning_score = Column(Integer, nullable=False, default=0)
    pace_score = Column(Integer, nullable=False, default=0)

    # 태그 목록을 JSON 문자열로 저장
    tags = Column(
        Text,
        nullable=False,
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