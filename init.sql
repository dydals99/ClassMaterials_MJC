--PostgreSQL 벡터 확장
CREATE EXTENSION IF NOT EXISTS vector;

--챗봇 관리 테이블
CREATE TABLE IF NOT EXISTS chatbots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    prompt TEXT,
    temperature FLOAT DEFAULT 0.7,
    top_p FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--채팅 기록 테이블
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    chatbot_id INTEGER REFERENCES chatbots(id),
    role VARCHAR(20),
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);