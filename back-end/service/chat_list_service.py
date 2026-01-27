from sqlalchemy.orm import Session
from models.models import Chatbot
from schemas.schemas import ChatbotCreate

#전체 챗봇 조회
class ChatListService:
    def get_all_chatbots(self, db: Session):

        return db.query(Chatbot).all()

    #새로운 챗봇 기본 정보 저장
    def create_new_chatbot(self, db: Session, chatbot_data: ChatbotCreate):

        db_chatbot = Chatbot(**chatbot_data.model_dump())
        db.add(db_chatbot)
        db.commit()
        db.refresh(db_chatbot)
        return db_chatbot
    
    #챗봇 삭제
    def delete_chatbot(self, db: Session, chatbot_id: int):
  
        db_bot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
        if db_bot:
            db.delete(db_bot)
            db.commit()
            return True
        return False

chat_list_service = ChatListService()