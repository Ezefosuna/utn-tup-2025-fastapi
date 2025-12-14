from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from database import create_db_and_tables
from autos import router as autos_router
from ventas import router as ventas_router
from auth_router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

app = FastAPI(
    title="FastAPI Auto Ventas API", 
    description="API para la gestión de ventas de autos.", 
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(autos_router)
app.include_router(ventas_router)
app.include_router(auth_router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
