# Documentación Técnica - Microservicio de Videollamadas Jitsi

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [API Reference](#api-reference)
3. [Integración Frontend](#integración-frontend)
4. [Uso del Microservicio](#uso-del-microservicio)
5. [Autenticación](#autenticación)
6. [Integración con Jitsi](#integración-con-jitsi)
7. [Ejemplos Completos](#ejemplos-completos)
8. [Manejo de Errores](#manejo-de-errores)

---

## Introducción

Este microservicio proporciona una API REST para gestionar videollamadas usando Jitsi Meet. Actúa como una capa de abstracción que gestiona salas, participantes y genera URLs de Jitsi.

### Base URL

```
http://localhost:8000  (desarrollo)
https://api.tu-dominio.com  (producción)
```

### Formato de Respuestas

Todas las respuestas son en formato JSON.

---

## API Reference

### Base Path

Todos los endpoints están bajo el prefijo: `/api/video`

---

### POST /api/video/create-room

Crea una nueva sala de videollamada.

#### Headers

```
Authorization: Bearer <token>
Content-Type: application/json
```

#### Request Body

```json
{
  "room_name": "mi-sala-reunion",
  "user_id": "user-123",
  "user_name": "Juan Pérez",
  "is_host": true,
  "workspace_id": "workspace-456",
  "channel_id": "channel-789"
}
```

#### Parámetros

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `room_name` | string | ✅ | Nombre único de la sala |
| `user_id` | string | ✅ | ID del usuario que crea la sala |
| `user_name` | string | ✅ | Nombre del usuario |
| `is_host` | boolean | ❌ | Si es el host (default: true) |
| `workspace_id` | string | ❌ | ID del workspace (opcional) |
| `channel_id` | string | ❌ | ID del canal (opcional) |

#### Response 200 OK

```json
{
  "room_id": "room-abc123",
  "room_name": "mi-sala-reunion",
  "host_id": "user-123",
  "workspace_id": "workspace-456",
  "channel_id": "channel-789",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "jitsi_url": "https://meet.jit.si/mi-sala-reunion",
  "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Response 401 Unauthorized

```json
{
  "detail": "Token de autenticación requerido"
}
```

#### Response 500 Internal Server Error

```json
{
  "detail": "Error creando sala: <mensaje>"
}
```

#### Ejemplo cURL

```bash
curl -X POST "http://localhost:8000/api/video/create-room" \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "room_name": "mi-sala",
    "user_id": "user-123",
    "user_name": "Juan"
  }'
```

---

### POST /api/video/join-room

Permite a un usuario unirse a una sala existente.

#### Headers

```
Authorization: Bearer <token>
Content-Type: application/json
```

#### Request Body

```json
{
  "room_id": "room-abc123",
  "user_id": "user-456",
  "user_name": "María García"
}
```

#### Parámetros

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `room_id` | string | ✅ | ID de la sala a la que se une |
| `user_id` | string | ✅ | ID del usuario |
| `user_name` | string | ✅ | Nombre del usuario |

#### Response 200 OK

```json
{
  "participant_id": "participant-xyz789",
  "user_id": "user-456",
  "user_name": "María García",
  "room_id": "room-abc123",
  "joined_at": "2024-01-15T10:35:00Z",
  "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Response 404 Not Found

```json
{
  "detail": "Sala no encontrada"
}
```

#### Response 400 Bad Request

```json
{
  "detail": "Sala no está activa"
}
```

#### Response 403 Forbidden

```json
{
  "detail": "Sala llena (máximo 50 participantes)"
}
```

#### Ejemplo cURL

```bash
curl -X POST "http://localhost:8000/api/video/join-room" \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "room_id": "room-abc123",
    "user_id": "user-456",
    "user_name": "María"
  }'
```

---

### GET /api/video/rooms/{room_id}

Obtiene información detallada de una sala incluyendo todos sus participantes.

#### Headers

```
Authorization: Bearer <token>
```

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `room_id` | string | ID de la sala |

#### Response 200 OK

```json
{
  "room_id": "room-abc123",
  "room_name": "mi-sala-reunion",
  "host_id": "user-123",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "participants": [
    {
      "participant_id": "participant-xyz789",
      "user_id": "user-123",
      "user_name": "Juan Pérez",
      "room_id": "room-abc123",
      "joined_at": "2024-01-15T10:30:00Z"
    },
    {
      "participant_id": "participant-abc456",
      "user_id": "user-456",
      "user_name": "María García",
      "room_id": "room-abc123",
      "joined_at": "2024-01-15T10:35:00Z"
    }
  ]
}
```

#### Ejemplo cURL

```bash
curl -X GET "http://localhost:8000/api/video/rooms/room-abc123" \
  -H "Authorization: Bearer test-token"
```

---

### DELETE /api/video/rooms/{room_id}

Termina una sala de videollamada. Solo el host puede terminar la sala.

#### Headers

```
Authorization: Bearer <token>
```

#### Path Parameters

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `room_id` | string | ID de la sala a terminar |

#### Response 200 OK

```json
{
  "message": "Sala terminada exitosamente"
}
```

#### Response 403 Forbidden

```json
{
  "detail": "Solo el host puede terminar la sala"
}
```

#### Ejemplo cURL

```bash
curl -X DELETE "http://localhost:8000/api/video/rooms/room-abc123" \
  -H "Authorization: Bearer test-token"
```

---

### GET /api/video/rooms

Lista todas las salas activas.

#### Headers

```
Authorization: Bearer <token>
```

#### Response 200 OK

```json
[
  {
    "room_id": "room-abc123",
    "room_name": "mi-sala-reunion",
    "host_id": "user-123",
    "workspace_id": "workspace-456",
    "channel_id": "channel-789",
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z",
    "jitsi_url": "https://meet.jit.si/mi-sala-reunion"
  },
  {
    "room_id": "room-def456",
    "room_name": "otra-sala",
    "host_id": "user-789",
    "workspace_id": null,
    "channel_id": null,
    "status": "active",
    "created_at": "2024-01-15T11:00:00Z",
    "jitsi_url": "https://meet.jit.si/otra-sala"
  }
]
```

#### Ejemplo cURL

```bash
curl -X GET "http://localhost:8000/api/video/rooms" \
  -H "Authorization: Bearer test-token"
```

---

## Integración Frontend

### Instalación del Servicio

El servicio está en `frontend/src/services/videoService.js`. Ya está configurado para usar `http://localhost:8000` por defecto.

### Configuración de la URL Base

```javascript
// frontend/src/services/videoService.js
const API_BASE_URL = 'http://localhost:8000'; // Cambiar en producción
```

### Uso Básico

#### 1. Importar el servicio

```javascript
import { videoService } from '@/services/videoService';
```

#### 2. Crear una sala

```javascript
const createVideoRoom = async () => {
  try {
    const authToken = 'test-token'; // O tu token real
    const roomData = {
      room_name: 'mi-reunion',
      user_id: 'user-123',
      user_name: 'Juan Pérez',
      is_host: true,
      workspace_id: 'workspace-456'
    };

    const response = await videoService.createRoom(roomData, authToken);
    console.log('Sala creada:', response);
    
    // response.jitsi_url contiene la URL de Jitsi
    // response.room_id contiene el ID de la sala
    
    return response;
  } catch (error) {
    console.error('Error creando sala:', error);
    throw error;
  }
};
```

#### 3. Unirse a una sala

```javascript
const joinVideoRoom = async (roomId) => {
  try {
    const authToken = 'test-token';
    const userData = {
      user_id: 'user-456',
      user_name: 'María García'
    };

    const response = await videoService.joinRoom(roomId, userData, authToken);
    console.log('Unido a sala:', response);
    
    return response;
  } catch (error) {
    console.error('Error uniéndose a sala:', error);
    throw error;
  }
};
```

#### 4. Obtener información de una sala

```javascript
const getRoomInfo = async (roomId) => {
  try {
    const authToken = 'test-token';
    const roomInfo = await videoService.getRoom(roomId, authToken);
    console.log('Info de sala:', roomInfo);
    console.log('Participantes:', roomInfo.participants);
    
    return roomInfo;
  } catch (error) {
    console.error('Error obteniendo sala:', error);
    throw error;
  }
};
```

### Integración con React Component

Ejemplo completo usando el componente `VideoCall`:

```javascript
import { useState } from 'react';
import { videoService } from '@/services/videoService';

const VideoCall = () => {
  const [isInCall, setIsInCall] = useState(false);
  const [jitsiUrl, setJitsiUrl] = useState('');
  const [error, setError] = useState(null);

  const handleStartCall = async (roomName, userName) => {
    try {
      const authToken = 'test-token';
      
      // 1. Crear sala en el backend
      const response = await videoService.createRoom({
        room_name: roomName,
        user_id: `user-${Date.now()}`,
        user_name: userName,
        is_host: true
      }, authToken);

      // 2. Construir URL de Jitsi con nombre de usuario
      const encodedRoomName = encodeURIComponent(response.room_name);
      const encodedUserName = encodeURIComponent(userName);
      const jitsiUrl = `https://meet.jit.si/${encodedRoomName}?userInfo.displayName=${encodedUserName}`;
      
      // 3. Actualizar estado y mostrar iframe
      setJitsiUrl(jitsiUrl);
      setIsInCall(true);
    } catch (err) {
      setError(err.message || 'Error iniciando la videollamada');
    }
  };

  const handleLeaveCall = () => {
    setIsInCall(false);
    setJitsiUrl('');
  };

  if (!isInCall) {
    // Mostrar formulario para crear/unirse
    return <PreCallScreen onStartCall={handleStartCall} />;
  }

  return (
    <div className="relative w-full h-screen bg-gray-900">
      {jitsiUrl && (
        <iframe
          src={jitsiUrl}
          allow="camera; microphone; display-capture; fullscreen"
          style={{
            width: '100%',
            height: '100%',
            border: 'none',
          }}
          title="Jitsi Meet"
        />
      )}
    </div>
  );
};
```

---

## Uso del Microservicio

### Desde otra aplicación (Backend a Backend)

#### Ejemplo en Python

```python
import httpx

class VideoServiceClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

    async def create_room(self, room_name: str, user_id: str, user_name: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/video/create-room",
                headers=self.headers,
                json={
                    "room_name": room_name,
                    "user_id": user_id,
                    "user_name": user_name,
                    "is_host": True
                }
            )
            response.raise_for_status()
            return response.json()

    async def join_room(self, room_id: str, user_id: str, user_name: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/video/join-room",
                headers=self.headers,
                json={
                    "room_id": room_id,
                    "user_id": user_id,
                    "user_name": user_name
                }
            )
            response.raise_for_status()
            return response.json()

    async def get_room(self, room_id: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/video/rooms/{room_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

# Uso
client = VideoServiceClient("http://localhost:8000", "test-token")

# Crear sala
room = await client.create_room(
    room_name="reunion-equipo",
    user_id="user-123",
    user_name="Juan Pérez"
)
print(f"Sala creada: {room['room_id']}")
print(f"URL Jitsi: {room['jitsi_url']}")
```

#### Ejemplo en Node.js

```javascript
const axios = require('axios');

class VideoServiceClient {
  constructor(baseUrl, authToken) {
    this.baseUrl = baseUrl;
    this.client = axios.create({
      baseURL: baseUrl,
      headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
      }
    });
  }

  async createRoom(roomName, userId, userName) {
    const response = await this.client.post('/api/video/create-room', {
      room_name: roomName,
      user_id: userId,
      user_name: userName,
      is_host: true
    });
    return response.data;
  }

  async joinRoom(roomId, userId, userName) {
    const response = await this.client.post('/api/video/join-room', {
      room_id: roomId,
      user_id: userId,
      user_name: userName
    });
    return response.data;
  }

  async getRoom(roomId) {
    const response = await this.client.get(`/api/video/rooms/${roomId}`);
    return response.data;
  }

  async listRooms() {
    const response = await this.client.get('/api/video/rooms');
    return response.data;
  }
}

// Uso
const client = new VideoServiceClient('http://localhost:8000', 'test-token');

async function crearSala() {
  const room = await client.createRoom(
    'reunion-equipo',
    'user-123',
    'Juan Pérez'
  );
  console.log('Sala creada:', room.room_id);
  console.log('URL Jitsi:', room.jitsi_url);
}
```

---

## Autenticación

### Token Bearer

Todas las peticiones requieren un token Bearer en el header `Authorization`.

#### Header requerido

```
Authorization: Bearer <tu-token>
```

### Desarrollo

En desarrollo, el microservicio acepta el token `test-token`:

```javascript
const authToken = 'test-token';
```

### Producción

En producción, necesitas generar tokens JWT válidos:

```javascript
// Ejemplo de cómo obtener token real
const authToken = await getUserToken(); // Tu función de autenticación
```

### Validación de Token

El microservicio valida tokens de la siguiente manera:

1. Si el token es `test-token` → acepta automáticamente (solo desarrollo)
2. Si no, intenta verificar como JWT usando `verify_user_jwt()`
3. Si falla → retorna 401 Unauthorized

### Payload del Token

El token debe contener al menos:
- `sub` o `user_id`: ID del usuario
- `user_name`: Nombre del usuario (opcional)

---

## Integración con Jitsi

> **⚠️ IMPORTANTE**: `meet.jit.si` tiene un límite de 5 minutos cuando se embebe en iframes. Solo es adecuado para desarrollo. Para producción, usa Jitsi as a Service (pago) o tu propio servidor Jitsi (gratuito pero requiere configuración).

### Construcción de URL de Jitsi

El microservicio genera URLs base de Jitsi, pero el frontend construye la URL final con parámetros adicionales.

#### URL Base (desde backend)

```
https://meet.jit.si/{room_name}
```

#### URL Final (frontend)

```javascript
const jitsiUrl = `https://meet.jit.si/${encodeURIComponent(roomName)}?userInfo.displayName=${encodeURIComponent(userName)}`;
```

### Parámetros de URL Jitsi

#### Parámetros comunes

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `userInfo.displayName` | Nombre del usuario | `?userInfo.displayName=Juan` |
| `config.startWithVideoMuted` | Iniciar sin video | `?config.startWithVideoMuted=true` |
| `config.startWithAudioMuted` | Iniciar sin audio | `?config.startWithAudioMuted=true` |

#### Ejemplo con múltiples parámetros

```javascript
const roomName = 'mi-sala';
const userName = 'Juan Pérez';
const params = new URLSearchParams({
  'userInfo.displayName': userName,
  'config.startWithVideoMuted': 'true',
  'config.startWithAudioMuted': 'false'
});
const jitsiUrl = `https://meet.jit.si/${encodeURIComponent(roomName)}?${params.toString()}`;
// Resultado: https://meet.jit.si/mi-sala?userInfo.displayName=Juan+P%C3%A9rez&config.startWithVideoMuted=true&config.startWithAudioMuted=false
```

### Renderizado del iframe

```javascript
<iframe
  src={jitsiUrl}
  allow="camera; microphone; display-capture; fullscreen"
  style={{
    width: '100%',
    height: '100%',
    border: 'none',
  }}
  title="Jitsi Meet"
/>
```

### Permisos del iframe

Los permisos necesarios son:
- `camera`: Acceso a la cámara
- `microphone`: Acceso al micrófono
- `display-capture`: Compartir pantalla
- `fullscreen`: Pantalla completa

### Notas sobre JWT

- El microservicio genera tokens JWT, pero el servidor público `meet.jit.si` no los acepta
- Para usar JWT necesitas tu propio servidor Jitsi
- Los tokens JWT se generan pero no se usan con el servidor público

### ⚠️ Limitaciones de meet.jit.si en iframes

**Importante**: Cuando embebes `meet.jit.si` en un iframe, tiene limitaciones:

- ❌ **Límite de tiempo**: Las llamadas se desconectan automáticamente después de **5 minutos**
- ❌ **Solo para desarrollo/demostración**: No está diseñado para uso en producción
- ❌ **Sin soporte oficial**: Jitsi recomienda usar sus servicios oficiales para producción

**Solución para producción:**

1. **Jitsi as a Service (JaaS)** - Servicio de pago gestionado
   - ✅ Sin límite de tiempo
   - ✅ Soporte para embedding
   - ✅ Más estable y confiable
   - 💰 Requiere suscripción de pago
   - 🔗 Más información: https://jitsi.org/jitsi-as-a-service/

2. **Servidor Jitsi propio** - Gratuito pero requiere configuración
   - ✅ Sin límites de tiempo
   - ✅ Control total de la infraestructura
   - ✅ Uso gratuito del software
   - ⚙️ Requiere configurar y mantener servidores propios
   - 📚 Documentación: https://jitsi.github.io/handbook/docs/devops-guide/

---

## Ejemplos Completos

### Ejemplo 1: Crear sala y unirse

```javascript
// 1. Crear sala
const room = await videoService.createRoom({
  room_name: 'reunion-equipo',
  user_id: 'user-1',
  user_name: 'Juan',
  is_host: true
}, 'test-token');

console.log('Sala creada:', room.room_id);

// 2. Construir URL y mostrar
const jitsiUrl = `https://meet.jit.si/${encodeURIComponent(room.room_name)}?userInfo.displayName=${encodeURIComponent('Juan')}`;
setJitsiUrl(jitsiUrl);

// 3. Otro usuario se une
const participant = await videoService.joinRoom(room.room_id, {
  user_id: 'user-2',
  user_name: 'María'
}, 'test-token');

console.log('Usuario unido:', participant.user_name);
```

### Ejemplo 2: Obtener participantes de una sala

```javascript
const roomInfo = await videoService.getRoom(roomId, 'test-token');

console.log('Sala:', roomInfo.room_name);
console.log('Host:', roomInfo.host_id);
console.log('Participantes:');

roomInfo.participants.forEach(participant => {
  console.log(`- ${participant.user_name} (${participant.user_id})`);
  console.log(`  Unido: ${participant.joined_at}`);
});
```

### Ejemplo 3: Listar todas las salas activas

```javascript
const response = await fetch('http://localhost:8000/api/video/rooms', {
  headers: {
    'Authorization': 'Bearer test-token'
  }
});

const rooms = await response.json();

console.log('Salas activas:');
rooms.forEach(room => {
  console.log(`- ${room.room_name} (${room.room_id})`);
  console.log(`  URL: ${room.jitsi_url}`);
  console.log(`  Host: ${room.host_id}`);
});
```

### Ejemplo 4: Terminar una sala

```javascript
const response = await fetch(`http://localhost:8000/api/video/rooms/${roomId}`, {
  method: 'DELETE',
  headers: {
    'Authorization': 'Bearer test-token'
  }
});

if (response.ok) {
  const result = await response.json();
  console.log(result.message); // "Sala terminada exitosamente"
}
```

---

## Manejo de Errores

### Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | OK - Petición exitosa |
| 400 | Bad Request - Datos inválidos o sala no activa |
| 401 | Unauthorized - Token inválido o faltante |
| 403 | Forbidden - Sin permisos (solo host puede terminar sala) o sala llena |
| 404 | Not Found - Sala no encontrada |
| 500 | Internal Server Error - Error del servidor |

### Manejo en JavaScript

```javascript
try {
  const room = await videoService.createRoom(roomData, authToken);
  // Éxito
} catch (error) {
  if (error.message.includes('401')) {
    // Token inválido
    console.error('Token inválido. Por favor, inicia sesión.');
  } else if (error.message.includes('404')) {
    // Sala no encontrada
    console.error('La sala no existe.');
  } else if (error.message.includes('403')) {
    // Sin permisos o sala llena
    console.error('No tienes permisos o la sala está llena.');
  } else {
    // Error genérico
    console.error('Error:', error.message);
  }
}
```

### Manejo en Python

```python
import httpx

try:
    response = await client.post(
        f"{base_url}/api/video/create-room",
        headers=headers,
        json=room_data
    )
    response.raise_for_status()
    room = response.json()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        print("Token inválido")
    elif e.response.status_code == 404:
        print("Sala no encontrada")
    elif e.response.status_code == 403:
        print("Sin permisos o sala llena")
    else:
        print(f"Error: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")
```

---

## Notas Adicionales

### Límites

- **Participantes máximos por sala**: 50
- **Autenticación**: Requiere token Bearer en todas las peticiones
- **Base de datos**: En memoria (se pierde al reiniciar el servidor)

### Configuración

Las configuraciones están en `video_service/app/config.py`:

- `JITSI_DOMAIN`: Dominio de Jitsi (default: `meet.jit.si`)
- `CORS_ORIGINS`: Orígenes permitidos para CORS
- `JWT_EXPIRATION_HOURS`: Expiración de tokens JWT (default: 2 horas)

### Producción

Para producción, considera:

1. **Configurar dominio de Jitsi**:
   - **Opción A**: Cambiar `JITSI_DOMAIN` a tu propio servidor Jitsi (gratuito pero requiere infraestructura)
   - **Opción B**: Usar Jitsi as a Service (JaaS) - de pago pero gestionado
   - ⚠️ **No usar `meet.jit.si` en producción**: Tiene límite de 5 minutos en iframes

2. **Autenticación**:
   - Implementar autenticación real con JWT
   - Eliminar el token `test-token` de desarrollo

3. **Base de datos**:
   - Migrar de memoria a base de datos persistente (PostgreSQL, MongoDB, etc.)

4. **Infraestructura**:
   - Configurar HTTPS
   - Ajustar `CORS_ORIGINS` a tus dominios de producción
   - Configurar balanceadores de carga si es necesario

5. **Monitoreo**:
   - Implementar logging y monitoreo de errores
   - Configurar alertas para problemas de servicio

---

## Soporte

Para más información, consulta:
- Documentación interactiva: `http://localhost:8000/docs` (Swagger UI)
- Código fuente: `video_service/app/routes/video.py`

