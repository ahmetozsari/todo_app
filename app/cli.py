# app/cli.py
from app.database import SessionLocal, init_db
from app.models import User, Task
from app.utils import format_task, parse_date
from getpass import getpass
from rich import print

# Veritabanı tablolarını oluştur
init_db()

# Veritabanı oturumu
db = SessionLocal()

# Global kullanıcı değişkeni
current_user = None

def register():
    """Yeni kullanıcı kaydı"""
    username = input("Kullanıcı adı: ")
    password = getpass("Şifre: ")
    if db.query(User).filter_by(username=username).first():
        print("[red]Bu kullanıcı zaten var![/red]")
        return
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    print("[green]Kayıt başarılı![/green]")

def login():
    """Kullanıcı girişi"""
    global current_user
    username = input("Kullanıcı adı: ")
    password = getpass("Şifre: ")
    user = db.query(User).filter_by(username=username, password=password).first()
    if user:
        current_user = user
        print(f"[green]Hoşgeldin, {user.username}![/green]")
    else:
        print("[red]Kullanıcı bulunamadı veya şifre yanlış[/red]")

def add_task():
    """Görev ekleme"""
    title = input("Görev başlığı: ")
    description = input("Açıklama (opsiyonel): ")
    priority = input("Öncelik (low/medium/high, default medium): ").lower() or "medium"
    due_input = input("Son tarih (YYYY-MM-DD, opsiyonel): ")
    due_date = parse_date(due_input)
    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        owner=current_user
    )
    db.add(task)
    db.commit()
    print("[green]Görev eklendi![/green]")

def list_tasks():
    """Kullanıcının görevlerini listele"""
    tasks = db.query(Task).filter(Task.owner==current_user).all()
    if not tasks:
        print("[yellow]Hiç görev yok![/yellow]")
        return
    for task in tasks:
        print(format_task(task))

def complete_task():
    """Görevi tamamlandı olarak işaretle"""
    task_id = input("Tamamlanacak görev ID: ")
    task = db.query(Task).filter(Task.id==task_id, Task.owner==current_user).first()
    if task:
        task.completed = True
        db.commit()
        print("[green]Görev tamamlandı![/green]")
    else:
        print("[red]Görev bulunamadı![/red]")

def menu():
    """Ana menü"""
    while True:
        print("\n[bold cyan]=== To-Do CLI ===[/bold cyan]")
        print("1. Kayıt ol")
        print("2. Giriş yap")
        print("3. Görev ekle")
        print("4. Görevleri listele")
        print("5. Görev tamamla")
        print("0. Çıkış")
        choice = input("Seçiminiz: ")
        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            if current_user:
                add_task()
            else:
                print("[red]Önce giriş yapmalısın![/red]")
        elif choice == "4":
            if current_user:
                list_tasks()
            else:
                print("[red]Önce giriş yapmalısın![/red]")
        elif choice == "5":
            if current_user:
                complete_task()
            else:
                print("[red]Önce giriş yapmalısın![/red]")
        elif choice == "0":
            break
        else:
            print("[red]Geçersiz seçenek![/red]")

if __name__ == "__main__":
    menu()
