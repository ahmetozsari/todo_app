from app.models import Task, User
from datetime import datetime

def test_sample():
    assert 1 + 1 == 2

def test_task_creation():
    user = User(username="test", password="123")
    task = Task(title="Deneme", description="Test", owner=user)
    assert task.title == "Deneme"
    assert task.completed is False
    assert task.owner.username == "test"
