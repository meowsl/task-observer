from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DateTime
)
from sqlalchemy.orm import Mapped

from server.config import (
    Base,
    TIMEZONE
)


class Task(Base):
    """
    Задача
    """

    __tablename__ = "task"

    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = Column(
        String(256),
        info={"label": "Наименование"}
    )

    description: Mapped[str] = Column(
        Text,
        nullable=True,
        info={"label": "Описание"}
    )

    date: Mapped[datetime] = Column(
        DateTime,
        default=datetime.now(TIMEZONE)
    )

    def __str__(self):
        return self.name
