"""Infrastructure ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class Infrastructure(Base):
    __tablename__ = "infrastructures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
