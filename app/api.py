# app/api.py
from flask import Flask, request, jsonify
from app.database import SessionLocal, init_db
from app.models import User, Task
from app.utils import parse_date

# Flask uygulaması
app = Flask(__name__)

# Veritabanı tablolarını oluştur
init_db()
db = SessionLocal()

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Tüm görevleri listele (username ile)"""
    username = request.args.get("user")
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Kullanıcı bulunamadı"}), 404
    tasks = db.query(Task).filter(Task.owner==user).all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed,
            "priority": t.priority,
            "due_date": t.due_date.strftime("%Y-%m-%d") if t.due_date else None
        }
        for t in tasks
    ])

@app.route("/api/tasks", methods=["POST"])
def add_task_api():
    """Yeni görev ekle"""
    data = request.get_json()
    user = db.query(User).filter_by(username=data.get("user")).first()
    if not user:
        return jsonify({"error": "Kullanıcı bulunamadı"}), 404
    due_date = parse_date(data.get("due_date")) if data.get("due_date") else None
    task = Task(
        title=data.get("title"),
        description=data.get("description", ""),
        priority=data.get("priority", "medium"),
        due_date=due_date,
        owner=user
    )
    db.add(task)
    db.commit()
    return jsonify({"message": "Görev oluşturuldu"}), 201

if __name__ == "__main__":
    app.run(debug=True)
