"""TypeInfrastructure ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class TypeInfrastructure(Base):
    __tablename__ = "types_infrastructure"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
