# backend/schemas.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# 게시글 공통 필드
class PostBase(BaseModel):
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        examples=["관광지"],
    )

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["광주 여행지 추천합니다"],
    )

    content: str = Field(
        ...,
        min_length=1,
        examples=["무등산에 다녀왔습니다."],
    )

    # 입력하지 않으면 프론트엔드에서 기본 이미지 사용
    image_url: Optional[str] = Field(
        default=None,
        examples=[
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
            "?auto=format&fit=crop&w=1200&q=80"
        ],
    )


# 게시글 작성 요청
class PostCreate(PostBase):
    password: str = Field(
        ...,
        min_length=4,
        max_length=50,
        examples=["1234"],
    )


# 게시글 수정 요청
class PostUpdate(PostBase):
    password: str = Field(
        ...,
        min_length=4,
        max_length=50,
        examples=["1234"],
    )


# 게시글 조회 응답
class PostResponse(PostBase):
    id: int
    created_at: datetime

    # SQLAlchemy ORM 객체를 Pydantic 응답으로 변환
    model_config = ConfigDict(from_attributes=True)