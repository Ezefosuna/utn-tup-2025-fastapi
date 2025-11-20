"""Routers for vehicle (auto) management endpoints.

This module handles all CRUD operations for vehicles including creation,
retrieval, updates, and deletion with batch operations support.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Sequence, Optional
from app.database import get_session
from app.models import Auto, AutoCreate, AutoRead, AutoUpdate
from app.repositories import AutoRepository
from app.utils import generate_chasis_number

router = APIRouter(prefix="/autos", tags=["autos"])


def get_auto_repo(session: Session = Depends(get_session)) -> AutoRepository:
    """Dependency to get the Auto repository instance.
    
    Args:
        session: Database session from dependency injection.
        
    Returns:
        AutoRepository: Repository instance for database operations.
    """
    return AutoRepository(session)


@router.post("/", response_model=AutoRead, status_code=status.HTTP_201_CREATED)
def create_auto(auto: AutoCreate, repo: AutoRepository = Depends(get_auto_repo)):
    """Create a new vehicle in the inventory.
    
    Args:
        auto: Vehicle data to create.
        repo: Auto repository instance.
        
    Returns:
        AutoRead: The created vehicle with assigned ID and VIN.
    """
    while True:
        numero_chasis = generate_chasis_number()
        if not repo.get_by_chasis(numero_chasis):
            break

    auto_dict = auto.model_dump()
    auto_dict["numero_chasis"] = numero_chasis
    auto_completo = Auto(**auto_dict)

    repo.session.add(auto_completo)
    repo.session.commit()
    repo.session.refresh(auto_completo)

    return auto_completo


@router.post("/batch/", response_model=Sequence[AutoRead], status_code=status.HTTP_201_CREATED)
def create_multiple_autos(
    autos: list[AutoCreate], repo: AutoRepository = Depends(get_auto_repo)
):
    """Create multiple vehicles in batch.
    
    Args:
        autos: List of vehicle data to create.
        repo: Auto repository instance.
        
    Returns:
        Sequence[AutoRead]: List of created vehicles with assigned IDs and VINs.
    """
    created_autos = []
    for auto in autos:
        while True:
            numero_chasis = generate_chasis_number()
            if not repo.get_by_chasis(numero_chasis):
                break

        auto_dict = auto.model_dump()
        auto_dict["numero_chasis"] = numero_chasis
        auto_completo = Auto(**auto_dict)

        repo.session.add(auto_completo)
        repo.session.flush()
        created_autos.append(auto_completo)

    repo.session.commit()
    for auto_obj in created_autos:
        repo.session.refresh(auto_obj)

    return created_autos


@router.get("/", response_model=Sequence[AutoRead])
def list_autos(
    marca: Optional[str] = None,
    modelo: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    repo: AutoRepository = Depends(get_auto_repo),
):
    """List all vehicles with optional filtering.
    
    Args:
        marca: Optional filter by brand.
        modelo: Optional filter by model.
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.
        repo: Auto repository instance.
        
    Returns:
        Sequence[AutoRead]: List of vehicles matching the criteria.
    """
    return repo.get_all(marca=marca, modelo=modelo, skip=skip, limit=limit)


@router.get("/chasis/{numero_chasis}", response_model=AutoRead)
def get_auto_by_chasis(numero_chasis: str, repo: AutoRepository = Depends(get_auto_repo)):
    """Retrieve a vehicle by its VIN (chassis number).
    
    Args:
        numero_chasis: The vehicle's VIN.
        repo: Auto repository instance.
        
    Returns:
        AutoRead: The requested vehicle.
        
    Raises:
        HTTPException: If vehicle is not found.
    """
    auto = repo.get_by_chasis(numero_chasis)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found with that VIN.",
        )
    return auto


@router.get("/{auto_id}", response_model=AutoRead)
def get_auto(auto_id: int, repo: AutoRepository = Depends(get_auto_repo)):
    """Retrieve a vehicle by its ID.
    
    Args:
        auto_id: The vehicle's unique ID.
        repo: Auto repository instance.
        
    Returns:
        AutoRead: The requested vehicle.
        
    Raises:
        HTTPException: If vehicle is not found.
    """
    auto = repo.get_by_id(auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found."
        )
    return auto


@router.put("/{auto_id}", response_model=AutoRead)
def update_auto(
    auto_id: int, auto_update: AutoUpdate, repo: AutoRepository = Depends(get_auto_repo)
):
    """Update a vehicle's information.
    
    Args:
        auto_id: The vehicle's unique ID.
        auto_update: Updated vehicle data.
        repo: Auto repository instance.
        
    Returns:
        AutoRead: The updated vehicle.
        
    Raises:
        HTTPException: If vehicle is not found.
    """
    auto = repo.get_by_id(auto_id)
    if not auto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found."
        )

    update_data = auto_update.model_dump(exclude_unset=True)
    return repo.update(auto_id, update_data)


@router.delete("/{auto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_auto(auto_id: int, repo: AutoRepository = Depends(get_auto_repo)):
    """Delete a vehicle from the inventory.
    
    Args:
        auto_id: The vehicle's unique ID.
        repo: Auto repository instance.
        
    Raises:
        HTTPException: If vehicle is not found.
    """
    if not repo.delete(auto_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found."
        )