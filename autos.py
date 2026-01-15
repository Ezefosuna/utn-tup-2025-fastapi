from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlmodel import Session
from database import get_session
from repository import AutoRepository, AutoRepositoryInterface
from models import AutoCreate, AutoResponse, AutoUpdate, AutoResponseWithVentas

router = APIRouter(
    prefix="/autos",
    tags=["autos"],
)

def get_auto_repo(session: Session = Depends(get_session)) -> AutoRepositoryInterface:
    return AutoRepository(session)

@router.post("/", response_model=AutoResponse)
def create_auto(auto: AutoCreate, repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    db_auto = repo.get_by_chasis(auto.numero_chasis)
    if db_auto:
        raise HTTPException(status_code=400, detail="Número de chasis ya registrado")
    return repo.create(auto)

@router.get("/", response_model=List[AutoResponse])
def get_all_autos(skip: int = 0, limit: int = 100, repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{auto_id}", response_model=AutoResponse)
def get_auto_by_id(auto_id: int, repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    db_auto = repo.get_by_id(auto_id)
    if not db_auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return db_auto

@router.get("/chasis/{numero_chasis}", response_model=AutoResponse)
def get_auto_by_chasis(numero_chasis: str, repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    db_auto = repo.get_by_chasis(numero_chasis)
    if not db_auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return db_auto

@router.put("/{auto_id}", response_model=AutoResponse)
def update_auto(auto_id: int, auto_update: AutoUpdate, repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    db_auto = repo.update(auto_id, auto_update)
    if not db_auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return db_auto

@router.delete("/{auto_id}", status_code=204)
def delete_auto(auto_id: int, repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    if not repo.delete(auto_id):
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return

@router.get("/{auto_id}/with-ventas", response_model=AutoResponseWithVentas)
def get_auto_with_ventas(auto_id: int, repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    db_auto = repo.get_by_id(auto_id)
    if not db_auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return db_auto
