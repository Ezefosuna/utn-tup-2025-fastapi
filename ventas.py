from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from database import get_session
from repository import VentaRepository, VentaRepositoryInterface, AutoRepository, AutoRepositoryInterface
from models import VentaCreate, VentaResponse, VentaUpdate, VentaResponseWithAuto

router = APIRouter(
    prefix="/ventas",
    tags=["ventas"],
)

def get_venta_repo(session: Session = Depends(get_session)) -> VentaRepositoryInterface:
    return VentaRepository(session)

def get_auto_repo(session: Session = Depends(get_session)) -> AutoRepositoryInterface:
    return AutoRepository(session)

@router.post("/", response_model=VentaResponse)
def create_venta(venta: VentaCreate, repo: VentaRepositoryInterface = Depends(get_venta_repo), auto_repo: AutoRepositoryInterface = Depends(get_auto_repo)):
    # Validate that the auto exists
    db_auto = auto_repo.get_by_id(venta.auto_id)
    if not db_auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return repo.create(venta)

@router.get("/", response_model=List[VentaResponse])
def get_all_ventas(skip: int = 0, limit: int = 100, repo: VentaRepositoryInterface = Depends(get_venta_repo)):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{venta_id}", response_model=VentaResponse)
def get_venta_by_id(venta_id: int, repo: VentaRepositoryInterface = Depends(get_venta_repo)):
    db_venta = repo.get_by_id(venta_id)
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_venta

@router.put("/{venta_id}", response_model=VentaResponse)
def update_venta(venta_id: int, venta_update: VentaUpdate, repo: VentaRepositoryInterface = Depends(get_venta_repo)):
    db_venta = repo.update(venta_id, venta_update)
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_venta

@router.delete("/{venta_id}", status_code=204)
def delete_venta(venta_id: int, repo: VentaRepositoryInterface = Depends(get_venta_repo)):
    if not repo.delete(venta_id):
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return

@router.get("/auto/{auto_id}", response_model=List[VentaResponse])
def get_ventas_by_auto_id(auto_id: int, repo: VentaRepositoryInterface = Depends(get_venta_repo)):
    return repo.get_by_auto_id(auto_id)

@router.get("/comprador/{nombre}", response_model=List[VentaResponse])
def get_ventas_by_comprador(nombre: str, repo: VentaRepositoryInterface = Depends(get_venta_repo)):
    return repo.get_by_comprador(nombre)

@router.get("/{venta_id}/with-auto", response_model=VentaResponseWithAuto)
def get_venta_with_auto(venta_id: int, repo: VentaRepositoryInterface = Depends(get_venta_repo)):
    db_venta = repo.get_by_id(venta_id)
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return db_venta
