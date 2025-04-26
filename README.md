# Litestar + SQLAlchemy Sample Application

This documentation provides a comprehensive guide to the Litestar + SQLAlchemy sample application, including its architecture, components, and how to use it.

**Date**: April 26, 2025  
**Version**: 1.0.0

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Core Components](#core-components)
    - [Application Configuration](#application-configuration)
    - [Database Configuration](#database-configuration)
    - [Models](#models)
    - [Controllers](#controllers)
5. [API Reference](#api-reference)
6. [Key Concepts](#key-concepts)
    - [Litestar Concepts](#litestar-concepts)
    - [SQLAlchemy Concepts](#sqlalchemy-concepts)
7. [Examples](#examples)
8. [Extending the Application](#extending-the-application)
9. [Troubleshooting](#troubleshooting)

## Overview

This sample application demonstrates the integration of Litestar (a modern, high-performance ASGI web framework) with SQLAlchemy (a powerful SQL toolkit and Object-Relational Mapping library). The application implements a simple Book API with CRUD operations, showcasing best practices for building web applications with these technologies.

The application serves as an educational tool to understand the fundamentals of:
- Litestar's routing, dependency injection, and request/response handling
- SQLAlchemy's ORM (Object-Relational Mapping) for database interactions
- REST API design and implementation
- Modern Python async web development

## Project Structure

```
/
├── app.py              # Main application entry point
├── app.db              # SQLite database file
├── controllers.py      # API route handlers and controllers
├── database.py         # Database configuration and setup
├── models.py           # SQLAlchemy ORM models
├── requirements.txt    # Project dependencies
└── README.md           # Basic project information
```

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. Clone the repository or download the source code
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

The server will start on `http://0.0.0.0:8000` with hot reload enabled.

## Core Components

### Application Configuration

The `app.py` file serves as the entry point for the application and contains:

- Application initialization
- Route registration
- OpenAPI documentation setup
- CORS configuration
- Server startup configuration

Key configuration elements:

```python
# OpenAPI configuration for API documentation
openapi_config = OpenAPIConfig(
    title="Book API",
    description="A simple Book API using Litestar and SQLAlchemy",
    version="1.0.0"
)

# Main application instance
app = Litestar(
    route_handlers=[hello_world, BookController],
    cors_config=cors_config,
    debug=True,
    openapi_config=openapi_config
)
```

### Database Configuration

The `database.py` file handles SQLAlchemy setup:

- Engine configuration with SQLite (for simplicity)
- Session management
- Base model class definition
- Helper functions for dependency injection and initialization

Key elements:

```python
# Database connection URL
DATABASE_URL = "sqlite:///./app.db"

# Engine configuration
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

# Session dependency
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
```

### Models

The `models.py` file defines the SQLAlchemy ORM models that represent database tables:

- The `Book` class with various column types
- Helper methods for data conversion
- String representation

```python
class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    published_year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Helper methods
    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"
        
    def to_dict(self):
        # Converts model to dictionary representation
        # ...
```

### Controllers

The `controllers.py` file contains the route handlers that process HTTP requests:

- The `BookController` class with CRUD operations
- Path definitions
- Request parameter validation
- Database interactions
- Error handling

Example controller method:

```python
@post("/")
async def create_book(
    self, 
    db_session: Session, 
    data: dict = Body(description="Book data to create")
) -> dict:
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
```

## API Reference

The application provides the following endpoints:

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|-------------|----------|
| GET | / | Welcome message | None | `{"message": "Welcome...", "endpoints": {...}}` |
| GET | /books | List all books | None | Array of book objects |
| GET | /books/{book_id} | Get book by ID | None | Book object or 404 error |
| POST | /books | Create a new book | Book data | Created book object |
| PUT | /books/{book_id} | Update a book | Updated fields | Updated book object |
| DELETE | /books/{book_id} | Delete a book | None | Success message |

### Request/Response Examples

#### Create a Book

Request:
```http
POST /books
Content-Type: application/json

{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "published_year": 1925,
  "description": "A novel about the American Dream",
  "price": 12.99
}
```

Response:
```json
{
  "id": 1,
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "published_year": 1925,
  "description": "A novel about the American Dream",
  "price": 12.99,
  "created_at": "2025-04-26T14:30:45.123456",
  "updated_at": "2025-04-26T14:30:45.123456"
}
```

## Key Concepts

### Litestar Concepts

1. **Route Handlers**: Functions and methods decorated with `@get`, `@post`, etc. to handle HTTP requests.
2. **Controllers**: Classes that group related route handlers under a common path.
3. **Dependency Injection**: Using Litestar's `Provide` to inject dependencies like database sessions.
4. **Parameter Validation**: Type checking and validation of request parameters.
5. **Exception Handling**: Built-in exceptions like `NotFoundException` for error responses.

### SQLAlchemy Concepts

1. **ORM Models**: Python classes that map to database tables.
2. **Session Management**: CRUD operations using database sessions.
3. **Query Building**: Constructing database queries using the ORM.
4. **Schema Definition**: Defining tables, columns, and constraints.
5. **Relationships**: (Not implemented in this sample, but SQLAlchemy supports complex model relationships).

## Examples

### Using curl to Interact with the API

1. **List all books**:
   ```bash
   curl http://localhost:8000/books/
   ```

2. **Get a specific book**:
   ```bash
   curl http://localhost:8000/books/1
   ```

3. **Create a new book**:
   ```bash
   curl -X POST http://localhost:8000/books/ \
     -H "Content-Type: application/json" \
     -d '{"title": "1984", "author": "George Orwell", "published_year": 1949}'
   ```

4. **Update a book**:
   ```bash
   curl -X PUT http://localhost:8000/books/1 \
     -H "Content-Type: application/json" \
     -d '{"price": 14.99}'
   ```

5. **Delete a book**:
   ```bash
   curl -X DELETE http://localhost:8000/books/1
   ```

## Extending the Application

This sample application can be extended in several ways:

1. **Authentication and Authorization**: Add user authentication using Litestar's auth features.
2. **Advanced Models**: Create relationships between models (e.g., Author, Category).
3. **Pagination**: Implement pagination for large collections.
4. **File Uploads**: Add support for uploading book covers.
5. **Database Migrations**: Implement migrations using Alembic.
6. **Testing**: Add unit and integration tests.

### Example: Adding Author Relationship

```python
# In models.py
class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    
    # Existing fields...
    
    author_id = Column(Integer, ForeignKey("authors.id"))
    author_relation = relationship("Author", back_populates="books")
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Check if the SQLite database file exists and has proper permissions.
   - Ensure the DATABASE_URL is correctly configured.

2. **Import Errors**:
   - Verify that all dependencies are installed.
   - Check for circular imports in the application.

3. **HTTP 500 Errors**:
   - Check the application logs for exceptions.
   - Verify that the database schema matches the models.

4. **Status Code Errors**:
   - Ensure that response bodies are compatible with the specified status codes.
   - For status codes 204, 304, or below 200, do not return a response body.

### Debugging Tips

1. Run the application in debug mode (`debug=True`) for detailed error messages.
2. Use Litestar's logging features to track request/response flow.
3. Inspect the database directly using an SQLite client like `sqlite3` command-line tool.
