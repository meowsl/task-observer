from fastapi.security import OAuth2PasswordBearer
import jwt
from functools import wraps

auth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Проверка на истечение срока действия токена
        if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            return False
        return payload
    except Exception:
        return False


def token_required(func):
    """
    Декоратор для проверки токена
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        token = kwargs.get('token', None) or args[0]
        if not token or not verify_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await func(*args, **kwargs)
    return wrapper
