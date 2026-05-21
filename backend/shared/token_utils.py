import jwt
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PRIVATE_KEY = (BASE / "keys" / "private.pem").read_bytes()


def issue_jwt(payload: dict, expiry_seconds: int):
    now = int(time.time())

    payload.update({
        "iat": now,
        "exp": now + expiry_seconds
    })

    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")