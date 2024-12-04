import pytest
import app

@pytest.fixture
def client():
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client

def test_get_shops(client):
    response = client.get('/shops')
    assert response.status_code == 200

def test_create_shop(client):
    response = client.post('/shops', json={
        "contact_name": "Jane Doe",
        "email_address": "jane@example.com",
        "address": "123 Main St",
        "phone_number": "555-1234",
        "bicycle_idbicycle": 1
    })
    assert response.status_code == 201
    assert b"Shop created" in response.data
