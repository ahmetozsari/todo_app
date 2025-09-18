
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import api
from app.database import init_db
from app.models import User, Task
from flask import Flask

@pytest.fixture
def client():
	api.app.config['TESTING'] = True
	with api.app.test_client() as client:
		with api.app.app_context():
			init_db()
		yield client

def test_register(client):
	response = client.post('/api/register', json={
		'username': 'testuser',
		'password': 'testpass'
	})
	assert response.status_code == 201
	assert 'Kayıt başarılı' in response.get_json()['message']

def test_login(client):
	# Register first
	client.post('/api/register', json={
		'username': 'testuser2',
		'password': 'testpass2'
	})
	# Login
	response = client.post('/api/login', json={
		'username': 'testuser2',
		'password': 'testpass2'
	})
	assert response.status_code == 200
	assert 'token' in response.get_json()

def test_protected_tasks(client):
	# Register and login
	client.post('/api/register', json={
		'username': 'testuser3',
		'password': 'testpass3'
	})
	login_resp = client.post('/api/login', json={
		'username': 'testuser3',
		'password': 'testpass3'
	})
	token = login_resp.get_json()['token']
	# Access protected endpoint
	headers = {'Authorization': f'Bearer {token}'}
	response = client.get('/api/tasks', headers=headers)
	assert response.status_code == 200
	# Access without token
	response_no_token = client.get('/api/tasks')
	assert response_no_token.status_code == 401
