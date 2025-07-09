
import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_get_book_genre(client):
    response = client.post('/api/book/genre', 
                          json={'title': 'Dune', 'author': 'Frank Herbert'})
    assert response.status_code == 200
    assert 'genre' in response.json

def test_invalid_book_genre(client):

    response = client.post('/api/book/genre', json={'title': 'Dune'}) 
    assert response.status_code == 400
    assert 'error' in response.get_json()