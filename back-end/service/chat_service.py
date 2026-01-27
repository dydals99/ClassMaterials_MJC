from sqlalchemy.orm import Session
from models.models import Chatbot, ChatHistory
from config.dbSettings import DATABASE_URL
from service.model.embedding import get_embeddings
from service.model.llm_model import gemini_client
from langchain_community.vectorstores import PGVector
from langchain_core.messages import SystemMessage, HumanMessage

class ChatService:
    def __init__(self):
        self.llm = gemini_client
        self.embeddings = get_embeddings()
        
        self.connection_string = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

    def get_chat_response(self, db: Session, chatbot_id: int, user_message: str):
        chatbot = db.query(Chatbot).filter(Chatbot.id == chatbot_id).first()
        if not chatbot:
            return "응답할 수 없습니다."

        context = self._get_relevant_context(chatbot_id, user_message)
        system_prompt = chatbot.prompt
        if context:
            system_prompt = f"""
                ### 지시 사항
                1. 아래 제공된 [지식 정보]를 바탕으로만 답변하세요.
                2. 답변은 반드시 마침표(.)로 끝나는 완성된 문장으로 마무리해야 합니다.
                3. **중요**: "더 궁금한 점이 있으시면..." 같은 맺음말은 절대 생략하고 본론만 작성하세요.

                ### [지식 정보]
                {context}

                ---
                위 지침에 따라 유저 질문에 핵심 위주로 답변하세요. (마지막 문장은 반드시 마침표로 끝낼 것)
            """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]

        ai_response = self.llm.get_response(
            messages=messages,
            temperature=chatbot.temperature,
            top_p=chatbot.top_p
        )
        self._save_history(db, chatbot_id, "user", user_message)
        self._save_history(db, chatbot_id, "assistant", ai_response.content)

        return ai_response.content

    def _get_relevant_context(self, chatbot_id: int, query: str) -> str:
        try:
            vector_db = PGVector(
                connection_string=self.connection_string,
                embedding_function=self.embeddings,
                collection_name=f"chatbot_{chatbot_id}"
            )
            
            # 유사도 검색 (상위 3개 문서 조각)
            docs = vector_db.similarity_search(query, k=3)
            return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"[Error] RAG 검색 실패: {e}")
            return ""

    def _save_history(self, db: Session, chatbot_id: int, role: str, content: str):
        history = ChatHistory(chatbot_id=chatbot_id, role=role, content=content)
        db.add(history)
        db.commit()

chat_service = ChatService()