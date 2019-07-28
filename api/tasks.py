from celery import shared_task
from celery.utils.log import get_task_logger


logger=get_task_logger(__name__)

# This is the decorator which a celery worker uses
@shared_task(name="get bot response")
def send_data(response_data):
    logger.info("Spoke to bot")
    return send_data(response_data)
