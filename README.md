# Academic Assignment Helper & Plagiarism Detector

A FastAPI-based academic assignment helper with RAG (Retrieval-Augmented Generation) for semantic search, integrated with **Postgres + pgvector** and **n8n workflow automation**.

---

## Features

- Store academic sources in Postgres with vector embeddings (pgvector)
- Query sources using semantic similarity (RAG)
- Automate data ingestion & tasks via n8n workflows
- Dockerized setup for easy deployment

---

## Prerequisites

- Docker & Docker Compose
- Python 3.11 (if running scripts locally)
- Optional: OpenAI API key (for full RAG functionality)

---

## Setup Instructions

1. **Clone the repository**
git clone <your_repo_url>
cd academic-assignment-helper

2. **Copy environment variables **
cp .env.example .env
# Add your OPENAI_API_KEY if available


3. **Start services using Docker Compose**
docker compose up -d --build


4. **Seed sample academic sources**
docker exec -it fastapi_backend python seed_academic_sources.py


5. **Verify backend is running**
curl http://localhost:8000/academic_sources


6. **Access n8n workflow UI**
Open http://localhost:5678 in your browser
Import or run n8n_workflows/workflow_export.json

---

## Sample Data

data/sample_academic_sources.json contains a few academic sources for testing:

[
  {
    "title": "Sample Paper 1",
    "authors": "John Doe",
    "abstract": "This is a sample abstract.",
    "source_type": "journal"
  },
  {
    "title": "Sample Paper 2",
    "authors": "Jane Smith",
    "abstract": "Another sample abstract.",
    "source_type": "conference"
  }
]

Environment Variables (.env.example)
DATABASE_URL=postgresql://student:password@academic_db:5432/academic_helper
OPENAI_API_KEY=your_openai_key_here


Replace your_openai_key_here with a valid key if you want RAG queries to work.

---

## Demo Instructions

- Start all services: docker compose up -d
- Seed data: docker exec -it fastapi_backend python seed_academic_sources.py
- Open n8n UI: http://localhost:5678
- Trigger workflow → check backend responses via API or logs
- Use sample API call:
    curl http://localhost:8000/academic_sources

---

## Notes

- The RAG service is included in backend/rag_service.py.
- If OpenAI API is not configured, the service will return sample/dummy data.
- All services are fully Dockerized; no local installation of Postgres is required.