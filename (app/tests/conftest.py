import pytest
from app import create_app, db
from app.models import User, Report

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_headers(client):
    # Create test user and get auth token
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    client.post('/api/auth/register', json=user_data)
    
    login_response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass123'
    })
    
    token = login_response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}
