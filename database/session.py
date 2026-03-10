from sqlalchemy.orm import sessionmaker
from .engine import engine

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


def get_db():
    """FastAPI dependency that provides a database session per request.

    Opens a new SQLAlchemy session, yields it to the route handler,
    then closes it when the request finishes — whether it succeeded or raised.

    Usage:
        @router.get("/example")
        def example(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
