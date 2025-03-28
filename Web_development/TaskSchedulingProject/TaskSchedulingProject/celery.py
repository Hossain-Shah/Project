import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskSchedulingProject.settings')
app = Celery('TaskSchedulingProject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()