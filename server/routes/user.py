import jwt
from datetime import timedelta
from typing import Annotated
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Response,
    Request
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from server.config import (
    SessionLocal,
    get_db,
    auth_scheme,
    SECRET_KEY,
    ALGORITHM,

)
import server.schemas as schemas
import server.service as service
import server.models as models

user_router = APIRouter(prefix="/user", tags=["Auth"])


@user_router.post("/login", summary="Authorization")
async def login(request: Request, user: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response, db: SessionLocal = Depends(get_db)) -> schemas.CustomAuth:
    """
    Авторизация пользователя
    """
    return await service.auth_user(db=db, user=user)


@user_router.post("/register", summary="Register for new user")
async def register(request: Request, user: schemas.UserCreate, response: Response, db: SessionLocal = Depends(get_db)):
    """
    Регистрация нового пользователя
    """

    if service.get_username(db=db, username=user.username):
        raise HTTPException(
            status_code=400,
            detail="Пользователь с указанным логином уже зарегистрирован."
        )

    new_user = models.User(
        username=user.username,
        firstname=user.firstname,
        password=user.password
    )

    db.add(new_user)
    db.commit()

    return JSONResponse(
        status_code=201,
        content=(await service.auth_user(db=db, user=user)).dict()
    )
