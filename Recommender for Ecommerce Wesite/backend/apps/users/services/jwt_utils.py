import jwt
from datetime import datetime, timedelta
from django.conf import settings

SECRET = getattr(settings, 'SECRET_KEY', 'dev-secret')
ALGORITHM = 'HS256'


def create_jwt_token(customer_id, expires_minutes=60*24*7):
    payload = {
        'sub': customer_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=expires_minutes)
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except Exception:
        return None
