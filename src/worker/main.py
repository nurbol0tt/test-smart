import logging
from datetime import timedelta

from dotenv import load_dotenv

from celery import Celery

from src.core.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')  # Получаем логгер для SQLAlchemy

logger.setLevel(logging.WARNING)

celery = Celery(
    'tasks',
    broker=settings.BROKER,
    backend=settings.BACKEND,
    include=['src.worker.tasks']
)

# Define the Celery Beat schedule
celery.conf.beat_schedule = {
    # 'hourly_task': {
    #     'task': 'src.worker.tasks.get_client_info_service_hourly_task',
    #     'schedule': timedelta(
    #         # days=int(os.environ.get('CELERY_SCHEDULE_DAYS', 1)),
    #         # minutes=int(os.environ.get('CELERY_SCHEDULE_HOURS', 60))
    #         hours=3
    #     ),
    #     'options': {'queue': 'nightly_task'}
    # },
    'save_data_bins_task': {
        'task': 'src.worker.tasks.save_data_bins',
        'schedule': timedelta(
            hours=3
        ),
        'options': {'queue': 'nightly_task'}
    },
    'update_service_id_task': {
        'task': 'src.worker.tasks.update_service_id',
        'schedule': timedelta(
            hours=3
        ),
        'options': {'queue': 'nightly_task'}
    }
}
celery.conf.broker_connection_retry_on_startup = True
