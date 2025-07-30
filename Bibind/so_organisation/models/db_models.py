"""Optional SQLAlchemy ORM models."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Example model
# class Example(Base):
#     __tablename__ = "example"
#     id = Column(Integer, primary_key=True)
