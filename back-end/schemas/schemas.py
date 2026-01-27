from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class ChatbotBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    prompt: Optional[str] = None
    temperature: float = Field(0.7, ge=0, le=1.0)
    top_p: float = Field(1.0, ge=0, le=1.0)

class ChatbotCreate(ChatbotBase):
    pass

class ChatbotResponse(ChatbotBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ChatRequest(BaseModel):
    chatbot_id: int
    message: str

class ChatResponse(BaseModel):
    chatbot_id: int
    response: str

class ChatHistoryResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class KnowledgeResponse(BaseModel):
    id: int
    chatbot_id: int
    file_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)