"""Projet ORM model."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Projet(Base):
    __tablename__ = "projets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    organisation_id = Column(Integer, ForeignKey("organisations.id"))

    organisation = relationship("Organisation", back_populates="projets")
    offres = relationship("Offre", back_populates="projet")
