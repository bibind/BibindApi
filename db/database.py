from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# URL pour la base de données PostgreSQL
DATABASE_URL = "postgresql://admin:password@localhost:5432/bindingapi"

# Configuration SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Gestion des sessions de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()