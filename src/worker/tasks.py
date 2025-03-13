from celery import shared_task


from src.worker.clients.bins import (
    UpdateServiceIdHandler,
)
from src.worker.clients.clients import (
    save_data,
)


@shared_task(queue='nightly_task')
def get_client_info_service_hourly_task():
    save_data(session)

@shared_task(queue='nightly_task')
def update_service_id():
    return UpdateServiceIdHandler(session)()
