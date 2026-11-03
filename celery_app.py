
from celery import Celery

celery_app = Celery(
    'upscale_tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['tasks']
)