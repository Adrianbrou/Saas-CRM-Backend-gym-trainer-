from app.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, func, String, Integer, ForeignKey


class WorkoutSession(Base):
    __tablename__ = "workout_session"

    id = Column(Integer, primary_key=True, nullable=False, index=True)

    gym_id = Column(Integer,
                    ForeignKey("gyms.id", ondelete="CASCADE"),
                    nullable=False
                    )
    staff_id = Column(Integer,
                      ForeignKey("staff.id", ondelete="CASCADE"),
                      nullable=False
                      )
    # timestamp
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationship

    gym = relationship("Gym",   back_populates="sessions")
    staff = relationship("Staff", back_populates="sessions")

    # Progress(Child) WorkoutSession(Parents):
    progress_logs = relationship(
        "Progress", back_populates="session", cascade="all, delete")

    """_summary_:creation of 2 links tables (or look-up tables)
       _Description: link tables do not need relationship just fK + PK
       look-up tables does not need timestamp snce they are not entity
    """


class Attendance(Base):
    __tablename__ = "attendance"

    workout_session_id = Column(Integer,
                                ForeignKey("workout_session.id",
                                           ondelete="CASCADE"),
                                nullable=False, primary_key=True)
    member_id = Column(Integer,
                       ForeignKey("members.id", ondelete="CASCADE"),
                       nullable=False, primary_key=True
                       )


class SessionWorkouts(Base):
    """_summary_: create a link table to link the workout_session and the workout  

    Args:
        Base (_type_): _description_
    """
    __tablename__ = "session_workouts"

    workout_session_id = Column(Integer,
                                ForeignKey("workout_session.id",
                                           ondelete="CASCADE"),
                                nullable=False, primary_key=True)
    workout_id = Column(Integer,
                        ForeignKey("workout.id",
                                   ondelete="CASCADE"),
                        nullable=False, primary_key=True)
