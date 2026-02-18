from pydantic import BaseModel
from datetime import datetime


class ReportCreate(BaseModel):
    title: str


class ReportOut(BaseModel):
    id: int
    title: str
    status: str
    result_url: str | None
    retry_count: int
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True
