import json
from typing import Dict, Any
import aio_pika
from aio_pika import Message
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class RabbitMQPublisher:
    def __init__(self):
        self._connection = None
        self._channel = None
        self._exchange = None
    
    async def connect(self):
        try:
            self._connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self._channel = await self._connection.channel()
            self._exchange = await self._channel.declare_exchange(
                settings.RABBITMQ_EXCHANGE,
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )
            logger.info("Conectado a RabbitMQ")
        except Exception as e:
            logger.error(f"Error conectando a RabbitMQ: {e}")
            self._connection = None
            self._channel = None
            self._exchange = None
    
    async def publish(self, routing_key: str, message: Dict[str, Any]):
        if not self._exchange:
            try:
                await self.connect()
            except Exception as e:
                logger.error(f"No se pudo conectar a RabbitMQ: {e}")
                return
        
        try:
            message_body = json.dumps(message, default=str)
            await self._exchange.publish(
                Message(
                    message_body.encode(),
                    content_type="application/json"
                ),
                routing_key=routing_key
            )
            logger.info(f"Evento publicado: {routing_key}")
        except Exception as e:
            logger.error(f"Error publicando evento: {e}")
    
    async def close(self):
        if self._connection:
            await self._connection.close()


rabbitmq_publisher = RabbitMQPublisher()
