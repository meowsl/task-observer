from pydantic import (
    BaseModel,
    Field,
    validator,
)
from typing import Optional
from datetime import datetime
from server.models import TaskStatus


class BaseTask(BaseModel):
    """
    Базовая схема задач
    """
    id: int
    name: str
    date: datetime

    class Config:
        from_attributes = True


class TaskDetail(BaseTask):
    """
    Детализированная схема задач
    """
    description: str
    status: TaskStatus

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    """
    Схема для создания новой задачи
    """
    name: str = Field(
        ...,
        max_length=256,
        description="Название задачи"
    )

    description: str = Field(
        description="Описание задачи"
    )


class TaskUpdate(BaseModel):
    """
    Схема для частичного обновления задачи
    """
    name: Optional[str] = Field(
        None,
        max_length=256,
        description="Новое название задачи"
    )
    description: Optional[str] = Field(
        None,
        description="Новое описание задачи"
    )
    status: Optional[str] = Field(
        None,
        description="Новый статус"
    )
