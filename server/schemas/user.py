from pydantic import (
    BaseModel,
    Field,
    validator
)


class BaseUser(BaseModel):
    """
    Базовая схема данных пользователя

    Note:
        Используется для авторизации
    """
    username: str
    password: str


class UserCreate(BaseModel):
    """
    Схема данных для регистрации нового пользователя
    """
    username: str = Field(
        ...,
        min_length=4,
        max_length=128,
        description="Логин пользователя"
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Пароль пользователя"
    )

    password_confirm: str = Field(
        ...,
        min_length=8,
        description="Подтверждение пароля"
    )

    firstname: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Имя пользователя"
    )

    @validator("password_confirm")
    def passwords_match(cls, v, values, **kwargs):
        other_password = values.get("password")
        if other_password != v:
            raise ValueError("Пароли не совпадают")
        return v

    class Config:
        from_attributes = True


class UserDetail(BaseModel):
    """
    Модель для получения данных пользователя
    """
    firstname: str
    username: str

    class Config:
        from_attributes = True


class CustomAuth(BaseModel):
    """
    Базовая схема данных для успешной авторизации
    """
    access_token: str
    refresh_token: str
    token_type: str
