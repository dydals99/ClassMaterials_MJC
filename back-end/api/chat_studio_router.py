from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from config.dbSettings import get_db
from schemas.schemas import ChatbotResponse, ChatbotBase, KnowledgeResponse, ChatbotCreate
from models.models import Chatbot, Knowledge 
import os

router = APIRouter(prefix="/api/studio", tags=["Chatbot Studio"])

UPLOAD_DIR = "uploads/knowledge"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ChatbotResponse)
async def create_chatbot(chatbot: ChatbotCreate, db: Session = Depends(get_db)):
    db_bot = Chatbot(**chatbot.model_dump())
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

@router.get("/{chatbot_id}/files", response_model=List[KnowledgeResponse])
def get_chatbot_files(chatbot_id: int, db: Session = Depends(get_db)):
    files = db.query(Knowledge).filter(Knowledge.chatbot_id == chatbot_id).all() #
    return files

@router.put("/{chatbot_id}/settings", response_model=ChatbotResponse)
async def update_settings(chatbot_id: int, settings: ChatbotBase, db: Session = Depends(get_db)):
    db_bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first() #
    if not db_bot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    for key, value in settings.model_dump().items():
        setattr(db_bot, key, value)
    
    db.commit()
    db.refresh(db_bot)
    return db_bot

@router.post("/{chatbot_id}/learn")
async def learn_from_file(chatbot_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".txt"]:
        raise HTTPException(status_code=400, detail="PDF와 TXT 파일만 지원합니다.")

    file_path = os.path.join(UPLOAD_DIR, f"{chatbot_id}_{file.filename}")
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        new_knowledge = Knowledge( #
            chatbot_id=chatbot_id,
            file_name=file.filename,
            file_path=file_path
        )
        db.add(new_knowledge)
        db.commit()      
        db.refresh(new_knowledge) 
        return {"message": f"Successfully learned from {file.filename}", "knowledge_id": new_knowledge.id}
    except Exception as e:
        db.rollback() 
        if os.path.exists(file_path): os.remove(file_path) 
        raise HTTPException(status_code=500, detail=f"DB 저장 중 오류 발생: {str(e)}")