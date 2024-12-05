from datetime import timedelta
from celery import Celery

from app.core.config import settings


celery = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["app.tasks.tasks"],
)

celery.autodiscover_tasks()

celery.conf.beat_schedule = {
    "pg_backup_every_8h": {
        "task": "app.tasks.tasks.pg_backup",
        "schedule": timedelta(hours=8),
    }
}
