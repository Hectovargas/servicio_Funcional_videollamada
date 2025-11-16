import jwt
from datetime import datetime, timedelta
from typing import Dict, Any
from app.config import settings


def generate_jitsi_token(
    user_id: str,
    user_name: str,
    room_name: str,
    is_moderator: bool = False,
    is_host: bool = False
) -> str:
    now = datetime.utcnow()
    exp = now + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    
    payload: Dict[str, Any] = {
        "iss": settings.JITSI_APP_ID,
        "aud": settings.JITSI_APP_ID,
        "exp": int(exp.timestamp()),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "sub": settings.JITSI_DOMAIN,
        "room": room_name,
        "context": {
            "user": {
                "id": user_id,
                "name": user_name,
                "moderator": is_moderator or is_host,
            },
            "features": {
                "recording": is_host,
                "livestreaming": is_host,
                "transcription": is_host,
                "outbound-call": is_host,
            },
        },
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def verify_user_jwt(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")
