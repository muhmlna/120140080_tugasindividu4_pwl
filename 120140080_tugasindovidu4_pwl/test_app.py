import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/register', json={'username': 'newuser', 'password': 'password'})
    assert response.status_code == 201

def test_login(client):
    response = client.post('/login', json={'username': 'newuser', 'password': 'password'})
    assert response.status_code == 200

def test_protected(client):
    response = client.get('/protected')
    assert response.status_code == 401  

    # guji endpoint protected dengan token akses
    response = client.get('/protected', headers={'Authorization': 'Bearer <TOKEN_AKSES>'})
    assert response.status_code == 200
