from celery import Celery
from celery.schedules import crontab
from celery.schedules import timedelta

def create_celery_app():
    celery_app = Celery(
        "tasks",
        broker="mongodb://localhost:27017",
        backend="mongodb://localhost:27017",
        include=["tasks"],
    )

    celery_app.conf.beat_schedule = {
        'run-master-scheduler-every-second': {
            'task': 'master_scheduler',
            'schedule': crontab(),
        }
    }

    return celery_app

# to start beat scheduler:
# celery -A tasks beat --loglevel=info  