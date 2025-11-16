# Informe Técnico: Implementación de Videollamadas con Jitsi Meet mediante iframe

## Resumen Ejecutivo

Se implementó un sistema completo de videollamadas utilizando Jitsi Meet como servicio de videoconferencia, integrado mediante iframe HTML en una aplicación React. El sistema consta de un backend FastAPI que gestiona las salas de videollamada y un frontend React que presenta la interfaz de usuario.

## Arquitectura del Sistema

### Componentes Principales

1. **Backend (FastAPI)**: Microservicio REST API que gestiona salas de videollamada
2. **Frontend (React + Vite)**: Interfaz de usuario con integración de Jitsi mediante iframe
3. **Jitsi Meet**: Servicio de videoconferencia externo (meet.jit.si)

## Implementación del Backend

### Estructura del Proyecto

El backend está organizado en la carpeta `video_service/` con la siguiente estructura:

```
video_service/
├── app/
│   ├── main.py              # Aplicación FastAPI principal
│   ├── config.py            # Configuración de variables de entorno
│   ├── models.py            # Modelos Pydantic para validación
│   ├── database.py          # Gestión de datos en memoria
│   ├── jwt_handler.py       # Generación de tokens (reservado para futuro)
│   ├── rabbitmq.py          # Publicación de eventos
│   └── routes/
│       └── video.py         # Endpoints REST
├── requirements.txt
└── README.md
```

### Configuración de FastAPI

En `app/main.py` se configura la aplicación FastAPI con:

- CORS habilitado para permitir peticiones desde el frontend (puertos 5173, 5174, 5175)
- Middleware CORS configurado para aceptar credenciales y todos los métodos HTTP
- Router de video incluido en la aplicación principal
- Eventos de startup/shutdown para gestión de conexiones RabbitMQ

### Endpoints Implementados

**POST /api/video/create-room**
- Función: Crea una nueva sala de videollamada
- Autenticación: Requiere token Bearer (acepta 'test-token' para desarrollo)
- Parámetros de entrada:
  - `room_name`: Nombre de la sala
  - `user_id`: Identificador del usuario
  - `user_name`: Nombre del usuario
  - `is_host`: Indica si el usuario es host
  - `workspace_id` (opcional): ID del workspace
  - `channel_id` (opcional): ID del canal
- Respuesta: Retorna información de la sala incluyendo `jitsi_url` y `jwt_token` (opcional)

**POST /api/video/join-room**
- Función: Permite a un usuario unirse a una sala existente
- Validaciones: Verifica existencia de sala, estado activo, límite de participantes

**GET /api/video/rooms/{room_id}**
- Función: Obtiene información de una sala específica incluyendo participantes

**DELETE /api/video/rooms/{room_id}**
- Función: Finaliza una sala de videollamada

**GET /api/video/rooms**
- Función: Lista todas las salas activas

### Sistema de Autenticación

Para desarrollo, se implementó un sistema simplificado que acepta el token 'test-token' como válido. La función `get_current_user` en `routes/video.py` verifica:

1. Presencia del header Authorization
2. Si el token es 'test-token', retorna un usuario de prueba
3. En caso contrario, intenta verificar un JWT real (funcionalidad futura)

### Gestión de Datos

Se utiliza una base de datos en memoria implementada en `database.py` mediante diccionarios Python. Esta implementación almacena:

- Salas de videollamada con sus metadatos
- Participantes por sala con información de entrada/salida
- Estados de las salas (active, ended)

### Integración con RabbitMQ

El sistema publica eventos en RabbitMQ cuando ocurren acciones importantes:

- `video.room.created`: Cuando se crea una nueva sala
- `video.participant.joined`: Cuando un usuario se une a una sala
- `video.room.ended`: Cuando se finaliza una sala

Los eventos se publican en el exchange 'video.events' con routing keys específicas.

## Implementación del Frontend

### Estructura del Proyecto

El frontend está organizado en la carpeta `frontend/` con la siguiente estructura:

