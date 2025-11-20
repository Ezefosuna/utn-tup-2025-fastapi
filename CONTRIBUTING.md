# 📋 Guía de Contribución y Estándares de Código

Este documento describe los estándares de código y convenciones para mantener la consistencia del proyecto FastAPI.

## 🎯 Estándares de Código Python

### Convenciones de Nombres

- **Funciones y variables**: `snake_case` (ej: `create_auto`, `get_ventas`)
- **Clases y modelos**: `PascalCase` (ej: `Auto`, `VentaCreate`, `AutoResponse`)
- **Constantes**: `UPPER_SNAKE_CASE` (ej: `API_PREFIX`, `MAX_RETRIES`)
- **Módulos y archivos**: `snake_case` (ej: `auth_router.py`, `models.py`)
- **Rutas API**: lowercase con guiones (ej: `/api/v1/autos`, `/auth/login`)

### Estructura de Imports

```python
# 1. Imports de librerías estándar
from datetime import datetime, timedelta
from typing import Optional, List
from functools import lru_cache

# 2. Imports de librerías externas
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import SQLModel, Session, select, create_engine
from pydantic import Field, field_validator

# 3. Imports locales
from config import DATABASE_URL, DEBUG
from app.models import Auto, Venta
from app.database import get_session
```

### Docstrings

Todo archivo debe tener un docstring de módulo:

```python
"""Module description.

This module provides [functionality] for [purpose].
It includes:
- Feature 1
- Feature 2
"""
```

Toda función debe tener docstring con Args, Returns, y Raises:

```python
def create_auto(auto_data: AutoCreate, session: Session = Depends(get_session)) -> Auto:
    """Create a new vehicle.
    
    Args:
        auto_data: Vehicle data to create
        session: Database session
    
    Returns:
        Auto: Created vehicle
    
    Raises:
        HTTPException: If vehicle creation fails or validation errors
    """
    # implementation
```

### Estructura de Archivos

#### Routers

```python
"""Router description."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.models import Auto, AutoCreate, AutoResponse

router = APIRouter(
    prefix="/api/v1/autos",
    tags=["Vehicles"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[AutoResponse])
async def list_autos(
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
) -> List[AutoResponse]:
    """List all vehicles with pagination."""
    # implementation
```

#### Modelos

```python
"""Models for [entity]."""

from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator
from typing import Optional, List


class AutoBase(SQLModel):
    """Base model for Auto."""
    
    marca: str = Field(index=True, description="Vehicle brand")
    modelo: str = Field(index=True, description="Model name")
    año: int = Field(description="Year of manufacture")


class Auto(AutoBase, table=True):
    """Auto table model."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    numero_chasis: str = Field(unique=True, description="VIN")
    ventas: List["Venta"] = Relationship(back_populates="auto")


class AutoCreate(AutoBase):
    """Model for creating Auto."""
    pass


class AutoResponse(AutoBase):
    """Response model for Auto."""
    
    id: int
    numero_chasis: str
```

## 🔄 Manejo de Errores

### Lanzar Excepciones

```python
from fastapi import HTTPException, status

# Error de validación
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# No encontrado
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Vehicle not found"
)

# No autorizado
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Authentication required"
)

# Conflict
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Resource already exists"
)
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def create_auto(auto_data: AutoCreate, session: Session):
    try:
        # implementation
        logger.info(f"Auto created: {auto.id}")
    except Exception as e:
        logger.error(f"Error creating auto: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## 🧪 Testing

### Test Structure

```python
"""Tests for auto endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.models import Auto

client = TestClient(app)


@pytest.fixture
def sample_auto_data():
    """Fixture for sample auto data."""
    return {
        "marca": "Toyota",
        "modelo": "Corolla",
        "año": 2023
    }


def test_create_auto(sample_auto_data):
    """Test creating a new auto."""
    response = client.post("/api/v1/autos/", json=sample_auto_data)
    assert response.status_code == 201
    assert response.json()["marca"] == "Toyota"


def test_list_autos():
    """Test listing all autos."""
    response = client.get("/api/v1/autos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## 📊 Validación de Datos

### Field Validators

```python
from pydantic import field_validator


class Auto(AutoBase, table=True):
    año: int
    
    @field_validator('año')
    @classmethod
    def validate_year(cls, v):
        """Validate year is between 1900 and current year."""
        if v < 1900 or v > 2024:
            raise ValueError('Year must be between 1900 and 2024')
        return v
```

## 🔐 Autenticación y Seguridad

### Variables de Entorno

```python
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DEBUG=false
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
CORS_ORIGINS=["http://localhost:3000", "https://example.com"]
```

### Protected Routes

```python
from auth import get_current_active_user

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user: User = Depends(get_current_active_user)):
    """Get current authenticated user."""
    return current_user
```

## 📝 Commits y PRs

### Mensaje de Commits

```
[TYPE] Brief description

More detailed explanation if needed.

Fixes #123
```

Tipos permitidos:
- `[Feature]` → Nueva funcionalidad
- `[Fix]` → Corrección de bug
- `[Refactor]` → Cambio de código sin funcionalidad nueva
- `[Docs]` → Cambios en documentación
- `[Test]` → Cambios en tests
- `[Chore]` → Cambios de configuración, dependencias, etc

### Pull Request

1. Crear rama: `git checkout -b feature/description`
2. Hacer commits semánticos
3. Hacer push a rama
4. Abrir PR con descripción clara
5. Aguardar revisión

## 🚀 Deployment

### Producción

```bash
# Build
pip install -r requirements.txt

# Environment
cp .env.example .env
# Editar .env con valores reales

# Database
python -m alembic upgrade head

# Run
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Docker

```bash
# Build image
docker build -t fastapi-app .

# Run container
docker run -p 8000:8000 --env-file .env fastapi-app

# Con Docker Compose
docker-compose up -d
```

## ✅ Checklist Antes de Submitear Código

- [ ] Código sigue convenciones de nombres
- [ ] Funciones tienen docstrings completos
- [ ] No hay `print()` (usar logging)
- [ ] No hay hardcoded secrets
- [ ] No hay imports no utilizados
- [ ] Tests pasan (`pytest`)
- [ ] Linter pasa (`pylint`, `flake8`)
- [ ] No hay warnings al compilar
- [ ] Documentación está actualizada
- [ ] Commit message es descriptivo

## 📚 Recursos

- [FastAPI Official Docs](https://fastapi.tiangolo.com)
- [SQLModel Official Docs](https://sqlmodel.tiangolo.com)
- [PEP 8 Style Guide](https://pep8.org)
- [REST API Best Practices](https://restfulapi.net)

---

**Última actualización**: Noviembre 2024
**Versión**: 1.0.0
