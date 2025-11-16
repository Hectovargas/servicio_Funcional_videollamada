from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateRoomRequest(BaseModel):
    room_name: str
    user_id: str
    user_name: str
    is_host: bool = True
    workspace_id: Optional[str] = None
    channel_id: Optional[str] = None


class JoinRoomRequest(BaseModel):
    room_id: str
    user_id: str
    user_name: str


class RoomResponse(BaseModel):
    room_id: str
    room_name: str
    host_id: str
    workspace_id: Optional[str]
    channel_id: Optional[str]
    status: str
    created_at: datetime
    jitsi_url: str
    jwt_token: Optional[str] = None


class ParticipantResponse(BaseModel):
    participant_id: str
    user_id: str
    user_name: str
    room_id: str
    joined_at: datetime
    jwt_token: Optional[str] = None


class RoomInfoResponse(BaseModel):
    room_id: str
    room_name: str
    host_id: str
    status: str
    created_at: datetime
    participants: list[ParticipantResponse]
