from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from config.dbSettings import get_db
from schemas.schemas import ChatbotResponse, ChatbotBase
from models.models import Chatbot
import shutil
import os

router = APIRouter(prefix="/api/studio", tags=["Chatbot Studio"])

# 1. 챗봇 상세 설정 업데이트 (프롬프트, 파라미터)
@router.put("/{chatbot_id}/settings", response_model=ChatbotResponse)
async def update_settings(chatbot_id: int, settings: ChatbotBase, db: Session = Depends(get_db)):
    db_bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
    if not db_bot:
        return {"error": "Chatbot not found"}
    
    for key, value in settings.model_dump().items():
        setattr(db_bot, key, value)
    
    db.commit()
    db.refresh(db_bot)
    return db_bot

# 2. 지식 학습 (RAG) - 파일 업로드 및 벡터화
@router.post("/{chatbot_id}/learn")
async def learn_from_file(
    chatbot_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # 파일 확장자 확인
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".txt"]:
        return {"error": "Only PDF and TXT files are supported"}

    # 임시 저장 및 텍스트 추출 로직 (Service에서 처리 권장)
    # 여기서는 흐름만 보여드립니다.
    content = await file.read()
    
    # [TODO] studio_service.embed_file(chatbot_id, content, ext) 호출
    # 1. 텍스트 추출 -> 2. Chunk 분할 -> 3. Gemini Embedding 생성 -> 4. pgvector 저장
    
    return {"message": f"Successfully learned from {file.filename}"}