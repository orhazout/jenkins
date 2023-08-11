import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_user(client):
    # Test adding a user to the database
    response = client.post('/add', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'phone': '555-1234',
        'email': 'johndoe@example.com',
        'profession': 'Software Engineer',
        'introduction': 'I am a software engineer.',
        'education': 'Bachelor of Science in Computer Science'
    })
    assert response.status_code == 200

def test_search_user(client):
    # Test searching for a user in the database
    response = client.post('/search', data={
        'profession': 'Software Engineer'
    })
    assert response.status_code == 200
    assert b'John' in response.data
    assert b'Doe' in response.data
    assert b'johndoe@example.com' in response.data
    assert b'Software Engineer' in response.data
    assert b'I am a software engineer.' in response.data
    assert b'Bachelor of Science in Computer Science' in response.data
