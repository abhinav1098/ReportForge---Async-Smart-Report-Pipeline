from app.core.celery_app import celery_app

# ensure task registration
import app.tasks.report_tasks  # noqa: F401
