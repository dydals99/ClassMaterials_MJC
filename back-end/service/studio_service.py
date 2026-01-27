import os
from sqlalchemy.orm import Session
from fastapi import UploadFile
from models.models import Knowledge
from config.dbSettings import GOOGLE_API_KEY, DATABASE_URL
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from service.model.embedding import get_embeddings

class StudioService:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.connection_string = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")

    async def save_and_learn_file(self, db: Session, chatbot_id: int, file: UploadFile):
        upload_dir = f"static/uploads/{chatbot_id}"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(documents)

        vector_db = PGVector.from_documents(
            documents=splits,
            embedding=self.embeddings,
            connection_string=self.connection_string,
            collection_name=f"chatbot_{chatbot_id}",
            use_jsonb=True
        )

        new_knowledge = Knowledge(
            chatbot_id=chatbot_id,
            file_name=file.filename,
            file_path=file_path
        )
        db.add(new_knowledge)
        db.commit()
        db.refresh(new_knowledge)

        return new_knowledge

studio_service = StudioService()