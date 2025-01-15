# Modèles SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    actions = relationship("Log", back_populates="user")


class Cloud(Base):
    __tablename__ = "clouds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False)


class TerraformAction(Base):
    __tablename__ = "terraform_actions"
    id = Column(Integer, primary_key=True, index=True)
    cloud_id = Column(Integer, ForeignKey("clouds.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    parameters = Column(Text)
    status = Column(String, default="pending")