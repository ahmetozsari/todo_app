# app/api.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import SessionLocal, init_db
from app.models import User, Task
from app.utils import parse_date

# Flask uygulaması
app = Flask(__name__)
SECRET_KEY = "your_secret_key_here"  # Change this to a secure value

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'error': 'Token gerekli'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = db.query(User).filter_by(username=data['username']).first()
        except Exception:
            return jsonify({'error': 'Geçersiz veya süresi dolmuş token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

# Veritabanı tablolarını oluştur
init_db()
db = SessionLocal()

@app.route("/api/register", methods=["POST"])
def register():
    """Kullanıcı kaydı"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Kullanıcı adı ve şifre gerekli"}), 400
    if db.query(User).filter_by(username=username).first():
        return jsonify({"error": "Kullanıcı adı zaten mevcut"}), 409
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    db.add(user)
    db.commit()
    return jsonify({"message": "Kayıt başarılı"}), 201

@app.route("/api/login", methods=["POST"])
def login():
    """Kullanıcı girişi"""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = db.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Geçersiz kullanıcı adı veya şifre"}), 401
    token = jwt.encode({
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")
    return jsonify({"message": "Giriş başarılı", "token": token}), 200

@app.route("/api/tasks", methods=["GET"])
@token_required
def get_tasks(current_user):
    """Tüm görevleri listele (JWT ile)"""
    tasks = db.query(Task).filter(Task.owner==current_user).all()
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
@token_required
def add_task_api(current_user):
    """Yeni görev ekle (JWT ile)"""
    data = request.get_json()
    due_date = parse_date(data.get("due_date")) if data.get("due_date") else None
    task = Task(
        title=data.get("title"),
        description=data.get("description", ""),
        priority=data.get("priority", "medium"),
        due_date=due_date,
        owner=current_user
    )
    db.add(task)
    db.commit()
    return jsonify({"message": "Görev oluşturuldu"}), 201

if __name__ == "__main__":
    app.run(debug=True)
