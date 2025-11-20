# Guía de Desarrollo

## Configuración

### Requisitos Previos
- Python 3.10+
- PostgreSQL 12+
- Git
- Editor de texto (VS Code recomendado)

### Configuración Inicial

1. **Clonar Repositorio**
   ```bash
   git clone https://github.com/jeredeldo/utn-tup-2025-fastapi.git
   cd back
   ```

2. **Crear Entorno Virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Instalar Dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus credenciales de PostgreSQL
   ```

5. **Ejecutar Aplicación**
   ```bash
   uvicorn main:app --reload
   ```

## Estructura del Proyecto

```
.
├── main.py                 # Punto de entrada de la aplicación
├── config.py               # Configuración
├── requirements.txt        # Dependencias
├── .env.example           # Plantilla de variables de entorno
├── .gitignore             # Reglas de git ignore
│
├── app/
│   ├── __init__.py
│   ├── database.py        # Configuración de base de datos
│   ├── models.py          # Definiciones de SQLModel
│   ├── repositories.py    # Patrón repositorio
│   ├── routers_autos.py   # Endpoints de vehículos
│   ├── routers_ventas.py  # Endpoints de ventas
│   └── utils.py           # Funciones de utilidad
│
└── tests/
    ├── __init__.py
    └── test_endpoints.py  # Pruebas de API
```

## Propósito de los Archivos

### main.py
- Inicialización de la aplicación FastAPI
- Registro de routers
- Configuración de middleware CORS
- Handlers de eventos del ciclo de vida

### config.py
- Configuración centralizada
- Variables de entorno
- Configuración de la aplicación

### app/database.py
- Configuración del motor SQLModel
- Gestión de sesiones
- Inicialización de base de datos

### app/models.py
- Definiciones de SQLModel
- Esquemas de Pydantic
- Decoradores de validación

### app/repositories.py
- Clase AutoRepository
- Clase VentaRepository
- Métodos de acceso a datos

### app/routers_autos.py
- Endpoints de vehículos
- Operaciones CRUD
- Validación de solicitudes

### app/routers_ventas.py
- Endpoints de ventas
- Operaciones CRUD
- Validación de solicitudes

### app/utils.py
- Funciones de validación
- Generación de VIN
- Funciones auxiliares

## Flujo de Trabajo de Desarrollo

### 1. Desarrollo de Características

Crear una rama de características:
```bash
git checkout -b feature/tu-caracteristica
```

Hacer cambios y probar:
```bash
pytest tests/ -v
```

Hacer commit y push:
```bash
git add .
git commit -m "feat: describe tu característica"
git push origin feature/tu-caracteristica
```

### 2. Ejecutar Pruebas

Ejecutar todas las pruebas:
```bash
pytest tests/ -v
```

Ejecutar prueba específica:
```bash
pytest tests/test_endpoints.py::test_create_auto -v
```

Ejecutar con cobertura:
```bash
pytest --cov=app --cov-report=html
```

### 3. Calidad del Código

Verificar con Pylance (en VS Code):
- Instalar extensión Pylance
- Ver el panel de problemas para problemas

Formatear código:
```bash
pip install black
black app/ main.py config.py
```

Verificar tipos:
```bash
pip install mypy
mypy app/ main.py config.py
```

### 4. Agregar Nuevos Endpoints

1. Definir modelo en `app/models.py`
2. Agregar método de repositorio en `app/repositories.py`
3. Crear router en `app/routers_*.py`
4. Registrar router en `main.py`
5. Agregar pruebas en `tests/test_endpoints.py`
6. Actualizar documentación

Ejemplo:

**models.py**:
```python
class MiCreacion(SQLModel):
    campo: str
    
class MiLectura(MiCreacion):
    id: int
```

**repositories.py**:
```python
class MiRepositorio:
    def crear(self, mi_creacion: MiCreacion) -> Mi:
        # Implementación
        pass
```

**routers_*.py**:
```python
@router.post("/endpoint/", response_model=MiLectura)
def crear_mi(mi: MiCreacion, repo = Depends(get_repo)):
    return repo.crear(mi)
```

## Variables de Entorno

Crear archivo `.env`:

```env
# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost/car_sales

# Aplicación
DEBUG=false
PORT=8000
HOST=0.0.0.0
```

## Debugging

### Usando print()
```python
print(f"Debug: {variable}")
```

### Usando debugger
```bash
# En VS Code, agregar breakpoints y presionar F5
```

### Revisar logs
```bash
# Los logs de Uvicorn aparecen en la terminal
```

## Problemas Comunes

### Errores de Importación
```bash
# Activar entorno virtual
source venv/bin/activate
```

### Conexión a Base de Datos
```bash
# Verificar que PostgreSQL está ejecutándose
# Verificar credenciales en .env
# Verificar que la base de datos existe
```

### Pruebas Fallidas
```bash
# Limpiar caché de pytest
pytest --cache-clear

# Ejecutar con salida verbose
pytest -vv
```

## Gestión de Base de Datos

### Crear Base de Datos
```bash
psql -U postgres -c "CREATE DATABASE car_sales;"
```

### Eliminar Base de Datos
```bash
psql -U postgres -c "DROP DATABASE car_sales;"
```

### Acceder a la Base de Datos
```bash
psql -U postgres -d car_sales
```

## Optimización del Desempeño

### Agregar Índices
```python
# En models.py
campo: str = Field(index=True)
```

### Agrupación de Conexiones
```python
# En database.py
engine = create_engine(
    DATABASE_URL,
    connect_args={"pool_size": 10, "max_overflow": 20}
)
```

### Optimización de Consultas
```python
# Usar declaraciones select eficientemente
statement = select(Auto).where(Auto.marca == "Toyota")
```

## Implementación

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Usando Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Usando Docker Compose
```yaml
version: '3'
services:
  db:
    image: postgres:12
    environment:
      POSTGRES_PASSWORD: contraseña
      POSTGRES_DB: car_sales
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://postgres:contraseña@db/car_sales
```

## Mejores Prácticas

1. **Siempre anotar tipos** en tus funciones
2. **Agregar docstrings** a todas las funciones
3. **Manejar errores gracefully** con try/except
4. **Escribir pruebas** para nuevas características
5. **Usar repositorios** para acceso a datos
6. **Mantener funciones pequeñas** y enfocadas
7. **Comentar lógica compleja** claramente
8. **Usar nombres significativos** para variables

## Comandos Útiles

```bash
# Ejecutar app
uvicorn main:app --reload

# Ejecutar pruebas
pytest tests/ -v

# Formatear código
black app/ main.py config.py

# Verificar tipos
mypy app/ main.py

# Instalar nuevo paquete
pip install nombre-paquete

# Generar requisitos
pip freeze > requirements.txt

# Crear base de datos
psql -U postgres -c "CREATE DATABASE car_sales;"

# Acceder a base de datos
psql -U postgres -d car_sales
```

## Recursos

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de SQLModel](https://sqlmodel.tiangolo.com/)
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación de Python](https://docs.python.org/3/)
- [Documentación de Pydantic](https://docs.pydantic.dev/)

---

**Última Actualización**: Noviembre 2024
