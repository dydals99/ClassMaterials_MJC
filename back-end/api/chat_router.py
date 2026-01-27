from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # 추가
from config.dbSettings import get_db
from schemas.schemas import ChatRequest, ChatResponse, ChatHistoryResponse
from models.models import ChatHistory  # [중요] DB 모델 임포트!
from service.chat_service import chat_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])

@router.get("/history/{chatbot_id}", response_model=List[ChatHistoryResponse]) # response_model 추가 추천
def get_history(chatbot_id: int, db: Session = Depends(get_db)):
    try:
        # [수정] ChatHistoryResponse(스키마) 대신 ChatHistory(모델)를 쿼리해야 합니다.
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