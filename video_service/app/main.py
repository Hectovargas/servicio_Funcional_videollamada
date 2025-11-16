from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import video

app = FastAPI(
    title="Video Service API",
    description="Microservicio para gestión de videollamadas con Jitsi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router)


@app.get("/")
async def root():
    return {"message": "Video Service API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
