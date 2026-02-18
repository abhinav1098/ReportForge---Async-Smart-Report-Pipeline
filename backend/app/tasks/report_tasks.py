import time
import random
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.database import SessionLocal
from app import models


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def generate_report(self, report_id: int):
    db: Session = SessionLocal()

    try:
        report = db.query(models.Report).filter(
            models.Report.id == report_id
        ).first()

        if not report:
            return

        # mark processing
        report.status = "processing"
        db.commit()

        # simulate heavy work
        time.sleep(5)

        # simulate random failure
        if random.random() < 0.2:
            raise Exception("Simulated report failure")

        # success
        report.status = "completed"
        report.result_url = f"/reports/{report_id}.txt"
        report.completed_at = datetime.utcnow()
        db.commit()

    except Exception as e:
        report = db.query(models.Report).filter(
            models.Report.id == report_id
        ).first()

        if report:
            report.retry_count += 1
            db.commit()

        # final failure
        if self.request.retries >= self.max_retries:
            if report:
                report.status = "failed"
                db.commit()

        raise e

    finally:
        db.close()
