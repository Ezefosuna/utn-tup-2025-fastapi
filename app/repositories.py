"""Repository classes for database operations.

This module provides repository pattern implementations for data access,
handling all database operations for vehicles and sales records.
"""
from typing import List, Optional, Sequence
from sqlmodel import Session, select
from sqlalchemy import func
from app.models import Auto, AutoCreate, Venta, VentaCreate


class AutoRepository:
    """Repository for vehicle database operations."""

    def __init__(self, session: Session):
        """Initialize the repository with a database session.
        
        Args:
            session: Active SQLModel database session.
        """
        self.session = session

    def create(self, auto_create: AutoCreate) -> Auto:
        """Create a new vehicle record.
        
        Args:
            auto_create: Vehicle creation schema.
            
        Returns:
            Auto: The created vehicle record with ID.
        """
        auto = Auto.model_validate(auto_create, from_attributes=True)
        self.session.add(auto)
        self.session.commit()
        self.session.refresh(auto)
        return auto

    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        """Get a vehicle by its ID.
        
        Args:
            auto_id: The vehicle's unique ID.
            
        Returns:
            Optional[Auto]: The vehicle if found, None otherwise.
        """
        return self.session.get(Auto, auto_id)

    def get_all(
        self,
        marca: Optional[str] = None,
        modelo: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> Sequence[Auto]:
        """Get all vehicles with optional filtering.
        
        Args:
            marca: Optional filter by brand (case-insensitive partial match).
            modelo: Optional filter by model (case-insensitive partial match).
            skip: Number of records to skip for pagination.
            limit: Maximum number of records to return.
            
        Returns:
            Sequence[Auto]: List of vehicles matching the criteria.
        """
        statement = select(Auto)
        if marca:
            statement = statement.where(
                func.lower(Auto.marca).like(f"%{marca.lower()}%")
            )
        if modelo:
            statement = statement.where(
                func.lower(Auto.modelo).like(f"%{modelo.lower()}%")
            )
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        """Get a vehicle by its VIN.
        
        Args:
            numero_chasis: The vehicle's VIN.
            
        Returns:
            Optional[Auto]: The vehicle if found, None otherwise.
        """
        statement = select(Auto).where(Auto.numero_chasis == numero_chasis)
        return self.session.exec(statement).first()

    def update(self, auto_id: int, auto_data: dict) -> Optional[Auto]:
        """Update a vehicle record.
        
        Args:
            auto_id: The vehicle's unique ID.
            auto_data: Dictionary of fields to update.
            
        Returns:
            Optional[Auto]: The updated vehicle if found, None otherwise.
        """
        auto = self.get_by_id(auto_id)
        if not auto:
            return None
        for key, value in auto_data.items():
            setattr(auto, key, value)
        self.session.add(auto)
        self.session.commit()
        self.session.refresh(auto)
        return auto

    def delete(self, auto_id: int) -> bool:
        """Delete a vehicle record.
        
        Args:
            auto_id: The vehicle's unique ID.
            
        Returns:
            bool: True if deletion was successful, False if not found.
        """
        auto = self.get_by_id(auto_id)
        if not auto:
            return False
        self.session.delete(auto)
        self.session.commit()
        return True

    def create_multiple(self, autos: List[AutoCreate]) -> List[Auto]:
        """Create multiple vehicle records in batch.
        
        Args:
            autos: List of vehicle creation schemas.
            
        Returns:
            List[Auto]: List of created vehicle records.
        """
        created_autos = []
        for auto_create in autos:
            auto = self.create(auto_create)
            created_autos.append(auto)
        return created_autos


class VentaRepository:
    """Repository for sales transaction database operations."""

    def __init__(self, session: Session):
        """Initialize the repository with a database session.
        
        Args:
            session: Active SQLModel database session.
        """
        self.session = session

    def create(self, venta_create: VentaCreate) -> Venta:
        """Create a new sales record.
        
        Args:
            venta_create: Sales creation schema.
            
        Returns:
            Venta: The created sales record with ID.
        """
        venta = Venta.model_validate(venta_create, from_attributes=True)
        self.session.add(venta)
        self.session.commit()
        self.session.refresh(venta)
        return venta

    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        """Get a sales record by its ID.
        
        Args:
            venta_id: The sales record's unique ID.
            
        Returns:
            Optional[Venta]: The sales record if found, None otherwise.
        """
        return self.session.get(Venta, venta_id)

    def get_all(self, skip: int = 0, limit: int = 10) -> Sequence[Venta]:
        """Get all sales records with pagination.
        
        Args:
            skip: Number of records to skip for pagination.
            limit: Maximum number of records to return.
            
        Returns:
            Sequence[Venta]: List of sales records.
        """
        statement = select(Venta).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_auto_id(self, auto_id: int) -> Sequence[Venta]:
        """Get all sales for a specific vehicle.
        
        Args:
            auto_id: The vehicle's unique ID.
            
        Returns:
            Sequence[Venta]: List of sales for the vehicle.
        """
        statement = select(Venta).where(Venta.auto_id == auto_id)
        return self.session.exec(statement).all()

    def get_by_comprador(self, nombre: str) -> Sequence[Venta]:
        """Get all sales by a specific buyer name.
        
        Args:
            nombre: The buyer's name (case-insensitive partial match).
            
        Returns:
            Sequence[Venta]: List of sales for the buyer.
        """
        statement = select(Venta).where(
            func.lower(Venta.nombre_comprador).like(f"%{nombre.lower()}%")
        )
        return self.session.exec(statement).all()

    def update(self, venta_id: int, venta_data: dict) -> Optional[Venta]:
        """Update a sales record.
        
        Args:
            venta_id: The sales record's unique ID.
            venta_data: Dictionary of fields to update.
            
        Returns:
            Optional[Venta]: The updated sales record if found, None otherwise.
        """
        venta = self.get_by_id(venta_id)
        if not venta:
            return None
        for key, value in venta_data.items():
            setattr(venta, key, value)
        self.session.add(venta)
        self.session.commit()
        self.session.refresh(venta)
        return venta

    def delete(self, venta_id: int) -> bool:
        """Delete a sales record.
        
        Args:
            venta_id: The sales record's unique ID.
            
        Returns:
            bool: True if deletion was successful, False if not found.
        """
        venta = self.get_by_id(venta_id)
        if not venta:
            return False
        self.session.delete(venta)
        self.session.commit()
        return True

    def count_by_modelo(self, modelo: str) -> int:
        """Count sales for a specific vehicle model.
        
        Args:
            modelo: The vehicle model name.
            
        Returns:
            int: Number of sales for the model.
        """
        statement = (
            select(func.count())
            .select_from(Venta)
            .join(Auto)
            .where(Auto.modelo == modelo)
        )
        result = self.session.exec(statement).first()
        return result if result is not None else 0

    def create_multiple(self, ventas: List[VentaCreate]) -> List[Venta]:
        """Create multiple sales records in batch.
        
        Args:
            ventas: List of sales creation schemas.
            
        Returns:
            List[Venta]: List of created sales records.
        """
        created_ventas = []
        for venta_create in ventas:
            venta = self.create(venta_create)
            created_ventas.append(venta)
        return created_ventas