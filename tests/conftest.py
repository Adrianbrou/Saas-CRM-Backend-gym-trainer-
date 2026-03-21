from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
import pytest

# create the test database url
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# create the engine to connect to the db test
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False})
# create the session that use the engine connection
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
