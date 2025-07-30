"""Optional SQLAlchemy ORM models for the release service."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Example model
# class Example(Base):
#     __tablename__ = "example"
#     id = Column(Integer, primary_key=True)
