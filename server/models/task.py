from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import (
    Mapped,
    relationship
)
import enum

from .user import User
from server.config import (
    Base,
    TIMEZONE
)


class TaskStatus(enum.Enum):
    PLANNED = "Запланирована"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершена"


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

    owner_id: Mapped[int] = Column(
        Integer,
        ForeignKey("user.uuid"),
        info={"label": "Автор"}
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

    status: Mapped[TaskStatus] = Column(
        Enum(TaskStatus),
        default=TaskStatus.PLANNED,
        info={"label": "Статус"}
    )

    owner = relationship(
        User,
        back_populates="tasks"
    )

    def __str__(self):
        return self.name
