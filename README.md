# team_triple_H_project
Start Camp 바이브 코딩 팀 프로젝트 레포지토리

project_dir/
├── .git/
├── .gitignore               # 프로젝트 전체용 (또는 하위 폴더에 각각 배치 가능)
├── README.md                # 전체 프로젝트 개요 및 배포 URL 기재
│
├── backend/                 # [Render 배포 영역]
│   ├── main.py              # FastAPI 진입점 (익명 CRUD, /api/chat 엔드포인트)
│   ├── database.py          # SQLAlchemy 연결 설정
│   ├── models.py            # SQLite 테이블 스키마 (posts 등)
│   ├── schemas.py           # Pydantic 모델
│   ├── local_info.json      # 당사 제공 원본 JSON 데이터
│   ├── lclsSystemCode.json  # 분류 체계 코드 JSON 파일
│   ├── .env                 # API 키, DB 경로 등 민감정보 (★절대 Git 커밋 금지)
│   ├── .gitignore           # backend 용 .env, .db, __pycache__ 제외 설정
│   ├── community.db         # 로컬 테스트용 SQLite 파일 (자동 생성됨)
│   └── requirements.txt     # 백엔드 의존성 패키지 목록 (fastapi, uvicorn, openai 등)
│
└── frontend/                # [Netlify 배포 영역]
    ├── index.html
    ├── package.json         # 프론트엔드 의존성 패키지 목록 (vue, axios, vite 등)
    ├── vite.config.js       # Vite 설정 파일
    ├── .env.production      # 배포 시 사용할 Render 백엔드 주소 (VITE_API_URL)
    ├── .env.local           # 로컬 개발 시 사용할 백엔드 주소 (http://localhost:8000)
    ├── .gitignore           # frontend 용 node_modules, dist 등 제외 설정
    ├── public/
    │   └── favicon.ico
    └── src/
        ├── main.js          # Vue.js 진입점
        ├── App.vue          # 최상위 루트 컴포넌트
        ├── assets/          # CSS, 이미지 등 정적 자원
        ├── components/
        │   └── ChatBot.vue  # 요구사항: 챗봇 UI 컴포넌트 (플로팅, 히스토리 유지)
        └── views/           # 요구사항: 1개 권역 카테고리 게시판 화면들
            ├── PostList.vue # 게시글 목록 조회 화면
            ├── PostDetail.vue # 게시글 상세 조회 화면
            └── PostForm.vue   # 게시글 작성 및 수정 화면 (비밀번호 입력 포함)
