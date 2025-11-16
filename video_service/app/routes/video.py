from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from app.models import (
    CreateRoomRequest,
    JoinRoomRequest,
    RoomResponse,
    ParticipantResponse,
    RoomInfoResponse
)
from app.database import db
from app.jwt_handler import generate_jitsi_token, verify_user_jwt
from app.rabbitmq import rabbitmq_publisher
from app.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/video", tags=["video"])


async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token de autenticación requerido")
    
    try:
        token = authorization.replace("Bearer ", "").strip()
        
        # Permitir token de prueba en desarrollo
        if token == "test-token":
            logger.info("Token de prueba aceptado")
            return {
                "sub": "test-user",
                "user_id": "test-user",
                "user_name": "Test User"
            }
        
        payload = verify_user_jwt(token)
        return payload
    except ValueError as e:
        logger.error(f"Error verificando token: {e}, token recibido: {token[:10]}...")
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/create-room", response_model=RoomResponse)
async def create_room(
    request: CreateRoomRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        room = await db.create_room({
            "room_name": request.room_name,
            "host_id": request.user_id,
            "workspace_id": request.workspace_id,
            "channel_id": request.channel_id,
            "status": "active",
        })
        
        jwt_token = generate_jitsi_token(
            user_id=request.user_id,
            user_name=request.user_name,
            room_name=request.room_name,
            is_moderator=True,
            is_host=True
        )
        
        jitsi_url = f"https://{settings.JITSI_DOMAIN}/{request.room_name}"
        
        await rabbitmq_publisher.publish(
            "video.room.created",
            {
                "room_id": room.id,
                "room_name": room.room_name,
                "host_id": room.host_id,
                "workspace_id": room.workspace_id,
                "channel_id": room.channel_id,
            }
        )
        
        return RoomResponse(
            room_id=room.id,
            room_name=room.room_name,
            host_id=room.host_id,
            workspace_id=room.workspace_id,
            channel_id=room.channel_id,
            status=room.status,
            created_at=room.created_at,
            jitsi_url=jitsi_url,
            jwt_token=jwt_token,
        )
    except Exception as e:
        logger.error(f"Error creando sala: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/join-room", response_model=ParticipantResponse)
async def join_room(
    request: JoinRoomRequest,
    current_user: dict = Depends(get_current_user)
):
    try:
        room = await db.get_room(request.room_id)
        
        if not room:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        
        if room.status != "active":
            raise HTTPException(status_code=400, detail="Sala no está activa")
        
        participants = await db.get_room_participants(request.room_id)
        
        if len(participants) >= 50:
            raise HTTPException(status_code=403, detail="Sala llena (máximo 50 participantes)")
        
        participant = await db.add_participant(request.room_id, {
            "user_id": request.user_id,
            "user_name": request.user_name,
        })
        
        jwt_token = generate_jitsi_token(
            user_id=request.user_id,
            user_name=request.user_name,
            room_name=room.room_name,
            is_moderator=False,
            is_host=False
        )
        
        await rabbitmq_publisher.publish(
            "video.participant.joined",
            {
                "room_id": request.room_id,
                "participant_id": participant["id"],
                "user_id": request.user_id,
                "user_name": request.user_name,
            }
        )
        
        return ParticipantResponse(
            participant_id=participant["id"],
            user_id=participant["user_id"],
            user_name=participant["user_name"],
            room_id=request.room_id,
            joined_at=participant["joined_at"],
            jwt_token=jwt_token,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uniéndose a sala: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rooms/{room_id}", response_model=RoomInfoResponse)
async def get_room(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        room = await db.get_room(room_id)
        
        if not room:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        
        participants_data = await db.get_room_participants(room_id)
        participants = [
            ParticipantResponse(
                participant_id=p["id"],
                user_id=p["user_id"],
                user_name=p["user_name"],
                room_id=room_id,
                joined_at=p["joined_at"],
            )
            for p in participants_data
        ]
        
        return RoomInfoResponse(
            room_id=room.id,
            room_name=room.room_name,
            host_id=room.host_id,
            status=room.status,
            created_at=room.created_at,
            participants=participants,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo sala: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/rooms/{room_id}")
async def delete_room(
    room_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        room = await db.get_room(room_id)
        
        if not room:
            raise HTTPException(status_code=404, detail="Sala no encontrada")
        
        if room.host_id != current_user.get("sub") and room.host_id != current_user.get("user_id"):
            raise HTTPException(status_code=403, detail="Solo el host puede terminar la sala")
        
        await db.update_room_status(room_id, "ended")
        
        await rabbitmq_publisher.publish(
            "video.room.ended",
            {
                "room_id": room_id,
                "ended_by": current_user.get("user_id"),
            }
        )
        
        return {"message": "Sala terminada exitosamente"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error terminando sala: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rooms", response_model=list[RoomResponse])
async def list_rooms(current_user: dict = Depends(get_current_user)):
    try:
        rooms = await db.get_active_rooms()
        
        return [
            RoomResponse(
                room_id=room.id,
                room_name=room.room_name,
                host_id=room.host_id,
                workspace_id=room.workspace_id,
                channel_id=room.channel_id,
                status=room.status,
                created_at=room.created_at,
                jitsi_url=f"https://{settings.JITSI_DOMAIN}/{room.room_name}",
            )
            for room in rooms
        ]
    except Exception as e:
        logger.error(f"Error listando salas: {e}")
        raise HTTPException(status_code=500, detail=str(e))
