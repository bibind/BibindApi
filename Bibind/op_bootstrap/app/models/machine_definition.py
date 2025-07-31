"""MachineDefinition ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class MachineDefinition(Base):
    __tablename__ = "machine_definitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
