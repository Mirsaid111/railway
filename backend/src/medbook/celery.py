import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medbook.settings')

app = Celery('medbook')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'
app.conf.timezone = 'UTC'