"""Routers for sales (venta) management endpoints.

This module handles all CRUD operations for vehicle sales including creation,
retrieval, updates, and deletion with batch operations and advanced filtering.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Sequence, Optional

from app.database import get_session
from app.models import Venta, VentaCreate, VentaRead, VentaReadWithAuto, VentaUpdate
from app.repositories import VentaRepository, AutoRepository

router = APIRouter(prefix="/ventas", tags=["ventas"])


def get_venta_repo(session: Session = Depends(get_session)) -> VentaRepository:
    """Dependency to get the Sales repository instance.
    
    Args:
        session: Database session from dependency injection.
        
    Returns:
        VentaRepository: Repository instance for sales database operations.
    """
    return VentaRepository(session)


def get_auto_repo(session: Session = Depends(get_session)) -> AutoRepository:
    """Dependency to get the Auto repository instance.
    
    Args:
        session: Database session from dependency injection.
        
    Returns:
        AutoRepository: Repository instance for vehicle database operations.
    """
    return AutoRepository(session)


@router.post("/", response_model=VentaReadWithAuto, status_code=status.HTTP_201_CREATED)
def create_venta(
    venta: VentaCreate,
    repo: VentaRepository = Depends(get_venta_repo),
    auto_repo: AutoRepository = Depends(get_auto_repo),
):
    """Create a new sales record.
    
    Args:
        venta: Sales data to create.
        repo: Sales repository instance.
        auto_repo: Auto repository for validation.
        
    Returns:
        VentaReadWithAuto: The created sales record with vehicle information.
        
    Raises:
        HTTPException: If the referenced vehicle is not found.
    """
    if not auto_repo.get_by_id(venta.auto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found."
        )
    return repo.create(venta)


@router.post(
    "/batch/", response_model=Sequence[VentaReadWithAuto], status_code=status.HTTP_201_CREATED
)
def create_multiple_ventas(
    ventas: list[VentaCreate],
    repo: VentaRepository = Depends(get_venta_repo),
    auto_repo: AutoRepository = Depends(get_auto_repo),
):
    """Create multiple sales records in batch.
    
    Args:
        ventas: List of sales data to create.
        repo: Sales repository instance.
        auto_repo: Auto repository for validation.
        
    Returns:
        Sequence[VentaReadWithAuto]: List of created sales records.
        
    Raises:
        HTTPException: If any referenced vehicle is not found.
    """
    for venta in ventas:
        if not auto_repo.get_by_id(venta.auto_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with ID {venta.auto_id} not found.",
            )
    return repo.create_multiple(ventas)


@router.get("/", response_model=Sequence[VentaReadWithAuto])
def list_ventas(
    skip: int = 0, limit: int = 10, repo: VentaRepository = Depends(get_venta_repo)
):
    """List all sales records with pagination.
    
    Args:
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        repo: Sales repository instance.
        
    Returns:
        Sequence[VentaReadWithAuto]: List of sales records.
    """
    return repo.get_all(skip=skip, limit=limit)


@router.get("/auto/{auto_id}", response_model=Sequence[VentaReadWithAuto])
def get_ventas_by_auto(
    auto_id: int,
    repo: VentaRepository = Depends(get_venta_repo),
    auto_repo: AutoRepository = Depends(get_auto_repo),
):
    """Get all sales for a specific vehicle.
    
    Args:
        auto_id: The vehicle's unique ID.
        repo: Sales repository instance.
        auto_repo: Auto repository for validation.
        
    Returns:
        Sequence[VentaReadWithAuto]: List of sales for the vehicle.
        
    Raises:
        HTTPException: If the vehicle is not found.
    """
    if not auto_repo.get_by_id(auto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found."
        )
    return repo.get_by_auto_id(auto_id)


@router.get("/comprador/{nombre}", response_model=Sequence[VentaReadWithAuto])
def get_ventas_by_comprador(
    nombre: str, repo: VentaRepository = Depends(get_venta_repo)
):
    """Get all sales by a specific buyer name.
    
    Args:
        nombre: The buyer's name.
        repo: Sales repository instance.
        
    Returns:
        Sequence[VentaReadWithAuto]: List of sales for the buyer.
    """
    return repo.get_by_comprador(nombre)


@router.get("/{venta_id}", response_model=VentaReadWithAuto)
def get_venta(venta_id: int, repo: VentaRepository = Depends(get_venta_repo)):
    """Retrieve a specific sales record.
    
    Args:
        venta_id: The sales record's unique ID.
        repo: Sales repository instance.
        
    Returns:
        VentaReadWithAuto: The requested sales record with vehicle info.
        
    Raises:
        HTTPException: If the sales record is not found.
    """
    venta = repo.get_by_id(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sales record not found."
        )
    return venta


@router.put("/{venta_id}", response_model=VentaRead)
def update_venta(
    venta_id: int,
    venta_update: VentaUpdate,
    repo: VentaRepository = Depends(get_venta_repo),
):
    """Update a sales record.
    
    Args:
        venta_id: The sales record's unique ID.
        venta_update: Updated sales data.
        repo: Sales repository instance.
        
    Returns:
        VentaRead: The updated sales record.
        
    Raises:
        HTTPException: If the sales record is not found.
    """
    venta = repo.get_by_id(venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sales record not found."
        )

    update_data = venta_update.model_dump(exclude_unset=True)
    return repo.update(venta_id, update_data)


@router.delete("/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_venta(venta_id: int, repo: VentaRepository = Depends(get_venta_repo)):
    """Delete a sales record.
    
    Args:
        venta_id: The sales record's unique ID.
        repo: Sales repository instance.
        
    Raises:
        HTTPException: If the sales record is not found.
    """
    if not repo.delete(venta_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sales record not found."
        )