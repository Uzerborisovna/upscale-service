
import io
import pytest
from app import app
from PIL import Image


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_upscale_endpoint(client):

    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)


    response = client.post('/upscale', data={'file': (img_byte_arr, 'test.png')})

    assert response.status_code == 202
    assert 'task_id' in response.get_json()


def test_get_task_status(client):

    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f'/tasks/{fake_id}')


    assert response.status_code == 200
    assert 'status' in response.get_json()


def test_get_processed_file_not_found(client):
    response = client.get('/processed/nonexistent.png')

    assert response.status_code == 404