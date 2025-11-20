"""SQLModel data models for the application.

This module defines the data models for vehicles and sales with validation,
relationships, and serialization schemas for API responses.
"""
from __future__ import annotations

from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from app.utils import (
    is_valid_year,
    is_valid_price,
    is_valid_future_date,
    is_valid_comprador_name,
)


# ============================================================================
# Vehicle (Auto) Models
# ============================================================================


class AutoBase(SQLModel):
    """Base vehicle model with common fields."""

    marca: str = Field(index=True, description="Vehicle brand/manufacturer")
    modelo: str = Field(index=True, description="Vehicle model name")
    año: int = Field(description="Year of manufacture")
    numero_chasis: str = Field(unique=True, description="Vehicle Identification Number (VIN)")


class Auto(AutoBase, table=True):
    """Vehicle database model with relationships."""

    id: Optional[int] = Field(default=None, primary_key=True)
    ventas: List[Venta] = Relationship(back_populates="auto")


class AutoCreate(SQLModel):
    """Schema for creating a new vehicle."""

    marca: str = Field(description="Vehicle brand")
    modelo: str = Field(description="Vehicle model")
    año: int = Field(description="Year of manufacture")

    @field_validator("año")
    @classmethod
    def validate_year(cls, v):
        """Validate year is between 1900 and current year."""
        if not is_valid_year(v):
            raise ValueError("Year must be between 1900 and the current year.")
        return v


class AutoRead(AutoBase):
    """Schema for reading a vehicle."""

    id: int = Field(description="Unique vehicle identifier")


class AutoUpdate(SQLModel):
    """Schema for updating a vehicle."""

    marca: Optional[str] = Field(None, description="Vehicle brand")
    modelo: Optional[str] = Field(None, description="Vehicle model")
    año: Optional[int] = Field(None, description="Year of manufacture")

    @field_validator("año")
    @classmethod
    def validate_year(cls, v):
        """Validate year if provided."""
        if v is not None and not is_valid_year(v):
            raise ValueError("Year must be between 1900 and the current year.")
        return v


class AutoReadWithVentas(AutoRead):
    """Schema for reading a vehicle with all its sales records."""

    ventas: List["VentaRead"] = Field(default_factory=list, description="List of sales for this vehicle")


# ============================================================================
# Sales (Venta) Models
# ============================================================================


class VentaBase(SQLModel):
    """Base sales model with common fields."""

    nombre_comprador: str = Field(index=True, description="Buyer's full name")
    precio: float = Field(gt=0, description="Sale price (must be greater than 0)")
    fecha_venta: datetime = Field(description="Date when the sale occurred")


class Venta(VentaBase, table=True):
    """Sales transaction database model with relationships."""

    id: Optional[int] = Field(default=None, primary_key=True)
    auto_id: int = Field(foreign_key="auto.id")
    auto: Optional[Auto] = Relationship(back_populates="ventas")


class VentaCreate(VentaBase):
    """Schema for creating a new sales record."""

    auto_id: int = Field(description="ID of the vehicle being sold")

    @field_validator("nombre_comprador")
    @classmethod
    def validate_comprador_name(cls, v):
        """Validate buyer name is not empty."""
        if not is_valid_comprador_name(v):
            raise ValueError("Buyer name cannot be empty.")
        return v

    @field_validator("precio")
    @classmethod
    def validate_price(cls, v):
        """Validate price is greater than zero."""
        if not is_valid_price(v):
            raise ValueError("Price must be greater than 0.")
        return v

    @field_validator("fecha_venta")
    @classmethod
    def validate_fecha_venta(cls, v):
        """Validate sale date is not in the future."""
        if not is_valid_future_date(v):
            raise ValueError("Sale date cannot be in the future.")
        return v


class VentaRead(VentaBase):
    """Schema for reading a sales record."""

    id: int = Field(description="Unique sales record identifier")
    auto_id: int = Field(description="ID of the sold vehicle")


class VentaUpdate(SQLModel):
    """Schema for updating a sales record."""

    nombre_comprador: Optional[str] = Field(None, description="Buyer's name")
    precio: Optional[float] = Field(None, gt=0, description="Sale price")
    fecha_venta: Optional[datetime] = Field(None, description="Sale date")

    @field_validator("nombre_comprador")
    @classmethod
    def validate_comprador_name(cls, v):
        """Validate buyer name if provided."""
        if v is not None and not is_valid_comprador_name(v):
            raise ValueError("Buyer name cannot be empty.")
        return v

    @field_validator("precio")
    @classmethod
    def validate_price(cls, v):
        """Validate price if provided."""
        if v is not None and not is_valid_price(v):
            raise ValueError("Price must be greater than 0.")
        return v

    @field_validator("fecha_venta")
    @classmethod
    def validate_fecha_venta(cls, v):
        """Validate sale date if provided."""
        if v is not None and not is_valid_future_date(v):
            raise ValueError("Sale date cannot be in the future.")
        return v


class VentaReadWithAuto(VentaRead):
    """Schema for reading a sales record with complete vehicle information."""

    auto: Optional[AutoRead] = Field(None, description="Details of the sold vehicle")