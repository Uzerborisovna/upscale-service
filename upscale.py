import cv2
from cv2 import dnn_superres
import numpy as np

MODEL_PATH = 'EDSR_x2.pb'
scaler = dnn_superres.DnnSuperResImpl_create()
scaler.readModel(MODEL_PATH)
scaler.setModel("edsr", 2)

def upscale_image(image_bytes: bytes) -> bytes:
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = scaler.upsample(image)
    _, encoded_image = cv2.imencode('.png', result)
    return encoded_image.tobytes()