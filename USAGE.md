# Guía de Uso - Sistema de Videollamadas Jitsi

## Backend (Video Service)

### Instalación

```bash
cd video_service
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o venv\Scripts\activate en Windows

pip install -r requirements.txt
```

### Configuración

1. Copiar `.env.example` a `.env` y ajustar valores:
```bash
cp .env.example .env
```

2. Iniciar RabbitMQ:
```bash
docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

3. Ejecutar servidor:
```bash
uvicorn app.main:app --reload --port 8000
```

### Endpoints

- Documentación: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Nota sobre Autenticación

Por ahora el backend acepta cualquier token Bearer. Para desarrollo puedes usar `test-token`.

## Frontend

### Uso del Componente

```jsx
import { VideoCall } from '@/components/video';

function App() {
  return <VideoCall />;
}
```

### Estructura

- `VideoCall.jsx` - Componente principal
- `PreCallScreen.jsx` - Pantalla de inicio
- `CallControls.jsx` - Controles flotantes
- `videoService.js` - Servicio API

### Requisitos

- React 18+
- Shadcn UI componentes: Button, Input, Label, Card
- Lucide React para iconos
- Tailwind CSS

## Prueba Completa

1. Backend corriendo en http://localhost:8000
2. Frontend en http://localhost:5173
3. Abrir navegador → ingresar nombre de sala y usuario
4. Click "Iniciar Videollamada"
5. Verificar eventos en RabbitMQ: http://localhost:15672 (guest/guest)
