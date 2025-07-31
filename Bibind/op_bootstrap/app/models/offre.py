"""Offre ORM model."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Offre(Base):
    __tablename__ = "offres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    projet_id = Column(Integer, ForeignKey("projets.id"))

    projet = relationship("Projet", back_populates="offres")
