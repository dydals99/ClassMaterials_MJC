import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# 우리가 만든 모듈들 임포트
from config.dbSettings import engine, Base
from api.chat_list_router import router as list_router
from api.chat_studio_router import router as studio_router
from api.chat_router import router as chat_router

# 1. 데이터베이스 테이블 생성
# 앱이 시작될 때 models.py에 정의된 테이블이 DB에 없으면 자동으로 만듭니다.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI CS Agent Automation",
    description="CS 업무 자동화를 위한 AI 에이전트 서비스"
)

# 2. CORS 설정 (필요 시)
# 다른 도메인에서 접근할 때 보안 문제를 방지합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 라우터 등록
app.include_router(list_router)    # 챗봇 목록 및 기본 관리
app.include_router(studio_router)  # 챗봇 상세 설정 및 RAG 학습
app.include_router(chat_router)    # 실제 AI 채팅 로직

# 4. 정적 파일 마운트 
app.mount("/static", StaticFiles(directory="/front-end"), name="static")

# 5. HTML 페이지 서빙
@app.get("/")
async def read_index():
    # 이제 static/이 아니라 /front-end/에서 직접 파일을 찾습니다.
    return FileResponse("/front-end/chatlist.html")

@app.get("/studio")
async def read_studio():
    return FileResponse("/front-end/chatstudio.html")

@app.get("/chat")
async def read_chat():
    return FileResponse("/front-end/chatpage.html")

if __name__ == "__main__":
    # 로컬에서 직접 실행할 때 사용 (uvicorn main:app --reload 와 동일)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)