# app/cli.py
import requests
from app.utils import format_task, parse_date
from getpass import getpass
from rich import print
import os


# API URL
API_URL = "http://127.0.0.1:5000/api"

# Token storage
TOKEN_FILE = "token.txt"

def save_token(token):
    with open(TOKEN_FILE, "w") as f:
        f.write(token)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None

def register():
    """Yeni kullanıcı kaydı (API)"""
    username = input("Kullanıcı adı: ")
    password = getpass("Şifre: ")
    resp = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
    if resp.status_code == 201:
        print("[green]Kayıt başarılı![green]")
    else:
        print(f"[red]{resp.json().get('error', 'Kayıt başarısız')}[/red]")

def login():
    """Kullanıcı girişi (API)"""
    username = input("Kullanıcı adı: ")
    password = getpass("Şifre: ")
    resp = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
    if resp.status_code == 200:
        token = resp.json()["token"]
        save_token(token)
        print(f"[green]Hoşgeldin, {username}![green]")
    else:
        print(f"[red]{resp.json().get('error', 'Giriş başarısız')}[/red]")

def add_task():
    """Görev ekleme (API)"""
    token = load_token()
    if not token:
        print("[red]Önce giriş yapmalısın![red]")
        return
    title = input("Görev başlığı: ")
    description = input("Açıklama (opsiyonel): ")
    priority = input("Öncelik (low/medium/high, default medium): ").lower() or "medium"
    due_input = input("Son tarih (YYYY-MM-DD, opsiyonel): ")
    data = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_input if due_input else None
    }
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.post(f"{API_URL}/tasks", json=data, headers=headers)
    if resp.status_code == 201:
        print("[green]Görev eklendi![green]")
    else:
        print(f"[red]{resp.json().get('error', 'Görev eklenemedi')}[/red]")

def list_tasks():
    """Kullanıcının görevlerini listele (API)"""
    token = load_token()
    if not token:
        print("[red]Önce giriş yapmalısın![red]")
        return
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API_URL}/tasks", headers=headers)
    if resp.status_code == 200:
        tasks = resp.json()
        if not tasks:
            print("[yellow]Hiç görev yok![yellow]")
            return
        for task in tasks:
            print(format_task(task))
    else:
        print(f"[red]{resp.json().get('error', 'Görevler alınamadı')}[/red]")

def complete_task():
    """Görevi tamamlandı olarak işaretle (API)"""
    token = load_token()
    if not token:
        print("[red]Önce giriş yapmalısın![red]")
        return
    task_id = input("Tamamlanacak görev ID: ")
    headers = {"Authorization": f"Bearer {token}"}
    # Assuming PATCH endpoint exists for completion (not implemented yet)
    resp = requests.patch(f"{API_URL}/tasks/{task_id}", json={"completed": True}, headers=headers)
    if resp.status_code == 200:
        print("[green]Görev tamamlandı![green]")
    else:
        print(f"[red]{resp.json().get('error', 'Görev tamamlanamadı')}[/red]")

def menu():
    """Ana menü (API)"""
    while True:
        print("\n[bold cyan]=== To-Do CLI ===[bold cyan]")
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
            add_task()
        elif choice == "4":
            list_tasks()
        elif choice == "5":
            complete_task()
        elif choice == "0":
            break
        else:
            print("[red]Geçersiz seçenek![red]")

if __name__ == "__main__":
    menu()