```
frontend/
├── src/
│   ├── components/
│   │   ├── video/
│   │   │   ├── VideoCall.jsx      # Componente principal
│   │   │   ├── PreCallScreen.jsx  # Pantalla de inicio
│   │   │   └── CallControls.jsx   # Controles flotantes
│   │   └── ui/                    # Componentes UI básicos
│   ├── services/
│   │   └── videoService.js        # Cliente API
│   ├── lib/
│   │   └── utils.js               # Utilidades
│   ├── App.jsx
│   └── main.jsx
├── vite.config.js
├── postcss.config.js
└── package.json
```

### Integración con Jitsi mediante iframe

La implementación utiliza un enfoque directo mediante iframe HTML, sin utilizar la External API de Jitsi. Este método es más simple pero con funcionalidad limitada de control programático.

#### Componente VideoCall.jsx

El componente principal gestiona el flujo completo de la videollamada:

**Estado del Componente:**
- `isInCall`: Indica si el usuario está en una llamada activa
- `isLoading`: Estado de carga durante la inicialización
- `error`: Mensajes de error
- `jitsiUrl`: URL completa de la sala de Jitsi
- `roomData`: Datos de la sala actual

**Flujo de Operación:**

1. **Pantalla Pre-Call**: Muestra `PreCallScreen` cuando `isInCall` es `false`
2. **Creación de Sala**: Al enviar el formulario, se llama a `handleStartCall`
3. **Llamada al Backend**: Se invoca `videoService.createRoom()` con los datos del formulario
4. **Construcción de URL**: Se construye la URL de Jitsi sin JWT (servidor público)
5. **Renderizado del iframe**: Se renderiza un elemento `<iframe>` con la URL construida

#### Construcción de la URL de Jitsi

La URL se construye siguiendo el formato estándar de Jitsi Meet:

```
https://meet.jit.si/{roomName}?userInfo.displayName={userName}
```

Donde:
- `roomName`: Nombre de la sala codificado con `encodeURIComponent()`
- `userName`: Nombre del usuario pasado como query parameter

**Decisión de Diseño**: Se decidió no incluir JWT en la URL porque:
- El servidor público `meet.jit.si` no acepta JWT externos
- Los JWT requieren configuración específica del servidor de Jitsi
- Para desarrollo, no es necesario autenticación avanzada

#### Renderizado del iframe

El iframe se renderiza con las siguientes características:

