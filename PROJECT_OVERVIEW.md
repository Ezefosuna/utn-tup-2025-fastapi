"""
================================================================================
PROYECTO FASTAPI - SISTEMA DE GESTIÓN DE VENTAS DE VEHÍCULOS
================================================================================

Aplicación backend completa construida con FastAPI, SQLModel y PostgreSQL
para gestionar inventario de vehículos, transacciones de ventas, personas y países.

STACK TECNOLÓGICO:
- FastAPI 0.120.4        → Framework web asincrónico
- SQLModel 0.0.27        → ORM + Validación de datos
- PostgreSQL 12+         → Base de datos relacional
- Uvicorn 0.38.0         → Servidor ASGI
- Pydantic 2.5+          → Validación de datos
- Python-jose + Passlib  → Autenticación JWT
- Pytest 8.4.2           → Testing

ESTRUCTURA DEL PROYECTO:

/app/                           # Módulo principal de la aplicación
├── __init__.py
├── database.py                 # Configuración de BD y sesiones
├── models.py                   # Modelos SQLModel (Autos, Ventas, Usuarios)
├── repositories.py             # Repositorios de datos (Autos, Ventas)
├── routers_autos.py            # Rutas API para vehículos
├── routers_ventas.py           # Rutas API para ventas
└── utils.py                    # Funciones auxiliares y validaciones

/root/                          # Archivos de aplicación (nivel raíz)
├── main.py                     # Punto de entrada + configuración app
├── config.py                   # Configuración global (constantes, CORS, etc)
│
├── auth.py                     # Utilidades de autenticación JWT
├── auth_router.py              # Rutas de autenticación (login/register)
│
├── models.py                   # Modelos adicionales (Persona, Pais, User)
├── database.py                 # Configuración alternativa de BD (legacy)
├── repository.py               # Repositorio para Persona/Pais
│
├── paises.py                   # Router para gestión de países
├── personas.py                 # Router para gestión de personas
├── objects.py                  # Router para objetos genéricos
│
├── protected_endpoints.py       # Ejemplos de endpoints protegidos
├── test_crud_direct.py         # Tests de CRUD
│
├── requirements.txt            # Dependencias Python
├── .env.example                # Variables de entorno de ejemplo
└── config.py                   # Configuración de la aplicación

/tests/                         # Tests unitarios
├── __init__.py
└── test_endpoints.py           # Tests de endpoints

/Trabajo Practico/              # Documentación de trabajo práctico
└── TP_Ventas_Autos.md          # Especificación del proyecto

DOCKER:
├── Dockerfile.postgres         # Image personalizada de PostgreSQL
└── docker-compose.yml          # Configuración multi-contenedor

DOCUMENTACIÓN:
├── README.md                   # Documentación principal del proyecto
├── README_API.md               # Referencia completa de API
├── README-Docker-PostgreSQL.md # Guía de configuración Docker
├── AUTH_EXAMPLES.md            # Ejemplos de autenticación JWT
├── DEVELOPMENT.md              # Guía de desarrollo
└── PROJECT_OVERVIEW.md         # Este archivo


CARACTERÍSTICAS PRINCIPALES:

1. GESTIÓN DE VEHÍCULOS (Autos)
   ✅ CRUD completo (POST, GET, PUT, DELETE)
   ✅ Generación automática de VIN (17 caracteres)
   ✅ Búsqueda por marca, modelo, año
   ✅ Paginación con skip/limit
   ✅ Relaciones con ventas
   
   Endpoints:
   - POST   /api/v1/autos/           → Crear vehículo
   - POST   /api/v1/autos/batch/     → Crear múltiples vehículos
   - GET    /api/v1/autos/           → Listar vehículos
   - GET    /api/v1/autos/{id}       → Obtener vehículo
   - GET    /api/v1/autos/chasis/... → Obtener por VIN
   - PUT    /api/v1/autos/{id}       → Actualizar vehículo
   - DELETE /api/v1/autos/{id}       → Eliminar vehículo

2. GESTIÓN DE VENTAS
   ✅ CRUD completo
   ✅ Validación de vehículos existentes
   ✅ Relaciones con compradores
   ✅ Búsqueda por comprador, vehículo, fecha
   ✅ Cálculos de estadísticas
   
   Endpoints:
   - POST   /api/v1/ventas/          → Crear venta
   - POST   /api/v1/ventas/batch/    → Crear múltiples ventas
   - GET    /api/v1/ventas/          → Listar ventas
   - GET    /api/v1/ventas/{id}      → Obtener venta
   - GET    /api/v1/ventas/auto/{id} → Obtener ventas por auto
   - GET    /api/v1/ventas/comprador/... → Obtener por comprador
   - PUT    /api/v1/ventas/{id}      → Actualizar venta
   - DELETE /api/v1/ventas/{id}      → Eliminar venta

3. AUTENTICACIÓN Y SEGURIDAD
   ✅ Sistema JWT completo
   ✅ Registro de usuarios
   ✅ Login con tokens
   ✅ Protección de endpoints
   ✅ Validación de contraseñas
   
   Endpoints:
   - POST /auth/register  → Registrar nuevo usuario
   - POST /auth/login     → Login y obtener token
   - POST /auth/refresh   → Renovar token (si aplica)
   - GET  /auth/me        → Obtener perfil (protegido)

4. GESTIÓN DE PAÍSES Y PERSONAS
   ✅ CRUD para países
   ✅ CRUD para personas
   ✅ Relaciones entre personas y países
   ✅ Validaciones de edad y datos
   
   Endpoints:
   - POST   /paises/         → Crear país
   - GET    /paises/         → Listar países
   - GET    /paises/{id}     → Obtener país
   - PUT    /paises/{id}     → Actualizar país
   - DELETE /paises/{id}     → Eliminar país
   
   - POST   /personas/       → Crear persona
   - GET    /personas/       → Listar personas
   - GET    /personas/{id}   → Obtener persona
   - PUT    /personas/{id}   → Actualizar persona
   - DELETE /personas/{id}   → Eliminar persona

5. GESTIÓN DE OBJETOS GENÉRICOS
   ✅ API simple para objetos con datos personalizados
   ✅ Almacenamiento en memoria (demostración)
   ✅ Flexibilidad en estructura de datos
   
   Endpoints:
   - GET    /objects     → Listar objetos
   - POST   /objects     → Crear objeto
   - GET    /objects/{id}    → Obtener objeto
   - PUT    /objects/{id}    → Actualizar objeto
   - DELETE /objects/{id}    → Eliminar objeto


CONFIGURACIÓN Y VARIABLES DE ENTORNO:

.env:
  DATABASE_URL=postgresql://user:pass@host:port/database
  DEBUG=false
  PORT=8000
  HOST=0.0.0.0
  SECRET_KEY=tu-clave-secreta
  ALGORITHM=HS256

Valores por defecto en config.py si no están en .env


DOCUMENTACIÓN INTERACTIVA:

- Swagger UI:  http://localhost:8000/docs
- ReDoc:       http://localhost:8000/redoc
- OpenAPI:     http://localhost:8000/openapi.json


INSTALACIÓN Y EJECUCIÓN:

1. Instalación de dependencias:
   pip install -r requirements.txt

2. Configuración de base de datos:
   - Crear archivo .env con DATABASE_URL
   - O usar Docker Compose para PostgreSQL

3. Ejecutar aplicación:
   uvicorn main:app --reload

4. Con Docker:
   docker-compose up -d postgres_utn
   (Luego correr la app localmente)

5. Tests:
   pytest tests/


PATRONES DE DISEÑO:

- Repository Pattern: Abstracción de acceso a datos
- Dependency Injection: DI nativo de FastAPI
- Model Validation: Pydantic para validación
- Async/Await: Programación asincrónica
- CORS Middleware: Comunicación con frontend


CONVENCIONES DE CÓDIGO:

Docstrings:
- Módulo: Descripción general al inicio del archivo
- Función: Descripción, Args, Returns, Raises
- Clase: Descripción y propósito

Imports:
1. Librerías estándar
2. Librerías externas
3. Imports locales

Nombres:
- Funciones/variables: snake_case
- Clases/modelos: PascalCase
- Constantes: UPPER_SNAKE_CASE


MANTENIMIENTO Y NOTAS:

- database.py (raíz) es versión simplificada, usar app/database.py
- models.py tiene tanto Persona/Pais como User (dependiendo necesidades)
- objects.py usa almacenamiento en memoria, solo para demostración
- Para producción, migrar objects.py a base de datos
- Cambiar SECRET_KEY en auth.py para producción
- Configurar CORS_ORIGINS en config.py según frontend


PRÓXIMAS CARACTERÍSTICAS RECOMENDADAS:

- [ ] Autenticación OAuth2
- [ ] Rate limiting
- [ ] Logging estructurado
- [ ] Caché con Redis
- [ ] Swagger con ejemplos mejorados
- [ ] GraphQL opcional
- [ ] Integración con Celery para tasks
- [ ] Migrations automáticas


REFERENCIAS Y DOCUMENTACIÓN:

- FastAPI Docs:    https://fastapi.tiangolo.com
- SQLModel Docs:   https://sqlmodel.tiangolo.com
- PostgreSQL Docs: https://postgresql.org/docs
- JWT:             https://tools.ietf.org/html/rfc7519
- OpenAPI Spec:    https://openapis.org

================================================================================
Última actualización: Noviembre 2024
Versión: 1.0.0
Estado: Producción Listo
================================================================================
"""
