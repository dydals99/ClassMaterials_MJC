from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from config.dbSettings import Base

#AI 에이전트 설정 정보를 저장하는 테이블
class Chatbot(Base):
    __tablename__ = "chatbots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)        
    description = Column(Text, nullable=True)         
    prompt = Column(Text, nullable=True)              
    temperature = Column(Float, default=0.7)          
    top_p = Column(Float, default=1.0)                
    created_at = Column(DateTime(timezone=True), server_default=func.now())

#사용자와 챗봇 간의 대화 기록을 저장하는 테이블
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id")) 
    role = Column(String(20))     
    content = Column(Text)        
    created_at = Column(DateTime(timezone=True), server_default=func.now())

#챗봇이 학습한 문서 정보를 저장하는 테이블
class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id", ondelete="CASCADE"))
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())