from todo_app.app.database import SessionLocal, Base, engine
from todo_app.app.models import User, Task
from utils import format_task, parse_date
from rich import print        # CLI çıktısını renkli göstermek için
from getpass import getpass   # Şifre girişini gizlemek için

# Veritabanındaki tabloları oluştur
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Giriş yapan kullanıcı (global)
current_user = None

# Kullanıcı kayıt fonksiyonu
def register():
    username = input("Kullanıcı adı: ")
    password = getpass("Şifre: ")
    if db.query(User).filter_by(username=username).first():
        print("[red]Bu kullanıcı zaten var![/red]")
        return
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    print("[green]Kayıt başarılı![/green]")

# Kullanıcı giriş fonksiyonu
def login():
    global current_user
    username = input("Kullanıcı adı: ")
    password = getpass("Şifre: ")
    user = db.query(User).filter_by(username=username, password=password).first()
    if user:
        current_user = user
        print(f"[green]Hoşgeldin, {user.username}![/green]")
    else:
        print("[red]Kullanıcı bulunamadı veya şifre yanlış[/red]")

# Görev ekleme
def add_task():
    title = input("Görev başlığı: ")
    desc = input("Açıklama (opsiyonel): ")
    priority = input("Öncelik (low/medium/high): ").lower() or "medium"
    due_str = input("Son tarih (YYYY-MM-DD, opsiyonel): ")
    due_date = parse_date(due_str)
    task = Task(title=title, description=desc, priority=priority, due_date=due_date, owner=current_user)
    db.add(task)
    db.commit()
    print("[green]Görev eklendi![/green]")

# Görevleri listeleme
def list_tasks():
    tasks = db.query(Task).filter(Task.owner == current_user).all()
    if not tasks:
        print("[yellow]Görev yok![/yellow]")
    for t in tasks:
        print(format_task(t))

# Görevi tamamla
def complete_task():
    task_id = int(input("Tamamlanacak görev ID: "))
    task = db.query(Task).filter(Task.id==task_id, Task.owner==current_user).first()
    if task:
        task.completed = True
        db.commit()
        print("[green]Görev tamamlandı[/green]")
    else:
        print("[red]Görev bulunamadı[/red]")

# Ana menü
def menu():
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
                print("[red]Önce giriş yapmalısın[/red]")
        elif choice == "4":
            if current_user:
                list_tasks()
            else:
                print("[red]Önce giriş yapmalısın[/red]")
        elif choice == "5":
            if current_user:
                complete_task()
            else:
                print("[red]Önce giriş yapmalısın[/red]")
        elif choice == "0":
            break
        else:
            print("[red]Geçersiz seçenek![/red]")

if __name__ == "__main__":
    menu()
