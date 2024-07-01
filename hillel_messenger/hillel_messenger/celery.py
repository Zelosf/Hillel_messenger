import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hillel_messenger.settings')

app = Celery(
	'hillel_messenger'
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)