"""ModuleInfrastructure ORM model."""

from sqlalchemy import Column, Integer, String

from .base import Base


class ModuleInfrastructure(Base):
    __tablename__ = "modules_infrastructure"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
