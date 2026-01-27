from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.dbSettings import get_db
from schemas.schemas import ChatbotCreate, ChatbotResponse
from models.models import Chatbot
from service.chat_list_service import chat_list_service
from typing import List

router = APIRouter(prefix="/api/chatbots", tags=["Chatbot List"])

#챗봇 조회
@router.get("/", response_model=List[ChatbotResponse])
async def get_chatbots(db: Session = Depends(get_db)):
    return chat_list_service.get_all_chatbots(db)

#챗봇 생성
@router.post("/", response_model=ChatbotResponse)
async def create_chatbot(chatbot: ChatbotCreate, db: Session = Depends(get_db)):
    return chat_list_service.create_new_chatbot(db, chatbot)

#챗봇 삭제
@router.delete("/{chatbot_id}")
async def delete_chatbot(chatbot_id: int, db: Session = Depends(get_db)):
    success = chat_list_service.delete_chatbot(db, chatbot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return {"message": "Deleted successfully"}