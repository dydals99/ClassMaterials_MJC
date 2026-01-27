from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from config.dbSettings import get_db
from schemas.schemas import ChatbotResponse, ChatbotBase
from models.models import Chatbot
from models.models import Knowledge 
import os

router = APIRouter(prefix="/api/studio", tags=["Chatbot Studio"])

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

UPLOAD_DIR = "uploads/knowledge"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        new_knowledge = Knowledge(
            chatbot_id=chatbot_id,
            file_name=file.filename,
            file_path=file_path
        )
        
        db.add(new_knowledge)
        db.commit()      
        db.refresh(new_knowledge) 

        return {
            "message": f"Successfully learned from {file.filename}",
            "knowledge_id": new_knowledge.id
        }
        
    except Exception as e:
        db.rollback() 
        if os.path.exists(file_path):
            os.remove(file_path) 
        raise HTTPException(status_code=500, detail=f"DB 저장 중 오류 발생: {str(e)}")