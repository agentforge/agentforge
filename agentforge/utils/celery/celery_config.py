from celery import Celery
from celery.schedules import crontab
from celery.schedules import timedelta

celery_app = Celery(
    "tasks",
    broker="mongodb://localhost:27017",
    backend="mongodb://localhost:27017",
    include=["tasks"],
)

celery_app.conf.beat_schedule = {
    'run-master-scheduler-every-second': {
            'task': 'master_scheduler',
            #'schedule': timedelta(seconds=10), for testing
            'schedule': crontab(),
        }
}

# to start beat scheduler:
# celery -A tasks beat --loglevel=info  