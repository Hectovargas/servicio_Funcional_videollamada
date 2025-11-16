from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from app.config import settings


class VideoRoom:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id", str(uuid.uuid4()))
        self.room_name: str = kwargs["room_name"]
        self.host_id: str = kwargs["host_id"]
        self.workspace_id: Optional[str] = kwargs.get("workspace_id")
        self.channel_id: Optional[str] = kwargs.get("channel_id")
        self.status: str = kwargs.get("status", "active")
        self.created_at: datetime = kwargs.get("created_at", datetime.utcnow())
        self.participants: List[Dict[str, Any]] = kwargs.get("participants", [])


class Database:
    def __init__(self):
        self._rooms: Dict[str, VideoRoom] = {}
        self._participants: Dict[str, List[Dict[str, Any]]] = {}
        
    async def create_room(self, room_data: dict) -> VideoRoom:
        room = VideoRoom(**room_data)
        self._rooms[room.id] = room
        self._participants[room.id] = []
        return room
    
    async def get_room(self, room_id: str) -> Optional[VideoRoom]:
        return self._rooms.get(room_id)
    
    async def get_active_rooms(self) -> List[VideoRoom]:
        return [room for room in self._rooms.values() if room.status == "active"]
    
    async def update_room_status(self, room_id: str, status: str):
        if room_id in self._rooms:
            self._rooms[room_id].status = status
    
    async def add_participant(self, room_id: str, participant_data: dict) -> dict:
        if room_id not in self._participants:
            self._participants[room_id] = []
        
        participant = {
            "id": str(uuid.uuid4()),
            "user_id": participant_data["user_id"],
            "user_name": participant_data["user_name"],
            "joined_at": datetime.utcnow(),
            "left_at": None,
        }
        
        self._participants[room_id].append(participant)
        return participant
    
    async def remove_participant(self, room_id: str, user_id: str):
        if room_id in self._participants:
            for participant in self._participants[room_id]:
                if participant["user_id"] == user_id and participant["left_at"] is None:
                    participant["left_at"] = datetime.utcnow()
                    break
    
    async def get_room_participants(self, room_id: str) -> List[Dict[str, Any]]:
        if room_id not in self._participants:
            return []
        return [p for p in self._participants[room_id] if p["left_at"] is None]


db = Database()
