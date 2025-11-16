from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import video
from app.rabbitmq import rabbitmq_publisher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando Video Service...")
    await rabbitmq_publisher.connect()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Cerrando Video Service...")
    await rabbitmq_publisher.close()


@app.get("/")
async def root():
    return {"message": "Video Service API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
