"""Groupe ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class Groupe(Base):
    __tablename__ = "groupes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
