import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from config.dbSettings import engine, Base
from api.chat_list_router import router as list_router
from api.chat_studio_router import router as studio_router
from api.chat_router import router as chat_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MY AI Chat Bot",
    description="나만의 챗봇 만들기"
)

app.include_router(list_router)  
app.include_router(studio_router)  
app.include_router(chat_router)    

app.mount("/static", StaticFiles(directory="/front-end"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("/front-end/chatlist.html")

@app.get("/studio")
async def read_studio():
    return FileResponse("/front-end/chatstudio.html")

@app.get("/chat")
async def read_chat():
    return FileResponse("/front-end/chatpage.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)