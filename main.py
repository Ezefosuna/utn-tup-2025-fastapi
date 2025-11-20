"""FastAPI application for vehicle sales management system.

This module sets up the main FastAPI application with:
- Database initialization and table creation
- Router registration for all endpoints
- CORS middleware configuration for frontend communication
- Application lifecycle management
- Interactive API documentation (Swagger UI, ReDoc)

The application provides comprehensive REST APIs for managing:
- Vehicle (Auto) inventory
- Sales transactions
- User authentication
- Country and person management
- Generic object storage
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers_autos import router as autos_router
from app.routers_ventas import router as ventas_router
from config import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    DEBUG,
    CORS_ORIGINS,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events.
    
    Startup: Initialize database and create tables
    Shutdown: Cleanup resources (empty for now)
    """
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    debug=DEBUG,
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register application routers
app.include_router(autos_router)
app.include_router(ventas_router)


@app.get("/", tags=["health"])
def read_root():
    """Health check endpoint."""
    return {
        "status": "operational",
        "service": APP_NAME,
        "version": APP_VERSION,
    }