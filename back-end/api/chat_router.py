from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # 추가
from config.dbSettings import get_db
from schemas.schemas import ChatRequest, ChatResponse, ChatHistoryResponse
from models.models import ChatHistory  
from service.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.get("/history/{chatbot_id}", response_model=List[ChatHistoryResponse]) 
def get_history(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        history = db.query(ChatHistory).filter(ChatHistory.chatbot_id == chatbot_id).order_by(ChatHistory.id.asc()).all()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        response_content = chat_service.get_chat_response(
            db, 
            request.chatbot_id, 
            request.message
        )
        return ChatResponse(
            chatbot_id=request.chatbot_id,
            response=response_content
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))