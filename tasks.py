import uuid
from celery_app import celery_app
from upscale import upscale_image
import redis

redis_client = redis.Redis(host='redis', port=6379, db=0)

TTL_SECONDS = 3600

@celery_app.task(bind=True)
def upscale_task(self, image_bytes: bytes):
    file_key = str(uuid.uuid4())
    result_bytes = upscale_image(image_bytes)
    redis_client.setex(file_key, TTL_SECONDS, result_bytes)
    return file_key