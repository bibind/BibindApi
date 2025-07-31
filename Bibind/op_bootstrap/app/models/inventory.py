"""Inventory ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
