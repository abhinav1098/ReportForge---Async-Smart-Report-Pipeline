from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import Base, engine
from app.routers import reports

app = FastAPI(title="Smart Report Generator API")

# Create tables (dev-safe; later Alembic in real prod)
Base.metadata.create_all(bind=engine)

# CORS
origins = [o.strip() for o in settings.allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(reports.router)


@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "smart-report-generator",
    }
