import pytest
import os
from app import app


# Fixture to set up a test client and temporary database
@pytest.fixture(scope="function")
def client(tmp_path):
    # Use a temporary database file for testing
    db_path = tmp_path / "test_todos.db"
    app.config['DATABASE'] = str(db_path)
    app.config['TESTING'] = True

    # Create the database
    with app.app_context():
        from app import init_db
        init_db()

    # Yield a test client
    with app.test_client() as client:
        yield client

    # Cleanup: Remove the temp db after tests
    if os.path.exists(db_path):
        os.remove(db_path)


# Test adding a to-do
def test_add_todo(client):
    response = client.post('/', data={'task': 'Buy milk'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Buy milk' in response.data


# Test viewing to-dos
def test_view_todos(client):
    client.post('/', data={'task': 'Call mom'}, follow_redirects=True)
    response = client.get('/')
    assert response.status_code == 200
    assert b'Call mom' in response.data


# Test completing a to-do (uses PUT /todos/<id>)
def test_complete_todo(client):
    client.post('/', data={'task': 'Write code'}, follow_redirects=True)
    response = client.put('/todos/1', json={'completed': True})
    assert response.status_code == 200
    assert b'Updated' in response.data
    # Verify completion
    todos = client.get('/todos').json
    assert todos[0]['completed'] is True


# Test getting todos via API
def test_get_todos(client):
    client.post('/', data={'task': 'Test app'}, follow_redirects=True)
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.json[0]['task'] == 'Test app'


# Test empty input handling
def test_empty_todo(client):
    response = client.post('/', data={'task': ''}, follow_redirects=True)
    assert response.status_code == 200
    assert len(client.get('/').data.split(b'<li>')) == 1  # No list items


# Test multiple to-dos
def test_multiple_todos(client):
    client.post('/', data={'task': 'Task 1'}, follow_redirects=True)
    client.post('/', data={'task': 'Task 2'}, follow_redirects=True)
    response = client.get('/')
    assert response.status_code == 200
    assert b'Task 1' in response.data
    assert b'Task 2' in response.data
