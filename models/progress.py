from app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, func, DateTime, Integer, Float


class Progress(Base):
    """_summary_: crate the class progress for table progress that will hold the progress
      of the client's workout 

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer,
                       ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    workout_id = Column(Integer, ForeignKey(
        "workout.id", ondelete="CASCADE"), nullable=False)
    workout_session_id = Column(Integer, ForeignKey(
        "workout_session.id", ondelete="CASCADE"), nullable=False)

    weight_kg = Column(Float, nullable=True)
    sets = Column(Integer)
    reps = Column(Integer)

    # Timestamp

    logged_at = Column(DateTime(timezone=True), server_default=func.now())

    """
    Relationship:
        child table no need of cascade in relationhsip
        these relationship are also related to its Foreign key : member_id , workout_id,workout_session_id
    """
    # In Progress class
    member = relationship("Member",         back_populates="progress_logs")
    workout = relationship("Workout",        back_populates="progress_logs")
    session = relationship("WorkoutSession", back_populates="progress_logs")
