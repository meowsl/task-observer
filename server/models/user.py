from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Text
)
from sqlalchemy.event import listens_for
from sqlalchemy.orm import (
    Mapped,
    relationship
)
from werkzeug.security import generate_password_hash
from uuid import uuid4

from server.config import Base


def get_uuid():
    return uuid4().hex


class User(Base):
    """
    Пользователь
    """

    __tablename__ = "user"

    uuid: Mapped[str] = Column(
        Text,
        primary_key=True,
        default=get_uuid()
    )

    firstname: Mapped[str] = Column(
        String(64),
        nullable=True,
        info={"label": "Имя"}
    )

    username: Mapped[str] = Column(
        String(128),
        unique=True,
        info={"label": "Логин"}
    )

    password: Mapped[str] = Column(
        String,
        info={"label": "Пароль"}
    )

    def __str__(self):
        return self.uuid


@listens_for(User, "before_insert")
def hash_password(mapper, connection, target):
    """
    Хэширование пароля
    """
    if target.password != generate_password_hash(target.password):
        target.password = generate_password_hash(target.password)
