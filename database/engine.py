
from sqlalchemy import create_engine
import os
from pathlib import Path
from dotenv import load_dotenv

# load the environement
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# get the database url from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")

# create the engine
engine = create_engine(DATABASE_URL,
                       echo=True,
                       pool_pre_ping=True,
                       )
