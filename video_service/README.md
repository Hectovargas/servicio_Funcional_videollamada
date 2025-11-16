# Video Service - Microservicio de Videollamadas con Jitsi

Microservicio FastAPI para gestionar videollamadas usando Jitsi.

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate en Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus valores
```

4. Ejecutar RabbitMQ (Docker):
```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

5. Ejecutar servidor:
```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `POST /api/video/create-room` - Crear sala
- `POST /api/video/join-room` - Unirse a sala
- `GET /api/video/rooms/{room_id}` - Info de sala
- `DELETE /api/video/rooms/{room_id}` - Terminar sala
- `GET /api/video/rooms` - Listar salas activas

Documentación API: http://localhost:8000/docs

## Notas

- La autenticación requiere Bearer token en header `Authorization`
- Por ahora usa base de datos en memoria (se puede integrar Supabase después)
- RabbitMQ debe estar corriendo para publicar eventos
