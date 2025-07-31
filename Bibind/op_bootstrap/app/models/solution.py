"""Solution ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class Solution(Base):
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
