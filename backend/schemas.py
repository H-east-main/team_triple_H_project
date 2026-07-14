# backend/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# 공통 필드 정의
class PostBase(BaseModel):
    category: str = Field(..., example="강원권")
    title: str = Field(..., max_length=100, example="속초 맛집 추천합니다")
    content: str = Field(..., example="중앙시장에 가면 닭강정은 꼭 드세요.")

# 1. 작성(Create) 요청용 스키마: 비밀번호 필수 필수
class PostCreate(PostBase):
    password: str = Field(..., min_length=4, example="1234")

# 2. 수정(Update) 요청용 스키마: 검증용 비밀번호 포함
class PostUpdate(PostBase):
    password: str = Field(..., example="1234")

# 3. 응답(Response) 반환용 스키마: ★비밀번호(password) 제외 보안 유지
class PostResponse(PostBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy ORM 객체를 Pydantic이 자동 변환해줌