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


# 여행 성향 세부 점수
class TravelTraits(BaseModel):
    hotplace: int = 0
    waiting: int = 0
    crowd: int = 0
    planning: int = 0
    pace: int = 0


# 여행 성향 저장 요청
class TravelProfileCreate(BaseModel):
    client_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["38c1375c-9ec7-47d0-85fa-55c72aadf29a"],
    )

    main_type: str = Field(
        ...,
        examples=["local"],
    )

    main_title: str = Field(
        ...,
        examples=["로컬 감성 여행가"],
    )

    traits: TravelTraits

    tags: list[str] = Field(
        default_factory=list,
        examples=[
            [
                "숨은명소선호",
                "노웨이팅선호",
                "한적한분위기",
                "즉흥형",
                "한장소집중",
            ]
        ],
    )


# 여행 성향 조회 응답
class TravelProfileResponse(BaseModel):
    id: int
    client_id: str
    main_type: str
    main_title: str
    traits: TravelTraits
    tags: list[str]
    created_at: datetime
    modified_at: datetime