"""
Database configuration for the Litestar and SQLAlchemy application.

This module sets up the SQLAlchemy engine, session, and base model.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# SQLite database URL - using SQLite for simplicity
# In a production environment, you would use a more robust database
DATABASE_URL = "sqlite:///./app.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a scoped session for thread safety
db_session = scoped_session(SessionLocal)

# Create a base class for declarative models
Base = declarative_base()

# Dependency function to get a database session
def get_db_session():
    """
    Get a database session for dependency injection.
    
    This function creates a new database session and closes it after use.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def init_db():
    """
    Initialize the database by creating all tables.
    
    This function should be called when the application starts.
    """
    # Import models here to avoid circular imports
    import models  # noqa
    
    # Create all tables
    Base.metadata.create_all(bind=engine)