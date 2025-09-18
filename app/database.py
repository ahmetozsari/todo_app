from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite veritabanı bağlantısı
DATABASE_URL = "sqlite:///todo.db"

# Engine ve session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class
Base = declarative_base()


def init_db():
    """Tüm tabloları oluşturur"""
    # Import döngüsünü önlemek için fonksiyon içinde import
    from app import models
    Base.metadata.create_all(bind=engine)
