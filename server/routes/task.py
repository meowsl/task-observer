from typing import (
    Annotated,
    List
)
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Response,
    Request
)
from fastapi.responses import JSONResponse
from server.config import (
    SessionLocal,
    get_db,
    auth_scheme,
    token_required
)
import server.schemas as schemas
import server.service as service
import server.models as models

task_router = APIRouter(prefix="/task", tags=["Task"])


@token_required
@task_router.get(
    "/list",
    dependencies=[Depends(auth_scheme)],
    summary="List of tasks",
    response_model=List[schemas.TaskDetail]
)
async def task_list(current_user: str = Depends(service.get_current_user), db: SessionLocal = Depends(get_db)):
    """
    Получение списка задач пользователя
    """
    tasks = db.query(models.Task).filter(
        models.Task.owner == current_user
    ).all()
    if not tasks:
        return []

    return [schemas.TaskDetail.from_orm(task) for task in tasks]


@task_router.get(
    "/{task_id}",
    dependencies=[Depends(auth_scheme)],
    summary="Detail for task",
    response_model=schemas.TaskDetail
)
async def task_detail(task_id: int, current_user: str = Depends(service.get_current_user), db: SessionLocal = Depends(get_db)):
    """
    Получение деталей задачи
    """
    current_task = db.query(models.Task).filter(
        models.Task.owner == current_user,
        models.Task.id == task_id
    ).first()

    if not current_task:
        raise HTTPException(status_code=404, detail="Задачи не существует")

    return schemas.TaskDetail.from_orm(current_task)


@task_router.post(
    "/create",
    dependencies=[Depends(auth_scheme)],
    summary="Create new task",
)
async def task_create(new_task: schemas.TaskCreate, current_user: str = Depends(service.get_current_user), db: SessionLocal = Depends(get_db)):
    """
    Создание новой задачи
    """
    try:
        new_task = models.Task(
            owner=current_user,
            name=new_task.name,
            description=new_task.description if new_task.description else None
        )

        db.add(new_task)
        db.commit()

        return schemas.TaskDetail.from_orm(new_task)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка сервера: {e}"
        )


@task_router.delete(
    "/{task_id}",
    dependencies=[Depends(auth_scheme)],
    summary="Delete current task"
)
async def task_delete(task_id: int, current_user: str = Depends(service.get_current_user), db: SessionLocal = Depends(get_db)):
    """
    Удаление определенной задачи
    """
    current_task = db.query(models.Task).filter(
        models.Task.owner == current_user,
        models.Task.id == task_id
    ).first()

    if not current_task:
        raise HTTPException(status_code=404, detail="Задачи не существует")

    db.delete(current_task)
    db.commit()

    return Response(
        status_code=204
    )


@task_router.patch(
    "/{task_id}",
    dependencies=[Depends(auth_scheme)],
    summary="Partial update of a task",
    response_model=schemas.TaskDetail
)
async def task_update(
    task_id: int,
    updates: schemas.TaskUpdate,
    current_user: str = Depends(service.get_current_user),
    db: SessionLocal = Depends(get_db)
):
    """
    Частичное обновление задачи
    """
    current_task = db.query(models.Task).filter(
        models.Task.owner == current_user,
        models.Task.id == task_id
    ).first()

    if not current_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if updates.name is not None:
        current_task.name = updates.name
    if updates.description is not None:
        current_task.description = updates.description
    if updates.status is not None:
        status_mapping = {status.value: status for status in models.TaskStatus}
        current_task.status = status_mapping.get(updates.status)

    try:
        db.commit()
        db.refresh(current_task)
        return schemas.TaskDetail.from_orm(current_task)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка сервера: {e}"
        )
