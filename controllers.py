"""
Controllers for the Litestar application.

This module defines controller classes that handle HTTP requests and responses.
"""
from typing import List, Optional

from litestar import Controller, get, post, put, delete, Router
from litestar.di import Provide
from litestar.params import Parameter, Body
from litestar.exceptions import NotFoundException
from sqlalchemy.orm import Session
from litestar.status_codes import HTTP_200_OK

from database import get_db_session
from models import Book


class BookController(Controller):
    """
    Controller for book-related routes.
    
    Demonstrates Litestar's class-based routing with dependency injection.
    """
    path = "/books"
    dependencies = {"db_session": Provide(get_db_session)}
    
    @get("/")
    async def get_books(self, db_session: Session) -> List[dict]:
        """
        Get all books from the database.
        
        Returns:
            A list of books as dictionaries.
        """
        books = db_session.query(Book).all()
        return [book.to_dict() for book in books]
    
    @get("/{book_id:int}")
    async def get_book(
        self, 
        db_session: Session, 
        book_id: int = Parameter(description="The ID of the book to retrieve")
    ) -> dict:
        """
        Get a book by ID.
        
        Args:
            book_id: The ID of the book to retrieve.
            db_session: SQLAlchemy database session.
            
        Returns:
            The book as a dictionary.
            
        Raises:
            NotFoundException: If the book is not found.
        """
        book = db_session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise NotFoundException(f"Book with ID {book_id} not found")
        return book.to_dict()
    
    @post("/")
    async def create_book(
        self, 
        db_session: Session, 
        data: dict = Body(description="Book data to create")
    ) -> dict:
        """
        Create a new book.
        
        Args:
            data: Book data from request body.
            db_session: SQLAlchemy database session.
            
        Returns:
            The created book as a dictionary.
        """
        # Create a new book from the request data
        book = Book(
            title=data["title"],
            author=data["author"],
            description=data.get("description"),
            price=data.get("price"),
            published_year=data.get("published_year")
        )
        
        # Add and commit to the database
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        return book.to_dict()
    
    @put("/{book_id:int}")
    async def update_book(
        self, 
        db_session: Session, 
        data: dict = Body(description="Book data to update"),
        book_id: int = Parameter(description="The ID of the book to update")
    ) -> dict:
        """
        Update an existing book.
        
        Args:
            book_id: The ID of the book to update.
            data: Updated book data.
            db_session: SQLAlchemy database session.
            
        Returns:
            The updated book as a dictionary.
            
        Raises:
            NotFoundException: If the book is not found.
        """
        # Find the book to update
        book = db_session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise NotFoundException(f"Book with ID {book_id} not found")
        
        # Update the book attributes
        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        if "description" in data:
            book.description = data["description"]
        if "price" in data:
            book.price = data["price"]
        if "published_year" in data:
            book.published_year = data["published_year"]
        
        # Commit the changes
        db_session.commit()
        db_session.refresh(book)
        
        return book.to_dict()
    
    @delete("/{book_id:int}", status_code=HTTP_200_OK)
    async def delete_book(
        self, 
        db_session: Session, 
        book_id: int = Parameter(description="The ID of the book to delete")
    ) -> dict:
        """
        Delete a book.
        
        Args:
            book_id: The ID of the book to delete.
            db_session: SQLAlchemy database session.
            
        Returns:
            A message confirming deletion.
            
        Raises:
            NotFoundException: If the book is not found.
        """
        # Find the book to delete
        book = db_session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise NotFoundException(f"Book with ID {book_id} not found")
        
        # Delete the book
        db_session.delete(book)
        db_session.commit()
        
        return {"message": f"Book with ID {book_id} deleted successfully"}