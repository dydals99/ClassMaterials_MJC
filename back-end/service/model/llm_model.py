import os
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        # 초기화 시에는 기본 구조만 잡습니다.
        # 실제 API 키는 환경 변수에서 자동으로 읽어옵니다.
        self.model_name = model

    def get_response(self, messages, temperature: float = 0.2, top_p: float = 1.0):
        """
        메시지와 함께 사용자가 설정한 파라미터를 받아 답변을 생성합니다.
        """
        # 호출 시점에 파라미터를 적용한 새로운 LLM 객체를 생성하거나 
        # 기존 객체의 설정을 바인딩합니다.
        llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=2048,
        )
        
        return llm.invoke(messages)

# 싱글톤으로 관리하여 모델 이름 등 기본 설정을 공유합니다.
gemini_client = GeminiClient()