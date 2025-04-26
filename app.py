"""
Main entry point for the Litestar and SQLAlchemy application.

This module sets up the Litestar application, defines routes,
and initializes the database connection.
"""
import uvicorn
from litestar import Litestar, get
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig

from database import init_db
from controllers import BookController


@get("/")
async def hello_world() -> dict:
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        A simple welcome message as a dictionary.
    """
    return {
        "message": "Welcome to the Litestar + SQLAlchemy Demo API",
        "endpoints": {
            "books": "/books"
        }
    }


# Configure CORS for the application
cors_config = CORSConfig(
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def create_app() -> Litestar:
    """
    Create and configure the Litestar application.
    
    This function creates a new Litestar application instance,
    registers routes, and sets up middleware.
    
    Returns:
        A configured Litestar application instance.
    """
    # Initialize the database
    init_db()
    
    # Configure OpenAPI documentation
    openapi_config = OpenAPIConfig(
        title="Book API",
        description="A simple Book API using Litestar and SQLAlchemy",
        version="1.0.0"
    )
    
    # Create the Litestar application
    app = Litestar(
        route_handlers=[hello_world, BookController],
        cors_config=cors_config,
        debug=True,
        openapi_config=openapi_config
    )
    
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    # Run the application using Uvicorn when script is executed directly
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )