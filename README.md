# 📝 To-Do App (Python + SQLite + SQLAlchemy + CLI & API)

Bu proje, Python ve SQLAlchemy kullanarak geliştirilmiş **basit bir To-Do uygulamasıdır**. Hem **CLI (komut satırı)** üzerinden hem de **REST API** üzerinden görevlerinizi yönetebilirsiniz.  

---

## 🚀 Özellikler

- Kullanıcı kaydı ve giriş sistemi  
- Görev ekleme, listeleme ve tamamlama  
- Görevler için öncelik ve son tarih ekleme  
- CLI ve API üzerinden yönetim  
- SQLite veritabanı ile hafif ve taşınabilir  
- Kolay genişletilebilir yapı  

---

## 🛠 Teknolojiler

- Python 3.10+  
- SQLAlchemy ORM  
- SQLite  
- Flask (API için)  
- Rich (CLI renkli çıktı)  

---

## 📁 Proje Yapısı

```
todo_app/
│── app/
│   │── __init__.py
│   │── database.py
│   │── models.py
│   │── utils.py
│   │── cli.py
│   │── api.py
│── README.md
```

---

## ⚡ Kurulum

1. Depoyu klonlayın:

```bash
git clone <repository_url>
cd todo_app
```

2. Sanal ortam oluşturun ve aktif edin:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:

```bash
pip install sqlalchemy flask rich
```

4. Veritabanını oluşturun:

```python
from app.database import init_db
init_db()
```

> Not: Eğer `tasks` tablosu eskiden oluşturulduysa ve yeni kolonlar eklediyseniz, `todo.db` dosyasını silip tekrar oluşturun.

---

## 💻 CLI Kullanımı

CLI üzerinden uygulamayı çalıştırın:

```bash
python -m app.cli
```

### Örnek Menü İşlemleri

```
=== To-Do CLI ===
1. Kayıt ol
2. Giriş yap
3. Görev ekle
4. Görevleri listele
5. Görev tamamla
0. Çıkış
```

- Kullanıcı kaydı ve giriş  
- Görev ekleme ve listeleme  
- Görevleri tamamlandı olarak işaretleme  

### Örnek CLI Çıktısı

```
Kullanıcı adı: ahmet
Şifre: ****
Hoşgeldin, ahmet!

Görev ekle:
Başlık: Alışveriş
Açıklama: Marketten yiyecek al
Öncelik (low/medium/high, default medium): high
Son tarih (YYYY-MM-DD, opsiyonel): 2025-09-20
Görev eklendi!

Görevleri listele:
[❌] 1. Alışveriş | Öncelik: high | Tarih: 2025-09-20
```

---

## 🌐 API Kullanımı

API’yi çalıştır:

```bash
python -m app.api
```

### Endpointler

- `GET /api/tasks?user=<username>` → Görevleri listele  
- `POST /api/tasks` → Yeni görev ekle  

### Örnek GET

```
GET http://127.0.0.1:5000/api/tasks?user=ahmet
```

**Response:**

```json
[
  {
    "id": 1,
    "title": "Alışveriş",
    "description": "Marketten yiyecek al",
    "completed": false,
    "priority": "high",
    "due_date": "2025-09-20"
  }
]
```

### Örnek POST

```
POST http://127.0.0.1:5000/api/tasks
Content-Type: application/json
```

```json
{
  "user": "ahmet",
  "title": "API üzerinden görev",
  "description": "Test",
  "priority": "medium",
  "due_date": "2025-09-21"
}
```

**Response:**

```json
{
  "message": "Görev oluşturuldu"
}
```

---

## ⚡ Notlar

- SQLite kullandığı için tablo güncellemeleri için `todo.db` silinip yeniden oluşturulmalıdır.  
- CLI ve API aynı veritabanını kullanır.  
- `description` gibi yeni kolonlar eklediğinizde, eski veritabanı tablolarını güncellemek için dosyayı silmek en hızlı çözümdür.  

---

## 🎯 Geliştirme Fikirleri

- Görevleri tarih ve öncelik sırasına göre filtreleme  
- Kullanıcı rolleri (admin/user) ekleme  
- Daha gelişmiş web arayüzü (React/Vue)  
- Alembic ile migration sistemi ekleyerek tablo güncellemelerini otomatik yapmak

---

## 📦 Lisans

MIT License
