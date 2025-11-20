"""Database configuration and session management.

This module handles database connection setup, session creation,
and table initialization for the application.
"""
import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please configure your .env file with DATABASE_URL."
    )

# Create database engine with appropriate configuration
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)


def get_session():
    """Get a new database session.
    
    Yields:
        Session: Active database session for query execution.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create all database tables based on SQLModel definitions.
    
    This function initializes the database schema on application startup
    and is called automatically during the application lifespan.
    """
    SQLModel.metadata.create_all(engine)