import jwt
from datetime import (
    timedelta,
    datetime,
    timezone
)
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from fastapi import (
    HTTPException,
    Depends,
    Response
)

import server.models as models
import server.schemas as schemas
from server.config import (
    SECRET_KEY,
    ALGORITHM,
    auth_scheme,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES
)


def get_username(db: Session, username: str):
    """
    Получение пользователя по логину
    """
    return db.query(models.User).filter(models.User.username == username).first()


async def auth_user(db: Session, user: schemas.BaseUser) -> schemas.CustomAuth:
    """
    Вспомогательная функция для авторизации пользователя
    """
    db_user = get_username(db=db, username=user.username)

    if not db_user or not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=403, detail="Логин или пароль неверны")

    access_token = await create_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = await create_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    return schemas.CustomAuth(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer"
    )


async def create_token(data: dict, expires_delta: timedelta) -> str:
    '''
    Генерация JWT токена
    '''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
