# 🚀 Guía de Inicio - Proyecto Jitsi

## ⚡ Inicio Rápido

### 1️⃣ Backend (FastAPI)

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

**Puerto:** `8000`

---

### 2️⃣ Frontend (React + Vite)

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

**Puerto:** `5173` (o el siguiente disponible si está ocupado)

---

### 3️⃣ RabbitMQ (Opcional)

Solo necesario si quieres ver los eventos publicados.

```bash
# Iniciar con Docker
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Acceder a la interfaz web
# http://localhost:15672
# Usuario: guest
# Contraseña: guest
```

**Puertos:**
- `5672` - AMQP
- `15672` - Interfaz web

---

## 📋 Orden de Inicio Recomendado

1. **Primero:** RabbitMQ (opcional, solo para eventos)
2. **Segundo:** Backend (FastAPI)
3. **Tercero:** Frontend (React)

---

## 🎮 Cómo Usar la Aplicación

### Paso 1: Abrir el Frontend
Abre http://localhost:5173 (o el puerto que indique Vite) en tu navegador.

### Paso 2: Crear una Videollamada
1. Ingresa un **nombre de sala** (ej: "MiReunion")
2. Ingresa tu **nombre** (ej: "Juan")
3. Haz clic en **"Iniciar Videollamada"**

### Paso 3: Permitir Acceso
- El navegador pedirá permiso para usar **cámara** y **micrófono**
- Haz clic en **"Permitir"**

### Paso 4: Usar los Controles
Los controles están en el iframe de Jitsi:
- 🔇 **Micro**: Mute/Unmute
- 📹 **Cámara**: Encender/Apagar
- 🖥️ **Pantalla**: Compartir pantalla
- ❌ **Salir**: Terminar la videollamada

### Paso 5: Compartir la Sala
- Copia la URL del navegador
- Compártela con otros participantes
- O abre otra ventana/ventana incógnita y usa el mismo nombre de sala

---

## 🔍 Verificar que Todo Funciona

### Backend
```bash
# Verificar que responde
curl http://localhost:8000/health
# Debe devolver: {"status":"healthy"}
```

### Frontend
- Debe mostrar la pantalla de inicio
- Sin errores en la consola del navegador (F12)

### RabbitMQ (si está corriendo)
- Abrir http://localhost:15672
- Login: guest/guest
- Ver exchange "video.events"
- Debería tener mensajes cuando creas salas

---

## ⚠️ Solución de Problemas

### Error: "Port 8000 is already in use"
```bash
# Cambiar puerto del backend
uvicorn app.main:app --reload --port 8001
```

### Error: "Port 5173 is already in use"
- Vite usa automáticamente el siguiente puerto disponible
- Revisa la terminal para ver qué puerto está usando

### Error: "RabbitMQ connection failed"
- Es normal si no tienes RabbitMQ corriendo
- El backend funcionará igual, solo no publicará eventos

### Error: "CORS error"
- Verificar que el backend tiene `http://localhost:5173` (o tu puerto) en `CORS_ORIGINS`
- Verificar en `video_service/app/config.py`

---

## 🛑 Detener los Servicios

### Backend
- Presiona `Ctrl+C` en la terminal del backend

### Frontend
- Presiona `Ctrl+C` en la terminal del frontend

### RabbitMQ
```bash
# Ver contenedores
docker ps

# Detener contenedor
docker stop <container_id>
```

---

## 📝 Notas Importantes

1. **Token de Autenticación:** Por ahora usa `test-token` (el backend lo acepta en desarrollo)
2. **Base de Datos:** Usa memoria en desarrollo (se pierde al reiniciar el backend)
3. **Jitsi:** Usa el dominio público `meet.jit.si` (sin configuración adicional)

---

## 🔗 URLs Importantes

- **Frontend:** http://localhost:5173 (o el puerto que indique Vite)
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **RabbitMQ UI:** http://localhost:15672 (si está corriendo)
