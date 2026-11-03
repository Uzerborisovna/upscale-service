
from flask import Flask, request, jsonify, Response
from tasks import upscale_task
from celery.result import AsyncResult
from celery_app import celery_app
import redis

app = Flask(__name__)


redis_client = redis.Redis(host='redis', port=6379, db=0)



@app.route('/upscale', methods=['POST'])
def upscale():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    image_bytes = file.read()
    task = upscale_task.delay(image_bytes)
    return jsonify({"task_id": task.id}), 202



@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = AsyncResult(task_id, app=celery_app)

    if task.state == 'PENDING':
        response = {"status": "PENDING"}
    elif task.state == 'SUCCESS':
        file_key = task.result
        response = {
            "status": "SUCCESS",
            "file_url": f"/processed/{file_key}"
        }
    elif task.state == 'FAILURE':
        response = {"status": "FAILURE", "error": str(task.info)}
    else:
        response = {"status": task.state}

    return jsonify(response)



@app.route('/processed/<path:file_key>', methods=['GET'])
def get_processed_file(file_key):
    file_bytes = redis_client.get(file_key)
    if not file_bytes:
        return jsonify({"error": "File not found"}), 404

    return Response(file_bytes, mimetype='image/png')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)