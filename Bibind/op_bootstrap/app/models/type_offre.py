"""TypeOffre ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class TypeOffre(Base):
    __tablename__ = "types_offre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
