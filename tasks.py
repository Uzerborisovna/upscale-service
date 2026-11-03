
import uuid
from celery_app import celery_app
from upscale import upscale_image
import redis


redis_client = redis.Redis(host='redis', port=6379, db=0)


@celery_app.task(bind=True)
def upscale_task(self, image_bytes: bytes):
    """
    Задача для Celery. Принимает байты изображения,
    апскейлит его и сохраняет результат в Redis (в памяти).
    Возвращает ключ (ID), по которому можно достать файл.
    """

    file_key = str(uuid.uuid4())


    result_bytes = upscale_image(image_bytes)


    redis_client.set(file_key, result_bytes)

    return file_key