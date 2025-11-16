# Implementación de Videollamadas con Jitsi Meet mediante iframe

Este proyecto implementa un sistema completo de videollamadas utilizando Jitsi Meet integrado mediante iframe dentro de un frontend en React, acompañado de un backend en FastAPI encargado de la gestión de salas, participantes y eventos.

## 🚀 Resumen General

El sistema permite:

- Crear salas de videollamada.
- Unirse a salas ya creadas.
- Administrar participantes y estados.
- Conectarse a Jitsi Meet usando URLs generadas por el backend.
- Integrarse mediante un iframe simple y compatible con todos los navegadores.

La arquitectura fue diseñada para entornos de desarrollo y pruebas, con miras a extenderse a producción mediante autenticación real, base de datos persistente y un servidor Jitsi propio.

## 📌 Arquitectura

### Componentes principales

- **Backend (FastAPI)**
  API REST encargada de gestionar salas y participantes.

- **Frontend (React + Vite)**
  Interfaz de usuario con integración vía iframe hacia Jitsi.

- **Jitsi Meet**
  Servicio externo utilizado para videoconferencias.

## 🛠 Backend (FastAPI)

### Estructura del proyecto

```
video_service/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── database.py
│   ├── jwt_handler.py
│   └── routes/
│       └── video.py
├── requirements.txt
└── README.md
```

### Funcionalidades principales

- Configuración CORS para entornos de desarrollo.
- API REST para crear, unirse, listar y finalizar salas.
- Almacenamiento temporal en memoria.
- Autenticación basada en token de prueba (test-token).

## 🖥 Frontend (React + Vite)

### Estructura del proyecto

```
frontend/
├── src/
│   ├── components/
│   │   ├── video/
│   │   │   ├── VideoCall.jsx
│   │   │   ├── PreCallScreen.jsx
│   │   │   └── CallControls.jsx
│   │   └── ui/
│   ├── services/
│   │   └── videoService.js
│   ├── lib/
│   └── App.jsx
├── vite.config.js
└── package.json
```

### Integración con Jitsi

Se utiliza un iframe para cargar:

```
https://meet.jit.si/{roomName}?userInfo.displayName={userName}
```

**Permisos del iframe:**
- Cámara
- Micrófono
- Pantalla compartida
- Pantalla completa

## ⭐ Ventajas

- Integración simple
- Cero librerías adicionales de Jitsi
- Aislamiento seguro mediante iframe
- Mantenimiento mínimo
- Compatible con todos los navegadores modernos

## ⚠️ Limitaciones

- **Límite de tiempo**: `meet.jit.si` desconecta las llamadas después de 5 minutos cuando se embebe en iframes
- **Solo para desarrollo**: El servidor público no está diseñado para uso en producción
- Control programático limitado
- No se reciben eventos de Jitsi desde el iframe
- Sin soporte para JWT en servidor público
- Personalización de interfaz restringida

### 🚀 Opciones para Producción

1. **Jitsi as a Service (JaaS)** - Servicio de pago gestionado
   - Sin límite de tiempo
   - Soporte oficial para embedding
   - Más información: https://jitsi.org/jitsi-as-a-service/

2. **Servidor Jitsi propio** - Gratuito pero requiere configuración
   - Sin límites de tiempo
   - Control total de la infraestructura
   - Documentación: https://jitsi.github.io/handbook/docs/devops-guide/

## 🚀 Guía de Inicio - Proyecto Jitsi

### ⚡ Inicio Rápido

#### 1️⃣ Backend (FastAPI)

**Ubicación:** `video_service/`

```bash
# Activar entorno virtual
cd video_service
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Ejecutar servidor
uvicorn app.main:app --reload --port 8000
```

**Verificar que funciona:**
- Health check: http://localhost:8000/health
- Documentación API: http://localhost:8000/docs
- Puerto: 8000

#### 2️⃣ Frontend (React + Vite)

**Ubicación:** `frontend/`

```bash
# Instalar dependencias (solo primera vez)
cd frontend
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

**Verificar que funciona:**
- URL: http://localhost:5173 (o el puerto que indique Vite)
- Debería abrir automáticamente en el navegador
- Puerto: 5173 (o el siguiente disponible si está ocupado)

### 📋 Orden de Inicio Recomendado

1. Backend
2. Frontend

## 🎮 Cómo Usar la Aplicación

### Paso 1: Abrir el Frontend

Acceder a: http://localhost:5173

### Paso 2: Crear una Videollamada

- Introducir nombre de sala
- Introducir nombre de usuario
- Presionar **Iniciar Videollamada**

### Paso 3: Permitir permisos

Aceptar permisos de cámara y micrófono.

### Paso 4: Controles dentro del iframe

- Silenciar micrófono
- Apagar cámara
- Compartir pantalla
- Salir de la llamada

### Paso 5: Compartir Sala

- Enviar la URL del navegador a otros usuarios
- O abrir otra ventana con la misma sala

## 🔍 Verificar que Todo Funciona

### Backend

```bash
curl http://localhost:8000/health
```

Debe devolver:

```json
{"status": "healthy"}
```

### Frontend

- Debe cargar la pantalla inicial
- Sin errores en la consola

## ⚠️ Solución de Problemas

### Puerto 8000 ocupado

```bash
uvicorn app.main:app --reload --port 8001
```

### Puerto 5173 ocupado

Vite toma el siguiente puerto disponible.

### Error CORS

Verificar los orígenes en:

`video_service/app/config.py`

## 🛑 Detener Servicios

### Backend

`Ctrl + C`

### Frontend

`Ctrl + C`

## 📝 Notas Importantes

- Token por defecto: `test-token`.
- Base de datos en memoria.
- Servidor público de Jitsi (meet.jit.si).

## 🔗 URLs Importantes

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

