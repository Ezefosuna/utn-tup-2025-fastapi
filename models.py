from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import BaseModel, conint
from datetime import datetime

# Auto models
class AutoBase(SQLModel):
    """Base model for Auto"""
    marca: str = Field(max_length=100, description="Marca del vehículo")
    modelo: str = Field(max_length=100, description="Modelo específico")
    año: conint(ge=1900, le=datetime.now().year) = Field(description="Año de fabricación")
    numero_chasis: str = Field(max_length=50, description="Número único de identificación del chasis", unique=True)

class Auto(AutoBase, table=True):
    """Auto table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship with ventas
    ventas: List["Venta"] = Relationship(back_populates="auto")

class AutoCreate(AutoBase):
    """Model for creating a new auto"""
    pass

class AutoUpdate(BaseModel):
    """Model for updating auto"""
    marca: Optional[str] = Field(None, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    año: Optional[conint(ge=1900, le=datetime.now().year)] = None
    numero_chasis: Optional[str] = Field(None, max_length=50)

class AutoResponse(AutoBase):
    """Model for auto response"""
    id: int

# Venta models
class VentaBase(SQLModel):
    """Base model for Venta"""
    fecha_venta: datetime = Field(default_factory=datetime.utcnow, description="Fecha de la venta")
    monto: float = Field(description="Monto de la venta")
    comprador_nombre: str = Field(max_length=200, description="Nombre del comprador")
    
    # Foreign key to Auto
    auto_id: Optional[int] = Field(default=None, foreign_key="auto.id")

class Venta(VentaBase, table=True):
    """Venta table model"""
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship with auto
    auto: Optional["Auto"] = Relationship(back_populates="ventas")

class VentaCreate(VentaBase):
    """Model for creating a new venta"""
    pass

class VentaUpdate(BaseModel):
    """Model for updating venta"""
    fecha_venta: Optional[datetime] = None
    monto: Optional[float] = None
    comprador_nombre: Optional[str] = None
    auto_id: Optional[int] = None

class VentaResponse(VentaBase):
    """Model for venta response"""
    id: int

# Now, define the models with relationships after all base models are defined.
class AutoResponseWithVentas(AutoResponse):
    """Model for auto response with ventas information"""
    ventas: List[VentaResponse] = []

class VentaResponseWithAuto(VentaResponse):
    """Model for venta response with auto information"""
    auto: Optional[AutoResponse] = None

# User/Auth models
class UserBase(SQLModel):
    """Base model for User"""
    username: str = Field(max_length=50, description="Username", unique=True)
    email: str = Field(max_length=100, description="Email address")
    is_active: bool = Field(default=True, description="User is active")

class User(UserBase, table=True):
    """User table model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(description="Hashed password")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str = Field(max_length=50, description="Username")
    email: str = Field(max_length=100, description="Email address")
    password: str = Field(min_length=6, description="Password")

class UserResponse(UserBase):
    """Model for user response"""
    id: int
    created_at: datetime

class UserLogin(BaseModel):
    """Model for user login"""
    username: str
    password: str

class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token data for validation"""
    username: Optional[str] = None
