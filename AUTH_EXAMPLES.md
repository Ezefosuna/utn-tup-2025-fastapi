# 🔐 Autenticación JWT - Guía Completa

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [Endpoints de Autenticación](#endpoints-de-autenticación)
3. [Endpoints Protegidos](#endpoints-protegidos)
4. [Ejemplos de Uso](#ejemplos-de-uso)
5. [Flujo de Autenticación](#flujo-de-autenticación)
6. [Manejo de Errores](#manejo-de-errores)

---

## Descripción General

Este sistema implementa autenticación JWT (JSON Web Tokens) para proteger endpoints de la API. Los tokens son generados al hacer login y deben ser incluidos en las solicitudes posteriores.

**Características:**
- ✅ Registro de usuarios
- ✅ Login con JWT
- ✅ Protección de endpoints
- ✅ Renovación de tokens
- ✅ Información del usuario autenticado

---

## Endpoints de Autenticación

### 1. Registro de Usuario

**Método**: `POST`  
**URL**: `/auth/register`  
**Autenticación**: No requerida

**Cuerpo de la solicitud:**
```json
{
  "username": "juan_perez",
  "email": "juan@example.com", 
  "password": "MiContraseña123!"
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "id": 1,
  "username": "juan_perez",
  "email": "juan@example.com",
  "message": "Usuario registrado exitosamente"
}
```

**Posibles errores:**
- 400: Username o email ya existe
- 422: Datos inválidos

---

### 2. Login de Usuario

**Método**: `POST`  
**URL**: `/auth/login`  
**Autenticación**: No requerida

**Cuerpo de la solicitud:**
```json
{
  "username": "juan_perez",
  "password": "MiContraseña123!"
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqdWFuX3BlcmV6IiwiZXhwIjoxNjk5MzAwMjAwfQ.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "juan_perez",
    "email": "juan@example.com"
  }
}
```

**Posibles errores:**
- 401: Credenciales inválidas
- 422: Datos incompletos

---

### 3. Login para Swagger UI (OAuth2)

**Método**: `POST`  
**URL**: `/auth/login-form`  
**Formato**: Form Data (no JSON)

**Parámetros:**
- `username` (string): Nombre de usuario
- `password` (string): Contraseña

Este endpoint es compatible con el formulario de autenticación de Swagger UI.

---

### 4. Información del Usuario Autenticado

**Método**: `GET`  
**URL**: `/auth/me`  
**Autenticación**: Requerida ✅

**Headers requeridos:**
```
Authorization: Bearer <access_token>
```

**Respuesta exitosa (200 OK):**
```json
{
  "id": 1,
  "username": "juan_perez",
  "email": "juan@example.com",
  "created_at": "2024-11-20T10:30:00Z"
}
```

**Posibles errores:**
- 401: Token no válido o expirado
- 401: Token no proporcionado

---

## Endpoints Protegidos

### 1. Test de Autenticación

**Método**: `GET`  
**URL**: `/protected/test`  
**Autenticación**: Requerida ✅

**Headers requeridos:**
```
Authorization: Bearer <access_token>
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Acceso autorizado",
  "user": "juan_perez",
  "timestamp": "2024-11-20T10:35:00Z"
}
```

---

### 2. Perfil de Usuario Detallado

**Método**: `GET`  
**URL**: `/protected/user-profile`  
**Autenticación**: Requerida ✅

**Headers requeridos:**
```
Authorization: Bearer <access_token>
```

**Respuesta exitosa (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "juan_perez",
    "email": "juan@example.com",
    "created_at": "2024-11-20T10:30:00Z",
    "role": "user",
    "last_login": "2024-11-20T10:35:00Z"
  },
  "stats": {
    "total_autos": 5,
    "total_ventas": 3
  }
}
```

---

## Ejemplos de Uso

### Usando cURL

#### Registro
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_perez",
    "email": "juan@example.com",
    "password": "MiContraseña123!"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_perez",
    "password": "MiContraseña123!"
  }'
```

#### Acceso a endpoint protegido
```bash
curl -X GET "http://localhost:8000/protected/test" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Usando JavaScript (Fetch API)

```javascript
// 1. Registro
const registroResponse = await fetch('http://localhost:8000/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'juan_perez',
    email: 'juan@example.com',
    password: 'MiContraseña123!'
  })
});

// 2. Login
const loginResponse = await fetch('http://localhost:8000/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'juan_perez',
    password: 'MiContraseña123!'
  })
});

const loginData = await loginResponse.json();
const token = loginData.access_token;

