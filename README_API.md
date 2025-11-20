# 📡 Referencia Completa de API REST

## 🌐 Configuración Base

**URL Base de Producción:**
```
http://localhost:8000/api/v1
```

**Documentación Interactiva:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🔐 Autenticación

### Tipos de Autenticación Soportados

1. **Sin Autenticación** (endpoints públicos)
2. **JWT Bearer Token** (endpoints protegidos)
   ```
   Authorization: Bearer <access_token>
   ```

Para más detalles sobre autenticación, ver [AUTH_EXAMPLES.md](./AUTH_EXAMPLES.md)

---

## 🚗 Endpoints de Vehículos (Autos)

### 1. Crear un Vehículo

```http
POST /autos/
Content-Type: application/json

{
  "marca": "Toyota",
  "modelo": "Corolla",
  "año": 2023
}
```

**Respuesta 201 Created:**
```json
{
  "id": 1,
  "marca": "Toyota",
  "modelo": "Corolla",
  "año": 2023,
  "numero_chasis": "1HGBH41JXMN109186"
}
```

**Validaciones:**
- `marca`: String no vacío (máx 50 caracteres)
- `modelo`: String no vacío (máx 50 caracteres)
- `año`: Entre 1900 y año actual

---

### 2. Crear Múltiples Vehículos (Batch)

```http
POST /autos/batch/
Content-Type: application/json

[
  {"marca": "Toyota", "modelo": "Corolla", "año": 2023},
  {"marca": "Ford", "modelo": "Focus", "año": 2022},
  {"marca": "Honda", "modelo": "Civic", "año": 2024}
]
```

**Respuesta 201 Created:**
```json
[
  {"id": 1, "marca": "Toyota", "modelo": "Corolla", "año": 2023, "numero_chasis": "1HGBH41JXMN109186"},
  {"id": 2, "marca": "Ford", "modelo": "Focus", "año": 2022, "numero_chasis": "2G1FB1E30D1234567"},
  {"id": 3, "marca": "Honda", "modelo": "Civic", "año": 2024, "numero_chasis": "3G1BH52K03S123456"}
]
```

---

### 3. Listar Vehículos

```http
GET /autos/?skip=0&limit=10&marca=Toyota
```

**Parámetros de Consulta:**

| Parámetro | Tipo | Valor por Defecto | Descripción |
|-----------|------|------------------|-------------|
| `skip` | int | 0 | Registros a omitir (paginación) |
| `limit` | int | 10 | Registros a devolver |
| `marca` | string | null | Filtrar por marca (búsqueda parcial) |
| `modelo` | string | null | Filtrar por modelo (búsqueda parcial) |

**Ejemplo con filtros:**
```http
GET /autos/?marca=Toyota&modelo=Corolla&limit=5
```

**Respuesta 200 OK:**
```json
[
  {
    "id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "1HGBH41JXMN109186"
  },
  {
    "id": 2,
    "marca": "Toyota",
    "modelo": "Camry",
    "año": 2024,
    "numero_chasis": "2T1BR1E30DC123456"
  }
]
```

---

### 4. Obtener Vehículo por ID

```http
GET /autos/1
```

**Respuesta 200 OK:**
```json
{
  "id": 1,
  "marca": "Toyota",
  "modelo": "Corolla",
  "año": 2023,
  "numero_chasis": "1HGBH41JXMN109186"
}
```

**Posibles errores:**
- 404 Not Found: Si el vehículo no existe

---

### 5. Obtener Vehículo por Número de Chasis (VIN)

```http
GET /autos/chasis/1HGBH41JXMN109186
```

**Respuesta 200 OK:**
```json
{
  "id": 1,
  "marca": "Toyota",
  "modelo": "Corolla",
  "año": 2023,
  "numero_chasis": "1HGBH41JXMN109186"
}
```

---

### 6. Actualizar Vehículo

```http
PUT /autos/1
Content-Type: application/json

{
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2024
}
```

**Respuesta 200 OK:**
```json
{
  "id": 1,
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2024,
  "numero_chasis": "1HGBH41JXMN109186"
}
```

