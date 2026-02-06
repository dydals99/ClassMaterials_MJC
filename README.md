# ClassMaterials_MJC
명지전문대학 예비대학 수업자료
RAG(Retrieval-Augmented Generation) 기반으로<br> PDF 문서를 벡터화하여 저장하고, 사용자 질문에 대해 관련 문서를 검색하여 답변을 제공합니다.

## 프로젝트 개요

이 프로젝트는 RAG 기반 챗봇입니다. 아래와 같이 구성되었습니다. 

### 개발 환경 

#2496ED

### 주요 기능
- **RAG 기반 챗봇**: PDF 문서를 벡터화하여 저장하고 의미 기반 검색 수행
- **벡터 검색**: PostgreSQL + pgvector를 활용한 고성능 벡터 검색

## 실행 방법
### Docker 설치
https://www.docker.com/products/docker-desktop/

### Docker Compose 명령어
#### 실행
```bash
docker-compose up --bulid -d
```
#### 종료/ 종료 및 불륨 삭제
```bash
docker-compose down
docker-compose down -v
```

## 환경변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `POSTGRES_USER` | PostgreSQL 사용자명 | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL 비밀번호 | `1234` |
| `POSTGRES_DB` | PostgreSQL 데이터베이스명 | `study_chatbot` |
| `POSTGRES_HOST` | PostgreSQL 호스트 | `db` |
| `POSTGRES_PORT` | PostgreSQL 포트 | `5432` |
| `GOOGLE_API_KEY` | Google Gemini API 키 | `your-google-api-key-here` |

### 환경변수 파일 예시 (.env)

```bash
# DB설정
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=study_chatbot
```

### 

DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://postgres:1234@db:5432/study_chatbot

GOOGLE_API_KEY=your-google-api-key-here
```
