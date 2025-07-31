"""ORM model placeholder."""

from .base import Base
from sqlalchemy import Column, Integer

class Model(Base):
    __tablename__ = "placeholder"
    id = Column(Integer, primary_key=True)
