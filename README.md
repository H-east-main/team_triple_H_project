# team_triple_H_project
Start Camp 바이브 코딩 팀 프로젝트 레포지토리



## 📂 프로젝트 디렉토리 구조 (Directory Structure)

```text
project_dir/
├── .git/
├── .gitignore               # 프로젝트 전체 통합용 제외 설정
├── README.md                # 전체 프로젝트 개요 및 배포 URL 기재
│
├── backend/                 # [Backend] Render 배포 서비스 영역
│   ├── main.py              # FastAPI 진입점 (익명 CRUD, /api/chat 엔드포인트)
│   ├── database.py          # SQLAlchemy 연결 및 세션 설정
│   ├── models.py            # SQLite 테이블 스키마 (posts 등)
│   ├── schemas.py           # Pydantic 데이터 검증 모델
│   ├── local_info.json      # 한국관광공사 제공 원본 JSON 데이터
│   ├── lclsSystemCode.json  # 분류 체계 코드 매핑 JSON 파일
│   ├── .env                 # API 키, DB 경로 등 민감정보 (★Git 커밋 절대 금지)
│   ├── .gitignore           # backend 전용 제외 설정 (.env, .db, __pycache__)
│   ├── community.db         # 로컬 테스트용 SQLite 파일 (구동 시 자동 생성)
│   └── requirements.txt     # 백엔드 의존성 패키지 목록 (FastAPI, Uvicorn, OpenAI 등)
│
└── frontend/                # [Frontend] Netlify 배포 서비스 영역
    ├── index.html           # SPA 메인 HTML 마스터 파일
    ├── package.json         # 프론트엔드 의존성 패키지 목록 (Vue 3, Axios, Vite 등)
    ├── vite.config.js       # Vite 빌드 및 개발 서버 설정 파일
    ├── .env.production      # 프로덕션 배포 시 사용할 Render 백엔드 API 주소
    ├── .env.local           # 로컬 개발 시 사용할 백엔드 주소 (http://localhost:8000)
    ├── .gitignore           # frontend 전용 제외 설정 (node_modules, dist 등)
    ├── public/
    │   └── favicon.ico      # 브라우저 탭 아이콘
    └── src/
        ├── main.js          # Vue.js 애플리케이션 진입점
        ├── App.vue          # 최상위 루트 컴포넌트
        ├── assets/          # 글로벌 CSS 스타일 및 정적 자원
        ├── components/
        │   └── ChatBot.vue  # [필수] 챗봇 UI 컴포넌트 (플로팅, 히스토리 유지, 모바일 대응)
        └── views/           # [필수] 1개 권역 카테고리 게시판 화면 정의
            ├── PostList.vue # 게시글 목록 조회 화면
            ├── PostDetail.vue # 게시글 상세 조회 화면
            └── PostForm.vue   # 게시글 작성 및 수정 화면 (수정용 비밀번호 처리 포함)

## 게시판 
<img width="1385" height="745" alt="image" src="https://github.com/user-attachments/assets/2d0f2f35-6a24-4d0a-aa55-e4a6def46f75" />