// 3. Usar token en endpoint protegido
const protectedResponse = await fetch('http://localhost:8000/protected/test', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const protectedData = await protectedResponse.json();
console.log(protectedData);
```

### Usando Python (Requests)

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Registro
registro_resp = requests.post(f"{BASE_URL}/auth/register", json={
    "username": "juan_perez",
    "email": "juan@example.com",
    "password": "MiContraseña123!"
})
print(registro_resp.json())

# 2. Login
login_resp = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "juan_perez",
    "password": "MiContraseña123!"
})
login_data = login_resp.json()
token = login_data["access_token"]

# 3. Usar token
headers = {"Authorization": f"Bearer {token}"}
protected_resp = requests.get(f"{BASE_URL}/protected/test", headers=headers)
print(protected_resp.json())
```

---

## Flujo de Autenticación

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       │ 1. POST /auth/register
       │    (username, email, password)
       ▼
┌─────────────────────┐
│ Crear Usuario       │
│ (Base de Datos)     │
└────────┬────────────┘
         │
         │ Respuesta: 201 Created
         ▼
    ┌─────────┐
    │ Mensaje │
    │ éxito   │
    └────┬────┘
         │
         │ 2. POST /auth/login
         │    (username, password)
         ▼
┌──────────────────────┐
│ Validar Credenciales │
│ Generar JWT Token    │
└──────┬───────────────┘
       │
       │ Respuesta: 200 OK
       │ {access_token, token_type}
       ▼
  ┌─────────────┐
  │   Token     │
  │  Guardado   │
  └────┬────────┘
       │
       │ 3. GET /protected/*
       │    Authorization: Bearer <token>
       ▼
┌───────────────────┐
│ Verificar Token   │
│ - Válido?         │
│ - Expirado?       │
└────┬──────────────┘
     │
     ├─ Válido ─────▶ ┌──────────┐
     │                │ 200 OK   │
     │                │ Acceso   │
     │                └──────────┘
     │
     └─ No válido ─▶  ┌──────────┐
                      │ 401      │
                      │ Denegado │
                      └──────────┘
```

---

## Manejo de Errores

| Código | Error | Solución |
|--------|-------|---------|
| 400 | Username ya existe | Elige otro nombre de usuario |
| 400 | Email ya registrado | Usa otro email |
| 401 | Credenciales inválidas | Verifica username y password |
| 401 | Token expirado | Vuelve a hacer login |
| 401 | Token no proporcionado | Incluye `Authorization` header |
| 422 | Datos inválidos | Valida el formato JSON |
| 500 | Error del servidor | Contacta al administrador |

### Respuestas de Error

```json
{
  "detail": "Credenciales inválidas",
  "error_code": "INVALID_CREDENTIALS",
  "timestamp": "2024-11-20T10:40:00Z"
}
```

---

## 🔑 Seguridad

### Mejores Prácticas

1. **Almacena el token de forma segura**
   - En aplicaciones web: localStorage/sessionStorage
   - En móvil: Keychain/Keystore
   - Nunca en localStorage si es posible

2. **Siempre usa HTTPS en producción**
   - Los tokens viajan en headers
   - Protege la comunicación

3. **Implementa refresh tokens**
   - Access token: Corta duración (15 min)
   - Refresh token: Larga duración (7 días)

4. **Valida tokens en el servidor**
   - Verifica firma
   - Verifica expiración
   - Verifica audiencia

5. **No expongas secretos**
   - Guarda JWT_SECRET en variables de entorno
   - No lo hagas público

---

## Troubleshooting

### "Token inválido"
```
Posibles causas:
- Token expirado
- Token corrupto
- Token de diferente servidor
```

### "Token no proporcionado"
```
Solución:
- Agrega header Authorization: Bearer <token>
- Verifica que el formato sea correcto
```

### "CORS error"
```
Solución:
- Configura CORS en FastAPI
- Incluye credenciales si es necesario
```

---

**Última Actualización**: Noviembre 2024  
**Versión**: 1.0.0
- Headers: `Authorization: Bearer <token>`

### 3. Dashboard
**GET** `/protected/dashboard`
- Headers: `Authorization: Bearer <token>`

## Ejemplo de Uso con cURL

### 1. Registrar Usuario
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser", 
    "password": "password123"
  }'
```

### 3. Acceder a Endpoint Protegido
```bash
# Reemplaza <TOKEN> con el token obtenido del login
curl -X GET "http://localhost:8000/protected/test" \
  -H "Authorization: Bearer <TOKEN>"
```

## Configuración

- **Duración del token**: 30 minutos (configurable en `auth.py`)
- **Algoritmo**: HS256
- **Secret Key**: Cambiar en producción (ver `auth.py`)

## Instalación de Dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar el Servidor

```bash
uvicorn main:app --reload
```

La documentación interactiva estará disponible en: http://localhost:8000/docs
