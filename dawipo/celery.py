import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dawipo.settings')

app = Celery('dawipo')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()