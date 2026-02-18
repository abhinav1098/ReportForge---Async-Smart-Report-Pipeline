from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, cast

from celery.app.task import Task

from app.database import get_db
from app import models, schemas
from app.tasks.report_tasks import generate_report

# ⭐ tell Pylance this is a Celery Task
generate_report = cast(Task, generate_report)

router = APIRouter(prefix="/reports", tags=["Reports"])


# Create report
@router.post(
    "",
    response_model=schemas.ReportOut,
    status_code=status.HTTP_201_CREATED,
)
def create_report(
    payload: schemas.ReportCreate,
    db: Session = Depends(get_db),
):
    report = models.Report(title=payload.title)

    db.add(report)
    db.commit()
    db.refresh(report)

    # 🔥 async trigger
    cast(Task, generate_report).delay(report.id)

    return report


# List reports
@router.get("", response_model=List[schemas.ReportOut])
def list_reports(db: Session = Depends(get_db)):
    return db.query(models.Report).order_by(models.Report.id.desc()).all()


# Get single report
@router.get("/{report_id}", response_model=schemas.ReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = (
        db.query(models.Report)
        .filter(models.Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report

# 🗑️ Delete report
@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = (
        db.query(models.Report)
        .filter(models.Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()
