from app.database.base import Base
from sqlalchemy import Column, Integer, DateTime, func, String
from sqlalchemy.orm import relationship


class Gym(Base):
    """_summary_ : create the gym class for the tables 
    """
    __tablename__ = "gyms"
    # primary key
    id = Column(Integer, primary_key=True, index=True)

    # Basic information
    name = Column(String, nullable=False, unique=True, index=True)
    location = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships

    """
        parent tables: need cascade on it
    """
    members = relationship(
        "Member", back_populates="gym", cascade="all, delete")
    staff = relationship(
        "Staff", back_populates="gym", cascade="all, delete")
    sessions = relationship(
        "WorkoutSession",   back_populates="gym", cascade="all, delete")
