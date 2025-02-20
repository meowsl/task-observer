from pydantic import (
    BaseModel,
    Field,
    validator
)
from datetime import datetime


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
