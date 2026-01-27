from langchain_huggingface import HuggingFaceEmbeddings

# 전역 변수로 선언하여 모델이 한 번만 메모리에 로드되도록 설정
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        print("[System] KURE-v1 한국어 임베딩 모델 로딩 시작...")
        embedding_model_name = 'nlpai-lab/KURE-v1'
        _embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={'device': 'cpu'}  # 로컬 개발 환경에 맞춰 CPU 사용
        )
        print("[System] 임베딩 모델 로드 완료.")
    return _embeddings