**Nota:** El número de chasis no se puede modificar.

---

### 7. Eliminar Vehículo

```http
DELETE /autos/1
```

**Respuesta 204 No Content** (sin cuerpo)

**Posibles errores:**
- 404 Not Found: Si el vehículo no existe
- 409 Conflict: Si el vehículo tiene ventas asociadas

---

## 💰 Endpoints de Ventas

### 1. Crear una Venta

```http
POST /ventas/
Content-Type: application/json

{
  "auto_id": 1,
  "nombre_comprador": "Juan Pérez",
  "precio": 25000.00,
  "fecha_venta": "2024-11-19T10:30:00"
}
```

**Respuesta 201 Created:**
```json
{
  "id": 1,
  "auto_id": 1,
  "nombre_comprador": "Juan Pérez",
  "precio": 25000.00,
  "fecha_venta": "2024-11-19T10:30:00",
  "auto": {
    "id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "1HGBH41JXMN109186"
  }
}
```

**Validaciones:**
- `auto_id`: Debe referenciar un vehículo existente
- `nombre_comprador`: String no vacío (máx 100 caracteres)
- `precio`: Mayor a 0
- `fecha_venta`: No puede ser en el futuro

---

### 2. Crear Múltiples Ventas (Batch)

```http
POST /ventas/batch/
Content-Type: application/json

[
  {
    "auto_id": 1,
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "fecha_venta": "2024-11-19T10:30:00"
  },
  {
    "auto_id": 2,
    "nombre_comprador": "María García",
    "precio": 30000.00,
    "fecha_venta": "2024-11-18T15:00:00"
  }
]
```

**Respuesta 201 Created:** Array de ventas creadas

---

### 3. Listar Ventas

```http
GET /ventas/?skip=0&limit=10
```

**Parámetros de Consulta:**

| Parámetro | Tipo | Valor por Defecto |
|-----------|------|------------------|
| `skip` | int | 0 |
| `limit` | int | 10 |

**Respuesta 200 OK:**
```json
[
  {
    "id": 1,
    "auto_id": 1,
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "fecha_venta": "2024-11-19T10:30:00",
    "auto": {
      "id": 1,
      "marca": "Toyota",
      "modelo": "Corolla",
      "año": 2023,
      "numero_chasis": "1HGBH41JXMN109186"
    }
  }
]
```

---

### 4. Obtener Venta por ID

```http
GET /ventas/1
```

**Respuesta 200 OK:**
```json
{
  "id": 1,
  "auto_id": 1,
  "nombre_comprador": "Juan Pérez",
  "precio": 25000.00,
  "fecha_venta": "2024-11-19T10:30:00",
  "auto": {
    "id": 1,
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023,
    "numero_chasis": "1HGBH41JXMN109186"
  }
}
```

---

### 5. Obtener Ventas por Vehículo

```http
GET /ventas/auto/1
```

**Respuesta 200 OK:** Array de ventas del vehículo especificado

---

### 6. Obtener Ventas por Nombre del Comprador

```http
GET /ventas/comprador/Juan Pérez
```

**Respuesta 200 OK:** Array de ventas del comprador especificado

---

### 7. Actualizar Venta

```http
PUT /ventas/1
Content-Type: application/json

{
  "nombre_comprador": "Juan Pérez García",
  "precio": 26000.00,
  "fecha_venta": "2024-11-20T11:00:00"
}
```

**Respuesta 200 OK:** Venta actualizada

---

### 8. Eliminar Venta

```http
DELETE /ventas/1
```

**Respuesta 204 No Content** (sin cuerpo)

---

## ❌ Respuestas de Error

### 400 - Solicitud Inválida

```json
{
  "detail": "El año debe estar entre 1900 y el año actual"
}
```

### 404 - No Encontrado

```json
{
  "detail": "Vehículo no encontrado con ID: 999"
}
```

### 422 - Validación Fallida

```json
{
  "detail": [
    {
      "loc": ["body", "año"],
      "msg": "asegurate de que este valor es menor o igual a 2024",
      "type": "value_error"
    }
  ]
}
```

