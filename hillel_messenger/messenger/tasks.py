from .models import Message
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def get_last_ten_messages():
	last_ten_messages = Message.objects.order_by('-created_at')[:10]
	for message in last_ten_messages:
		logger.info(f'"{message.content}" created by "{message.author}" ("{message.created_at}")')