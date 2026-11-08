
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


# .env dosyasındaki bilgileri yükle
load_dotenv()

# Veritabanı bağlantı bilgileri
database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port=int(os.getenv("POSTGRES_PORT", "5432")),
    database=os.getenv("POSTGRES_DB")
)

# PostgreSQL bağlantısı
engine = create_engine(
    database_url,
    pool_pre_ping=True
)

# Veritabanı oturumları
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Veritabanı modellerinin temel sınıfı
Base = declarative_base()


# API isteklerinde veritabanı oturumu oluştur
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
