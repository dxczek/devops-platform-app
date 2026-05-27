"""
Database configuration and connection setup.
Uses SQLAlchemy for ORM and PostgreSQL as the database.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://postgres:postgres@localhost:5432/tasks_db"
    )

    class Config:
        env_file = ".env"


settings = Settings()

# Create database engine
engine = create_engine(settings.database_url, pool_pre_ping=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Dependency function that provides database session.
    Used by FastAPI for dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
