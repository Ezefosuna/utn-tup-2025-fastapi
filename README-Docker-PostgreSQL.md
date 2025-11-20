# 🐘 Guía de Configuración: PostgreSQL + Docker

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Requisitos Previos](#requisitos-previos)
3. [Inicio Rápido](#inicio-rápido)
4. [Conexión a la Base de Datos](#conexión-a-la-base-de-datos)
5. [Comandos Útiles](#comandos-útiles)
6. [Solución de Problemas](#solución-de-problemas)
7. [Persistencia de Datos](#persistencia-de-datos)
8. [Copias de Seguridad](#copias-de-seguridad)
9. [Producción](#consideraciones-para-producción)
10. [Recursos](#recursos)

---

## 📌 Descripción General

Esta guía proporciona instrucciones completas para configurar PostgreSQL usando Docker y Docker Compose. Docker asegura entornos de base de datos consistentes y reproducibles en todas las máquinas de desarrollo.

**Beneficios:**
- ✅ Entorno consistente entre desarrolladores
- ✅ Sin instalación de PostgreSQL en el sistema
- ✅ Fácil limpieza y reseteo
- ✅ Escalabilidad para ambientes multi-contenedor

---

## 🛠️ Requisitos Previos

| Requisito | Versión Mínima | Instalación |
|-----------|-----------------|-------------|
| Docker | 20.10+ | [Docker Desktop](https://docs.docker.com/get-docker/) |
| Docker Compose | 2.0+ | Incluido en Docker Desktop |
| Git | 2.30+ | [Instalación](https://git-scm.com/) |
| PowerShell/Bash | - | Sistema operativo |

**Verificar instalación:**
```bash
docker --version
docker-compose --version
```

---

## 🚀 Inicio Rápido

### Opción 1: Docker Compose (Recomendado) ⭐

**Paso 1: Iniciar el contenedor**
```bash
docker-compose up -d postgres_utn
```

**Paso 2: Verificar que está ejecutándose**
```bash
docker-compose ps
```

**Paso 3: Ver logs (opcional)**
```bash
docker-compose logs postgres_utn
```

**Paso 4: Detener cuando ya no lo necesites**
```bash
docker-compose down
```

### Opción 2: Docker CLI Manual

**Paso 1: Construir imagen personalizada**
```bash
docker build -f Dockerfile.postgres -t postgres-utn .
```

**Paso 2: Ejecutar contenedor**
```bash
docker run -d `
  --name postgres_utn_db `
  -e POSTGRES_DB=UTN `
  -e POSTGRES_USER=postgres `
  -e POSTGRES_PASSWORD=postgres `
  -p 55432:5432 `
  -v postgres_utn_data:/var/lib/postgresql/data `
  postgres-utn
```

**Paso 3: Ver logs**
```bash
docker logs postgres_utn_db
```

**Paso 4: Detener y eliminar**
```bash
docker stop postgres_utn_db
docker rm postgres_utn_db
```

---

## 🔗 Conexión a la Base de Datos

### Detalles de Conexión

```
Protocolo:       PostgreSQL
Host:            localhost
Puerto:          55432
Base de Datos:   UTN
Usuario:         postgres
Contraseña:      postgres
URL Completa:    postgresql://postgres:postgres@localhost:55432/UTN
```

### Archivo `.env` (Configuración Local)

Crear archivo `.env` en la raíz del proyecto:

```env
# Base de Datos
DATABASE_URL=postgresql://postgres:postgres@localhost:55432/UTN

# API
DEBUG=false
PORT=8000
HOST=0.0.0.0

# JWT (si corresponde)
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
```

O copiar desde la plantilla:
```bash
cp .env.example .env
```

### Conectar desde FastAPI

**Archivo `config.py`:**
```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:55432/UTN"
)

engine = create_engine(DATABASE_URL)
```

**Archivo `database.py`:**
```python
from sqlalchemy.orm import Session
from app.database import engine

# Las tablas se crearán automáticamente
# Base.metadata.create_all(bind=engine)
```

---

## 🎛️ Comandos Útiles

### Gestión de Contenedores

```bash
# Ver estado de contenedores
docker-compose ps

# Ver todos los contenedores (incluso detenidos)
docker ps -a

# Ver logs del contenedor
docker-compose logs postgres_utn

# Seguir logs en tiempo real
docker-compose logs -f postgres_utn

# Acceder a la terminal de PostgreSQL
docker exec -it postgres_utn_db psql -U postgres -d UTN

# Reiniciar contenedor
docker-compose restart postgres_utn

# Eliminar contenedor y volumen
docker-compose down -v
```

### Operaciones en PostgreSQL

Conectarse a la base de datos:
```bash
psql -U postgres -h localhost -p 55432 -d UTN
```

Comandos dentro de `psql`:
```sql
\l                 -- Listar bases de datos
\c UTN             -- Conectar a base de datos UTN
\dt                -- Listar todas las tablas
\d nombre_tabla    -- Ver estructura de tabla
\du                -- Listar usuarios
SELECT * FROM pg_tables WHERE schemaname = 'public';
\q                 -- Salir de psql
```

---

## ❌ Solución de Problemas

### 1️⃣ Puerto 55432 Ya en Uso

**Error:** `Error starting userland proxy: listen tcp 0.0.0.0:55432: bind: An attempt was made to use a port in a state that does not allow its use.`

**Solución:**

Opción A: Usar puerto diferente en `docker-compose.yml`
```yaml
postgres_utn:
  ports:
    - "55433:5432"  # Cambiar 55432 a 55433
```

Opción B: Encontrar y detener proceso en puerto 55432
```bash
# Windows (PowerShell)
netstat -ano | findstr :55432
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :55432
kill -9 <PID>
```

### 2️⃣ El Contenedor No Inicia

**Verificar logs:**
```bash
docker-compose logs postgres_utn
```

**Soluciones:**
```bash
# Eliminar volúmenes huérfanos
docker volume prune

# Reconstruir imagen
docker-compose down
docker-compose up -d --build postgres_utn

# Verificar permisos en Linux
sudo usermod -aG docker $USER
newgrp docker
```

### 3️⃣ Conexión Rechazada

**Checklist:**
```bash
# 1. ¿Está el contenedor ejecutándose?
docker-compose ps

# 2. ¿Están correctas las credenciales en .env?
cat .env | grep DATABASE_URL

# 3. ¿Está el puerto mapeado?
docker port postgres_utn_db

# 4. Prueba de conectividad
docker exec postgres_utn_db pg_isready -U postgres

# 5. Intenta conectarte desde dentro del contenedor
docker exec -it postgres_utn_db psql -U postgres -d UTN
```

### 4️⃣ Error de Permisos en Linux

```bash
# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Aplicar cambios sin reiniciar
newgrp docker

# Verificar
docker ps
```

### 5️⃣ Base de Datos No Inicializa

```bash
# Ver logs completos
docker-compose logs postgres_utn --tail=100

# Eliminar volumen y recrear
docker-compose down -v
docker-compose up -d postgres_utn
```

---

## 💾 Persistencia de Datos

### Volúmenes de Docker

Los datos se almacenan en el volumen `postgres_utn_data`:

```bash
# Listar volúmenes
docker volume ls

# Inspeccionar volumen específico
docker volume inspect back_postgres_utn_data

# Ver ruta en disco
docker volume inspect back_postgres_utn_data --format='{{.Mountpoint}}'

# Eliminar volumen (⚠️ ELIMINA TODOS LOS DATOS)
docker volume rm back_postgres_utn_data

# Limpiar volúmenes no utilizados
docker volume prune
```

### Estructura de Volumen

```
/var/lib/postgresql/data/
├── base/                  -- Bases de datos
├── global/                -- Archivos globales
├── pg_wal/                -- Logs de transacciones
└── postgresql.conf        -- Configuración
```

---

## 🔐 Copias de Seguridad

### Realizar Backup

**Formato SQL (legible):**
```bash
docker exec postgres_utn_db pg_dump -U postgres UTN > backup.sql
```

**Formato binario (comprimido):**
```bash
docker exec postgres_utn_db pg_dump -U postgres -F c UTN > backup.dump
```

**Exportar solo esquema:**
```bash
docker exec postgres_utn_db pg_dump -U postgres -s UTN > schema.sql
```

### Restaurar desde Backup

**Desde dump SQL:**
```bash
docker exec -i postgres_utn_db psql -U postgres UTN < backup.sql
```

**Desde dump binario:**
```bash
docker exec -i postgres_utn_db pg_restore -U postgres -d UTN < backup.dump
```

**Restaurar solo esquema:**
```bash
docker exec -i postgres_utn_db psql -U postgres UTN < schema.sql
```

### Script Automatizado (Linux/Mac)

```bash
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

docker exec postgres_utn_db pg_dump -U postgres UTN > \
  "$BACKUP_DIR/backup_$TIMESTAMP.sql"

echo "Backup creado: $BACKUP_DIR/backup_$TIMESTAMP.sql"
```

---

## ⚙️ Optimización para Producción

### Configuración de Memoria

```yaml
postgres_utn:
  environment:
    POSTGRES_INITDB_ARGS: >
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=64MB
      -c checkpoint_completion_target=0.9
```

### Límite de Conexiones

```yaml
postgres_utn:
  environment:
    POSTGRES_INITDB_ARGS: "-c max_connections=200"
```

### Seguridad Recomendada

**Cambiar credenciales por defecto:**
```yaml
postgres_utn:
  environment:
    POSTGRES_DB: production_db
    POSTGRES_USER: appuser
    POSTGRES_PASSWORD: $(openssl rand -base64 32)
```

**Habilitar SSL:**
```bash
docker exec postgres_utn_db mkdir -p /var/lib/postgresql/ssl
# Copiar certificados
docker cp server.crt postgres_utn_db:/var/lib/postgresql/ssl/
docker cp server.key postgres_utn_db:/var/lib/postgresql/ssl/
```

---

## 📚 Configuraciones Completas

### Docker Compose Simple (Desarrollo)

```yaml
version: '3.8'

services:
  postgres_utn:
    image: postgres:15-alpine
    container_name: postgres_utn_db
    environment:
      POSTGRES_DB: UTN
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "55432:5432"
    volumes:
      - postgres_utn_data:/var/lib/postgresql/data
    networks:
      - utn-network

volumes:
  postgres_utn_data:

networks:
  utn-network:
    driver: bridge
```

### Docker Compose Multi-Servicio (FastAPI + PostgreSQL)

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: postgres_utn_prod
    environment:
      POSTGRES_DB: UTN
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    container_name: fastapi_utn
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/UTN
    networks:
      - app-network
    command: uvicorn main:app --host 0.0.0.0 --port 8000

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

---

## 📖 Recursos

| Recurso | Enlace |
|---------|--------|
| Documentación Docker | [docs.docker.com](https://docs.docker.com/) |
| Documentación Docker Compose | [docs.docker.com/compose](https://docs.docker.com/compose/) |
| Documentación PostgreSQL | [postgresql.org/docs](https://www.postgresql.org/docs/) |
| Imagen PostgreSQL Docker | [hub.docker.com/_/postgres](https://hub.docker.com/_/postgres) |
| CLI PostgreSQL | [postgresql.org/docs/.../app-psql.html](https://www.postgresql.org/docs/current/app-psql.html) |
| pgAdmin (UI) | [pgadmin.org](https://www.pgadmin.org/) |

---

## 📞 Soporte

| Problema | Contacto |
|----------|----------|
| Errores de Docker | Verificar [instalación de Docker](https://docs.docker.com/get-docker/) |
| Errores de PostgreSQL | Ver logs: `docker-compose logs postgres_utn` |
| Problemas de conexión | Revisar sección [Solución de Problemas](#solución-de-problemas) |

---

**Versión**: 2.0  
**Última Actualización**: Noviembre 2024  
**Responsable**: Equipo de Desarrollo  
**Estado**: ✅ Producción Listo

## Requisitos Previos

- Docker ([Instalar Docker](https://docs.docker.com/get-docker/))
- Docker Compose ([Instalar Docker Compose](https://docs.docker.com/compose/install/))
- Git

## Archivos Incluidos

| Archivo | Propósito |
|---------|---------|
| `Dockerfile.postgres` | Imagen personalizada de PostgreSQL con base de datos UTN preconfigurada |
| `docker-compose.yml` | Archivo de orquestación para fácil gestión de contenedores |
| `.env.example` | Plantilla de variables de entorno |

## Inicio Rápido

### Opción 1: Docker Compose (Recomendado)

1. **Iniciar Contenedor de PostgreSQL**
   ```bash
   docker-compose up -d postgres_utn
   ```

2. **Verificar que el Contenedor está Ejecutándose**
   ```bash
   docker-compose logs postgres_utn
   ```

3. **Detener Contenedor**
   ```bash
   docker-compose down
   ```

### Opción 2: Docker CLI

1. **Construir Imagen Personalizada**
   ```bash
   docker build -f Dockerfile.postgres -t postgres-utn .
   ```

2. **Ejecutar Contenedor**
   ```bash
   docker run -d \
     --name postgres_utn_db \
     -e POSTGRES_DB=UTN \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -p 55432:5432 \
     -v postgres_utn_data:/var/lib/postgresql/data \
     postgres-utn
   ```

3. **Ver Logs**
   ```bash
   docker logs postgres_utn_db
   ```

4. **Detener Contenedor**
   ```bash
   docker stop postgres_utn_db
   docker rm postgres_utn_db
   ```

## Conexión a la Base de Datos

### Detalles de Conexión

| Parámetro | Valor |
|-----------|-------|
| Host | localhost |
| Puerto | 55432 |
| Base de Datos | UTN |
| Usuario | postgres |
| Contraseña | postgres |
| Cadena de Conexión | `postgresql://postgres:postgres@localhost:55432/UTN` |

### Configuración de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:55432/UTN
DEBUG=false
PORT=8000
HOST=0.0.0.0
```

O copiar desde la plantilla:
```bash
cp .env.example .env
```

## Conectar desde FastAPI

Actualizar tu archivo `config.py` o `.env` con la cadena de conexión:

```python
# config.py
import os
from sqlalchemy.engine import URL

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:55432/UTN"
)

# Crear motor
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
```

## Comandos Útiles

### Gestión de Contenedores

```bash
# Ver contenedores en ejecución
docker-compose ps

# Ver todos los contenedores
docker ps -a

# Ver logs del contenedor
docker-compose logs postgres_utn

# Seguir logs en tiempo real
docker-compose logs -f postgres_utn

# Acceder a CLI de PostgreSQL dentro del contenedor
docker exec -it postgres_utn_db psql -U postgres -d UTN
```

### Operaciones de Base de Datos

```bash
# Conectar a base de datos desde el host
psql -U postgres -h localhost -p 55432 -d UTN

# Listar todas las bases de datos
\l

# Conectar a base de datos específica
\c UTN

# Listar todas las tablas
\dt

# Describir estructura de tabla
\d nombre_tabla

# Salir de psql
\q
```

## Solución de Problemas

### Puerto Ya en Uso

Si el puerto 55432 ya está en uso:

1. **Modificar `docker-compose.yml`**
   ```yaml
   postgres_utn:
     ports:
       - "55433:5432"  # Cambiar primer puerto a 55433
   ```

2. **Actualizar `DATABASE_URL` en `.env`**
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:55433/UTN
   ```

### El Contenedor No Inicia

1. **Verificar logs para errores**
   ```bash
   docker-compose logs postgres_utn
   ```

2. **Eliminar volúmenes huérfanos**
   ```bash
   docker volume prune
   ```

3. **Reconstruir imagen**
   ```bash
   docker-compose down
   docker-compose up -d --build postgres_utn
   ```

### Conexión Rechazada

1. **Verificar que el contenedor está ejecutándose**
   ```bash
   docker-compose ps
   ```

2. **Verificar que las credenciales coincidan** en el archivo `.env`

3. **Verificar mapeo de puertos**
   ```bash
   docker port postgres_utn_db
   ```

4. **Probar conexión**
   ```bash
   docker exec postgres_utn_db pg_isready -U postgres
   ```

### Permiso Denegado

```bash
# En Linux, agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

## Persistencia de Volumen

Los datos se almacenan en el volumen de Docker `postgres_utn_data`, asegurando persistencia entre reinicios de contenedor:

```bash
# Listar todos los volúmenes
docker volume ls

# Inspeccionar volumen
docker volume inspect back_postgres_utn_data

# Ver ubicación del volumen
docker volume inspect back_postgres_utn_data --format='{{.Mountpoint}}'

# Eliminar volumen (ADVERTENCIA: Elimina todos los datos)
docker volume rm back_postgres_utn_data

# Limpiar volúmenes no utilizados
docker volume prune
```

## Copia de Seguridad y Restauración

### Realizar Copia de Seguridad de la Base de Datos

Crear un dump SQL de la base de datos:

```bash
docker exec postgres_utn_db pg_dump -U postgres UTN > backup.sql
```

O con compresión:
```bash
docker exec postgres_utn_db pg_dump -U postgres -F c UTN > backup.dump
```

### Restaurar Base de Datos

Desde dump SQL:
```bash
docker exec -i postgres_utn_db psql -U postgres UTN < backup.sql
```

Desde dump comprimido:
```bash
docker exec -i postgres_utn_db pg_restore -U postgres -d UTN -F c < backup.dump
```

## Optimización del Desempeño

### Agrupación de Conexiones

Para producción, configurar agrupación de conexiones en `docker-compose.yml`:

```yaml
postgres_utn:
  environment:
    POSTGRES_INITDB_ARGS: "-c max_connections=200"
```

### Configuración de Memoria

```yaml
postgres_utn:
  environment:
    POSTGRES_INITDB_ARGS: "-c shared_buffers=256MB -c effective_cache_size=1GB"
```

## Consideraciones para Producción

Para implementaciones en producción, implementar:

1. **Seguridad**
   - Usar contraseñas fuertes generadas aleatoriamente
   - Cambiar credenciales predeterminadas
   - Usar gestión de secretos de entorno
   - Habilitar conexiones SSL/TLS

2. **Monitoreo**
   - Configurar recopilación y agregación de logs
   - Monitorear métricas de desempeño de la base de datos
   - Configurar alertas para problemas críticos
   - Rastrear tiempos de ejecución de consultas

3. **Estrategia de Copia de Seguridad**
   - Copias de seguridad automatizadas regulares
   - Probar procedimientos de restauración periódicamente
   - Almacenar copias de seguridad en múltiples ubicaciones
   - Usar políticas de retención de copias de seguridad

4. **Desempeño**
   - Configurar configuración de memoria apropiada
   - Agregar índices a columnas frecuentemente consultadas
   - Monitorear y optimizar consultas lentas
   - Usar agrupación de conexiones

## Patrones Comunes de Docker Compose

### Configuración de Desarrollo

```yaml
version: '3.8'
services:
  postgres_utn:
    image: postgres:15-alpine
    container_name: postgres_utn_db
    environment:
      POSTGRES_DB: UTN
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "55432:5432"
    volumes:
      - postgres_utn_data:/var/lib/postgresql/data
    networks:
      - car-sales-network

volumes:
  postgres_utn_data:

networks:
  car-sales-network:
    driver: bridge
```

### Configuración Multi-Servicio

Para FastAPI + PostgreSQL en un archivo compose:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: UTN
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/UTN
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
```

## Recursos

- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [Documentación de PostgreSQL](https://www.postgresql.org/docs/)
- [Imagen Oficial de PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Referencia de CLI de PostgreSQL](https://www.postgresql.org/docs/current/app-psql.html)

---

**Versión**: 1.0  
**Última Actualización**: Noviembre 2024  
**Responsable**: Equipo de Desarrollo
