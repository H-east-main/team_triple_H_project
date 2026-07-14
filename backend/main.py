# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os, json

import backend.models as models, backend.schemas as schemas
from backend.database import engine, get_db

# 애플리케이션 시작 시 DB 테이블 자동 생성 (Migration 대용)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anonymous Region Community API")

# 프론트엔드(Vue.js) 연동을 위한 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실무 배포 시에는 Netlify URL 주소만 딱 넣어야 해
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# JSON 파일 경로 지정
JSON_PATH = os.path.join("local_infos", "광주_전라권_관광지.json")

# [CREATE] 게시글 작성
@app.post("/api/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)  # DB에서 자동 생성된 id와 created_at을 반영
    return db_post

# [READ] 게시글 전체 목록 조회 (카테고리 필터링 포함)
@app.get("/api/posts", response_model=List[schemas.PostResponse])
def read_posts(category: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Post)
    if category:
        query = query.filter(models.Post.category == category)
    return query.order_by(models.Post.created_at.desc()).all()

# [READ] 게시글 상세 조회
@app.get("/api/posts/{post_id}", response_model=schemas.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return db_post

# [UPDATE] 게시글 수정 (평문 비밀번호 대조 검증)
@app.put("/api/posts/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    # 요구사항: 평문 패스워드 검증 규칙 적용
    if db_post.password != updated_post.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다 권한이 없습니다.")
    
    # 데이터 업데이트
    db_post.title = updated_post.title
    db_post.content = updated_post.content
    db_post.category = updated_post.category
    
    db.commit()
    db.refresh(db_post)
    return db_post

# [DELETE] 게시글 삭제 (Query Parameter로 비밀번호 수신)
@app.delete("/api/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, password: str, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    # 요구사항: 평문 패스워드 검증 규칙 적용
    if db_post.password != password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다 권한이 없습니다.")
    
    db.delete(db_post)
    db.commit()
    return {"status": "success", "message": "게시글이 삭제되었습니다."}



@app.get("/api/spots")
def get_spots():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # 공공데이터 특유의 구조(response -> body -> items -> item)에 따른 안전한 파싱
        # 데이터 구조가 다를 경우를 대비해 예외처리를 꼼꼼하게 다듬었습니다.
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        
        # 리스트 형태가 아니라 단일 딕셔너리로 들어올 경우를 대비한 방어 코드
        if isinstance(items, dict):
            items = [items]
            
        return items
    except Exception as e:
        return {"error": f"파일을 읽는 중 오류가 발생했습니다: {str(e)}"}