```jsx
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

**Permisos del iframe:**
- `camera`: Permite acceso a la cámara
- `microphone`: Permite acceso al micrófono
- `display-capture`: Permite compartir pantalla
- `fullscreen`: Permite modo pantalla completa

**Estilos:**
- Ancho y alto al 100% del contenedor
- Sin borde para integración visual
- Contenedor con fondo oscuro (`bg-gray-900`)

#### Componente PreCallScreen.jsx

Pantalla de inicio que presenta un formulario con:

- Campo de texto para nombre de sala
- Campo de texto para nombre de usuario
- Botón de envío que valida campos requeridos

Al enviar, se genera automáticamente un `user_id` basado en timestamp y se marca al usuario como host.

#### Componente CallControls.jsx

Controles flotantes posicionados en la parte inferior de la pantalla. Actualmente, estos controles son principalmente decorativos ya que los controles reales están dentro del iframe de Jitsi. El único control funcional es el botón de salir.

### Servicio de API (videoService.js)

Cliente HTTP que se comunica con el backend FastAPI. Implementa tres métodos principales:

1. `createRoom(roomData, authToken)`: Crea una nueva sala
2. `joinRoom(roomId, userData, authToken)`: Se une a una sala existente
3. `getRoom(roomId, authToken)`: Obtiene información de una sala

Todos los métodos incluyen:
- Header `Authorization` con token Bearer
- Manejo de errores HTTP
- Parsing de respuestas JSON

### Configuración de Tailwind CSS

El proyecto utiliza Tailwind CSS v4 con la siguiente configuración:

**postcss.config.js:**
- Plugin `@tailwindcss/postcss` para procesamiento
- Plugin `autoprefixer` para compatibilidad de navegadores

**src/index.css:**
- Directiva `@import "tailwindcss"` para importar utilidades

**vite.config.js:**
- Alias `@` configurado para importaciones relativas desde `src/`
- Path resolution configurado para módulos ES6

## Flujo Completo de Usuario

1. **Usuario abre la aplicación**: Se carga el componente `VideoCall`
2. **Pantalla de inicio**: Se muestra `PreCallScreen` con formulario
3. **Ingreso de datos**: Usuario ingresa nombre de sala y su nombre
4. **Envío del formulario**: Se ejecuta `handleSubmit` en `PreCallScreen`
5. **Llamada al backend**: Se invoca `videoService.createRoom()` con token 'test-token'
6. **Backend procesa**: El backend valida el token, crea la sala en memoria y genera URL de Jitsi
7. **Respuesta al frontend**: Se recibe información de la sala incluyendo `jitsi_url`
8. **Construcción de URL**: Se construye URL completa con nombre de sala y usuario
9. **Renderizado de iframe**: Se renderiza iframe con la URL de Jitsi
10. **Permisos del navegador**: Navegador solicita permisos para cámara y micrófono
11. **Conexión a Jitsi**: Usuario se conecta a la videollamada dentro del iframe
12. **Videollamada activa**: Usuario puede interactuar con Jitsi usando los controles nativos

## Ventajas de la Implementación con iframe

1. **Simplicidad**: No requiere cargar librerías externas adicionales
2. **Mantenimiento**: Jitsi gestiona actualizaciones y mejoras automáticamente
3. **Seguridad**: El iframe proporciona aislamiento de seguridad
4. **Rendimiento**: Carga eficiente sin dependencias adicionales
5. **Compatibilidad**: Funciona en todos los navegadores modernos

## Limitaciones de la Implementación Actual

1. **Control Limitado**: No se puede controlar programáticamente los controles dentro del iframe
2. **Eventos**: No se reciben eventos de Jitsi (usuario unido, salió, etc.)
3. **Autenticación**: No se puede usar JWT personalizado con servidor público
4. **Personalización**: Limitaciones en personalización de la interfaz de Jitsi

## Consideraciones Técnicas

### CORS

El backend está configurado con CORS habilitado para permitir peticiones desde múltiples puertos de desarrollo. La configuración incluye los puertos 5173, 5174 y 5175 para Vite, así como el puerto 3000 para React tradicional.

### Gestión de Estado

El estado de la aplicación se gestiona mediante React hooks (`useState`). No se utiliza estado global ni librerías de gestión de estado como Redux o Zustand.

### Base de Datos

La implementación actual utiliza almacenamiento en memoria. Para producción, sería necesario migrar a una base de datos persistente como PostgreSQL o MongoDB.

### Autenticación

El sistema actual acepta un token de prueba ('test-token') para desarrollo. En producción, se requeriría implementar un sistema de autenticación completo con JWT válidos.

## Mejoras Futuras Recomendadas

1. **Integración de External API**: Para mayor control programático sobre Jitsi
2. **Persistencia de Datos**: Migración a base de datos real (PostgreSQL/Supabase)
3. **Autenticación Real**: Implementación de sistema de autenticación completo
4. **Manejo de Eventos**: Integración de webhooks o polling para eventos de Jitsi
5. **Servidor Jitsi Propio**: Configuración de servidor Jitsi propio para JWT personalizado
6. **Mejoras de UI**: Implementación de controles personalizados más funcionales
7. **Grabación**: Integración de funcionalidad de grabación de videollamadas
8. **Notificaciones**: Sistema de notificaciones cuando usuarios se unen/salen

## Conclusiones

La implementación actual proporciona una solución funcional para videollamadas utilizando Jitsi Meet mediante iframe. El enfoque elegido prioriza la simplicidad y facilidad de mantenimiento sobre el control programático avanzado. El sistema está preparado para desarrollo y pruebas, con una arquitectura que permite escalabilidad futura mediante mejoras incrementales.

La separación clara entre backend y frontend facilita el mantenimiento y la evolución del sistema. El backend actúa como capa de abstracción que gestiona metadatos y eventos, mientras que el frontend se enfoca en la presentación y experiencia de usuario.
