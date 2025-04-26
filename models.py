"""
Database models for the Litestar and SQLAlchemy application.

This module defines SQLAlchemy ORM models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float

from database import Base

class Book(Base):
    """
    Book model representing a book in a library or bookstore.
    
    Demonstrates basic SQLAlchemy model definition with various field types.
    """
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    published_year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the book."""
        return f"<Book {self.title} by {self.author}>"
        
    def to_dict(self):
        """Convert the model instance to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "price": self.price,
            "published_year": self.published_year,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }