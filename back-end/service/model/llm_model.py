import os
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash-lite"):
        self.model_name = model

    def get_response(self, messages, temperature: float = 0.2, top_p: float = 1.0):
        
        llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=2048,
        )   
        return llm.invoke(messages)

gemini_client = GeminiClient()