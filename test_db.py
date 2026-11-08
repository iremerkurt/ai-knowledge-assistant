
from sqlalchemy import inspect

from app.db.database import engine, Base
from app.db.models import Document, DocumentChunk


# Python modellerinden PostgreSQL tablolarını oluştur
Base.metadata.create_all(bind=engine)

# Oluşturulan tabloları kontrol et
inspector = inspect(engine)

tables = inspector.get_table_names()

print("Database tables:")

for table in tables:
    print("-", table)
