from abc import ABC, abstractmethod
from typing import List, Optional
from sqlmodel import Session, select
from models import Auto, AutoCreate, AutoUpdate, Venta, VentaCreate, VentaUpdate

class AutoRepositoryInterface(ABC):
    """Interface for Auto repository"""
    
    @abstractmethod
    def create(self, auto: AutoCreate) -> Auto:
        pass
    
    @abstractmethod
    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        pass
    
    @abstractmethod
    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Auto]:
        pass
    
    @abstractmethod
    def update(self, auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]:
        pass
    
    @abstractmethod
    def delete(self, auto_id: int) -> bool:
        pass

class AutoRepository(AutoRepositoryInterface):
    """Repository for Auto entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, auto: AutoCreate) -> Auto:
        db_auto = Auto.model_validate(auto)
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto
    
    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        statement = select(Auto).where(Auto.id == auto_id)
        return self.session.exec(statement).first()

    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        statement = select(Auto).where(Auto.numero_chasis == numero_chasis)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Auto]:
        statement = select(Auto).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]:
        db_auto = self.get_by_id(auto_id)
        if not db_auto:
            return None
        
        auto_data = auto_update.model_dump(exclude_unset=True)
        for key, value in auto_data.items():
            setattr(db_auto, key, value)
        
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto
    
    def delete(self, auto_id: int) -> bool:
        db_auto = self.get_by_id(auto_id)
        if not db_auto:
            return False
        
        self.session.delete(db_auto)
        self.session.commit()
        return True

class VentaRepositoryInterface(ABC):
    """Interface for Venta repository"""
    
    @abstractmethod
    def create(self, venta: VentaCreate) -> Venta:
        pass
    
    @abstractmethod
    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venta]:
        pass
    
    @abstractmethod
    def update(self, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
        pass
    
    @abstractmethod
    def delete(self, venta_id: int) -> bool:
        pass

    @abstractmethod
    def get_by_auto_id(self, auto_id: int) -> List[Venta]:
        pass

    @abstractmethod
    def get_by_comprador(self, nombre: str) -> List[Venta]:
        pass

class VentaRepository(VentaRepositoryInterface):
    """Repository for Venta entity using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, venta: VentaCreate) -> Venta:
        db_venta = Venta.model_validate(venta)
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta
    
    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        statement = select(Venta).where(Venta.id == venta_id)
        return self.session.exec(statement).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venta]:
        statement = select(Venta).offset(skip).limit(limit)
        return self.session.exec(statement).all()
    
    def update(self, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
        db_venta = self.get_by_id(venta_id)
        if not db_venta:
            return None
        
        venta_data = venta_update.model_dump(exclude_unset=True)
        for key, value in venta_data.items():
            setattr(db_venta, key, value)
        
        self.session.add(db_venta)
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta
    
    def delete(self, venta_id: int) -> bool:
        db_venta = self.get_by_id(venta_id)
        if not db_venta:
            return False
        
        self.session.delete(db_venta)
        self.session.commit()
        return True

    def get_by_auto_id(self, auto_id: int) -> List[Venta]:
        statement = select(Venta).where(Venta.auto_id == auto_id)
        return self.session.exec(statement).all()

    def get_by_comprador(self, nombre: str) -> List[Venta]:
        statement = select(Venta).where(Venta.nombre_comprador.ilike(f"%{nombre}%"))
        return self.session.exec(statement).all()
