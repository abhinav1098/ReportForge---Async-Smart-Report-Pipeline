# 🚀 ReportForge — Async Smart Report Pipeline

A production-ready distributed report generation system built with FastAPI, Celery, Redis, PostgreSQL, React, and Docker.

ReportForge demonstrates how modern backend systems handle long-running jobs asynchronously with retries, background workers, and real-time UI polling.

---

## 🏗 Architecture Overview

ReportForge follows an event-driven async architecture:

React UI → FastAPI API → PostgreSQL
│
└── Celery Worker → Redis Broker → Background Processing


### Flow

1. User creates report from UI  
2. FastAPI stores report (status: pending)  
3. Celery worker picks up job  
4. Worker processes report with retry logic  
5. UI polls backend for live status updates  
6. User can delete reports instantly  

---

## ✨ Features

### 🔐 Backend

- FastAPI REST API
- SQLAlchemy ORM
- PostgreSQL database
- Celery background workers
- Redis message broker
- Automatic retry with exponential backoff
- Status lifecycle tracking:
- pending → processing → retrying → completed → failed
- Production-ready Docker setup
- Environment-based configuration

---

### 🎨 Frontend

- React + Vite
- TypeScript
- TanStack React Query
- Optimistic UI updates
- Live polling dashboard
- Per-row mutation locking
- Status badges with visual states
- Nginx production container

---

### 🐳 DevOps

- Multi-service Docker Compose
- Backend container
- Worker container
- Redis container
- PostgreSQL container
- Frontend Nginx container
- Ready for cloud deployment

---

## 📁 Project Structure

ReportForge/
├── backend/
│ ├── app/
│ │ ├── routers/
│ │ ├── tasks/
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── database.py
│ │ └── main.py
│ ├── worker.py
│ └── Dockerfile
│
├── frontend/
│ ├── src/
│ └── Dockerfile
│
└── docker-compose.yml


---

## 🚀 Run with Docker (Recommended)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ReportForge.git
cd ReportForge
2️⃣ Start all services
docker compose up --build
3️⃣ Access the app
Service	URL
Frontend	http://localhost:5174
Backend API	http://localhost:8000
Swagger Docs	http://localhost:8000/docs

```

🔄 Report Lifecycle
Each report moves through states:


pending → processing → retrying → completed
↘ failed (after max retries)

The UI reflects these states in real time.

⚙️ Environment Variables
Create:

backend/.env
Example:

DATABASE_URL=postgresql+psycopg://postgres:postgres@postgres:5432/reports_db

REDIS_URL=redis://redis:6379/0

ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174


🧠 Why This Project Matters
ReportForge demonstrates real-world backend patterns:

Async job processing

Distributed workers

Message queues

Retry-safe pipelines

Optimistic frontend UX

Container orchestration

Production-style architecture

This mirrors how systems like:

email pipelines

video processors

analytics jobs

AI batch systems

are built in industry.

🚀 Future Improvements
WebSocket live updates

S3 report storage

RBAC / authentication

CI/CD pipeline

Kubernetes deployment

Observability (Prometheus/Grafana)

📜 License
MIT License © 2026 Abhinav K
