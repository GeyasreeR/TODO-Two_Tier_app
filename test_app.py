import pytest
import os
from app import app  # Replace with your app import path if different


# Fixture to set up a test client and temporary database
@pytest.fixture
def client(tmp_path):
    # Use a temporary database file for testing
    db_path = tmp_path / "test_todos.db"
    app.config['DATABASE'] = str(db_path)  # Adjust if your app uses a different config key
    app.config['TESTING'] = True


    # Create the database (assumes app has an init_db function or similar)
    with app.app_context():
        # If your app has an init_db function, call it here
        # Example: init_db()
        # For now, assuming table creation is handled in app.py on first run
        pass


    # Yield a test client
    with app.test_client() as client:
        yield client


    # Cleanup: Remove the temp db after tests
    if os.path.exists(db_path):
        os.remove(db_path)


# Test adding a to-do
def test_add_todo(client):
    response = client.post('/add', data={'todo': 'Buy milk'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Buy milk' in response.data  # Check if "Buy milk" appears in HTML


# Test viewing to-dos
def test_view_todos(client):
    # Add a to-do first
    client.post('/add', data={'todo': 'Call mom'}, follow_redirects=True)
    response = client.get('/')
    assert response.status_code == 200
    assert b'Call mom' in response.data


# Test completing a to-do
def test_complete_todo(client):
    # Add a to-do
    client.post('/add', data={'todo': 'Write code'}, follow_redirects=True)
    # Assume first to-do has ID 1 (adjust if your app uses different IDs)
    response = client.post('/complete', data={'id': '1'}, follow_redirects=True)
    assert response.status_code == 200
    # Check for completion marker (e.g., CSS class or text)
    assert b'completed' in response.data or b'strikethrough' in response.data  # Adjust based on your UI


# Test deleting a to-do
def test_delete_todo(client):
    # Add a to-do
    client.post('/add', data={'todo': 'Test app'}, follow_redirects=True)
    # Delete it
    response = client.post('/delete', data={'id': '1'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Test app' not in response.data  # To-do should be gone


# Test empty input handling
def test_empty_todo(client):
    response = client.post('/add', data={'todo': ''}, follow_redirects=True)
    assert response.status_code == 200
    # Check no new to-do added (adjust if your app flashes an error)
    assert len(client.get('/').data.split(b'<li>')) == 1  # No list items


# Test multiple to-dos
def test_multiple_todos(client):
    client.post('/add', data={'todo': 'Task 1'}, follow_redirects=True)
    client.post('/add', data={'todo': 'Task 2'}, follow_redirects=True)
    response = client.get('/')
    assert response.status_code == 200
    assert b'Task 1' in response.data
    assert b'Task 2' in response.data

