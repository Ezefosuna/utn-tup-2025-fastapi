"""Application configuration settings.

This module contains configuration constants and settings for the FastAPI application.
Configuration can be overridden via environment variables.
"""
import os
from typing import Optional

# Application Settings
APP_NAME = "Car Sales Management API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "RESTful API for managing vehicle inventory and sales transactions"

# Database Settings
DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "sqlite:///./car_sales.db"  # Default to SQLite for development
)

# Debug Mode
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

# Server Settings
PORT: int = int(os.getenv("PORT", 8000))
HOST: str = os.getenv("HOST", "0.0.0.0")

# CORS Settings
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

# API Settings
API_PREFIX = ""
API_TITLE = APP_NAME
API_DOCS_URL = "/docs"
API_REDOC_URL = "/redoc"
