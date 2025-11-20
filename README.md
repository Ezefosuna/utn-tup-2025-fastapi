[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.120-green)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-336791)](https://www.postgresql.org/)

## Descripción General

Una API REST completa construida con **FastAPI**, **SQLModel** y **PostgreSQL** para gestionar inventario de vehículos y transacciones de ventas. La aplicación demuestra una arquitectura lista para producción con código limpio, validación exhaustiva y patrones de diseño modernos.

## ✨ Características Principales

- **CRUD Completo**: Operaciones completas para vehículos y ventas
- **Generación Automática de VIN**: VIN único de 17 caracteres por vehículo (estándar VIN)
- **Filtrado Avanzado**: Búsqueda por marca, modelo, chasis, nombre del comprador
- **Paginación**: Paginación basada en skip/limit para todas las listas
- **Relaciones Uno-a-Muchos**: Manejo automático de relaciones
- **Documentación Interactiva**: Swagger UI + ReDoc
- **Patrón Repositorio**: Abstracción limpia de acceso a datos
- **Inyección de Dependencias**: Sistema DI nativo de FastAPI
- **Seguridad de Tipos**: Anotaciones de tipos Python completas
- **Soporte Async**: Async/await en toda la aplicación

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|-----------|---------|---------|
| FastAPI | 0.120.4 | Framework web |
| SQLModel | 0.0.27 | ORM |
| PostgreSQL | 12+ | Base de datos |
| Uvicorn | 0.38.0 | Servidor ASGI |
| Pydantic | 2.5+ | Validación |
| Pytest | 8.4.2 | Testing |

## 📋 Requisitos

- Python 3.10+
- PostgreSQL 12+
- Git

## 🚀 Inicio Rápido

### 1. Clonar y Configurar

```bash
git clone https://github.com/jeredeldo/utn-tup-2025-fastapi.git
cd back
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar

```bash
cp .env.example .env
# Editar .env con las credenciales de PostgreSQL
```

### 3. Ejecutar

```bash
uvicorn main:app --reload
```

Acceso:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 Endpoints de la API

### Vehículos

```
POST   /autos/             Crear vehículo
POST   /autos/batch/       Crear múltiples
GET    /autos/             Listar (con filtros)
GET    /autos/{id}         Obtener por ID
GET    /autos/chasis/{vin} Obtener por VIN
PUT    /autos/{id}         Actualizar
DELETE /autos/{id}         Eliminar
```

### Ventas

```
POST   /ventas/              Crear venta
POST   /ventas/batch/        Crear múltiples
GET    /ventas/              Listar ventas
GET    /ventas/{id}          Obtener por ID
GET    /ventas/auto/{id}     Obtener por vehículo
GET    /ventas/comprador/{nombre} Obtener por comprador
PUT    /ventas/{id}          Actualizar
DELETE /ventas/{id}          Eliminar
```

## 💾 Esquema de Base de Datos

### Auto
- `id` (Integer, PK)
- `marca` (String, Indexed)
- `modelo` (String, Indexed)
- `año` (Integer)
- `numero_chasis` (String, Unique)

### Venta
- `id` (Integer, PK)
- `auto_id` (Integer, FK)
- `nombre_comprador` (String)
- `precio` (Float)
- `fecha_venta` (DateTime)

## ✔️ Reglas de Validación

- **Año**: 1900 al año actual
- **Precio**: Mayor a 0
- **Nombre del Comprador**: No vacío
- **Fecha de Venta**: No en el futuro
- **VIN**: Auto-generado, único, formato de 17 caracteres

## 📝 Ejemplos de Solicitudes

### Crear Vehículo
```bash
curl -X POST "http://localhost:8000/autos/" \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023
  }'
```

### Crear Venta
```bash
curl -X POST "http://localhost:8000/ventas/" \
  -H "Content-Type: application/json" \
  -d '{
    "auto_id": 1,
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "fecha_venta": "2024-11-19T10:30:00"
  }'
```

## 📂 Estructura del Proyecto

```
.
├── main.py                 # Punto de entrada
├── config.py               # Configuración
├── requirements.txt        # Dependencias
├── .env.example           # Plantilla de variables de entorno
├── README.md              # Documentación principal
├── README_API.md          # Referencia de API
├── DEVELOPMENT.md         # Guía de desarrollo
└── app/
    ├── __init__.py
    ├── database.py        # Configuración de BD
    ├── models.py          # Definiciones SQLModel
    ├── repositories.py    # Acceso a datos
    ├── routers_autos.py   # Rutas de vehículos
    ├── routers_ventas.py  # Rutas de ventas
    └── utils.py           # Utilidades
```

## 🧪 Testing

```bash
# Ejecutar pruebas
pytest

# Verbose
pytest -v

# Con cobertura
pytest --cov=app
```

## 📄 Documentación

- [Referencia de API](./README_API.md) - Documentación detallada de endpoints
- [Desarrollo](./DEVELOPMENT.md) - Flujo de trabajo de desarrollo

## 🔧 Configuración

### Variables de Entorno

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost/car_sales
DEBUG=false
PORT=8000
HOST=0.0.0.0
```

## 📊 Códigos de Estado

| Código | Significado |
|------|---------|
| 200 | OK |
| 201 | Creado |
| 204 | Sin contenido |
| 400 | Solicitud inválida |
| 404 | No encontrado |
| 500 | Error del servidor |

## 🏗️ Arquitectura

### Patrones de Diseño
- **Patrón Repositorio**: Abstracción de acceso a datos
- **Inyección de Dependencias**: Sistema DI de FastAPI
- **Separación de Modelos**: Modelos de BD vs esquemas de API

### Calidad del Código
- Anotaciones de tipo completas
- Docstrings exhaustivos
- Separación limpia de responsabilidades
- Arquitectura async/await

## 📄 Licencia

MIT License

## 👨‍💼 Autor

**Equipo de Desarrollo**  
Repositorio: [github.com/jeredeldo/utn-tup-2025-fastapi](https://github.com/jeredeldo/utn-tup-2025-fastapi)

---

**Versión**: 1.0.0 | **Última Actualización**: Noviembre 2024