### 409 - Conflicto

```json
{
  "detail": "No se puede eliminar vehículo que tiene ventas asociadas"
}
```

### 500 - Error del Servidor

```json
{
  "detail": "Error interno del servidor"
}
```

---

## 📊 Tabla de Códigos de Estado

| Código | Descripción | Cuándo Ocurre |
|--------|-------------|---------------|
| 200 | OK | Solicitud exitosa (GET, PUT) |
| 201 | Creado | Recurso creado exitosamente (POST) |
| 204 | Sin Contenido | Solicitud exitosa sin retornar datos (DELETE) |
| 400 | Solicitud Inválida | Validación fallida, datos inválidos |
| 401 | No Autorizado | Token faltante o inválido |
| 403 | Prohibido | Permisos insuficientes |
| 404 | No Encontrado | Recurso no existe |
| 409 | Conflicto | Operación genera conflicto (ej: FK constraint) |
| 422 | No Procesable | Esquema JSON inválido |
| 500 | Error del Servidor | Error interno no esperado |

---

## 🔄 Paginación

Todos los endpoints de listado soportan paginación con `skip` y `limit`:

**Ejemplo:**
```http
GET /autos/?skip=0&limit=5
```

- `skip=0, limit=5` → Items 1-5
- `skip=5, limit=5` → Items 6-10
- `skip=10, limit=5` → Items 11-15

**Respuesta:** Array de hasta `limit` elementos

---

## 🔎 Filtrado

### Filtrado en Vehículos

```http
GET /autos/?marca=Toyota&modelo=Corolla&limit=10
```

- Búsqueda parcial (case-insensitive)
- Combinable con otros parámetros
- Utiliza índices de BD para mejor performance

### Ejemplo Real:

```bash
# Buscar todos los Toyotas
GET /autos/?marca=Toyota

# Buscar Corollas de 2023
GET /autos/?modelo=Corolla&año=2023

# Paginar resultados
GET /autos/?skip=10&limit=5
```

---

## 📝 Ejemplos de Uso Completo

### Flujo Completo: Crear Vehículo y Venta

```bash
# 1. Crear vehículo
curl -X POST http://localhost:8000/autos/ \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Toyota",
    "modelo": "Corolla",
    "año": 2023
  }'
# Respuesta: {"id": 1, "numero_chasis": "1HGBH41JXMN109186", ...}

# 2. Crear venta del vehículo
curl -X POST http://localhost:8000/ventas/ \
  -H "Content-Type: application/json" \
  -d '{
    "auto_id": 1,
    "nombre_comprador": "Juan Pérez",
    "precio": 25000.00,
    "fecha_venta": "2024-11-19T10:30:00"
  }'
# Respuesta: {"id": 1, "auto_id": 1, ...}

# 3. Listar todas las ventas
curl -X GET http://localhost:8000/ventas/

# 4. Obtener ventas de Juan
curl -X GET http://localhost:8000/ventas/comprador/Juan Pérez
```

---

## ⚙️ Especificación de Generación de VIN

El número de chasis (VIN - Vehicle Identification Number) se genera automáticamente:

- **Formato**: 17 caracteres
- **Caracteres válidos**: 0-9, A-Z (sin I, O, Q)
- **Generación**: Aleatoria única por vehículo
- **Inmutable**: No puede ser cambiada después de crear

**Ejemplo VIN:**
```
1HGBH41JXMN109186
```

---

## 🧪 Pruebas Usando cURL

### Prueba 1: Crear Vehículo
```bash
curl -X POST "http://localhost:8000/autos/" \
  -H "Content-Type: application/json" \
  -d '{"marca":"Toyota","modelo":"Corolla","año":2023}'
```

### Prueba 2: Listar Vehículos
```bash
curl -X GET "http://localhost:8000/autos/?limit=5"
```

### Prueba 3: Obtener por VIN
```bash
curl -X GET "http://localhost:8000/autos/chasis/1HGBH41JXMN109186"
```

---

**Última Actualización**: Noviembre 2024  
**Versión API**: 1.0.0  
**Estado**: Producción Listo
