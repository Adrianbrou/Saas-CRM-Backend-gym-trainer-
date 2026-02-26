from app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, func, String, Integer, ForeignKey


class Workout(Base):

    __tablename__ = "workout"

    # create the table rows

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True, unique=True)

    # foreign key
    body_part_id = Column(Integer,
                          ForeignKey("body_part.id", ondelete="CASCADE"),

                          nullable=False)
    # timestampss
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    body_part = relationship("BodyPart", back_populates="workouts")
    progress_logs = relationship(
        "Progress", back_populates="workout", cascade="all, delete")


class BodyPart(Base):
    __tablename__ = "body_part"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # "the field on Workout is called body_part"
    workouts = relationship("Workout", back_populates="body_part")
    # Progress(child) Workout(parent):
