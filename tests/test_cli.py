import pytest
from todo_app.app.models import Task
from todo_app.app.database import SessionLocal

# Test veritabanı oturumu
db = SessionLocal()

# Görev ekleme testi
def test_add_task():
    task = Task(title="Test Görev", description="Test", completed=False)
    db.add(task)
    db.commit()
    t = db.query(Task).filter_by(title="Test Görev").first()
    assert t is not None
    db.delete(t)
    db.commit()
