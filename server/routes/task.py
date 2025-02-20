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
    auth_scheme
)
import server.schemas as schemas
import server.service as service
import server.models as models

task_router = APIRouter(prefix="/task", tags=["Task"])


@task_router.get(
    "/list",
    dependencies=[Depends(auth_scheme)],
    summary="List of tasks",
    response_model=List[schemas.BaseTask]
)
async def task_list(current_user: str = Depends(service.get_current_user), db: SessionLocal = Depends(get_db)):
    """
    Получение списка задач пользователя
    """
    tasks = db.query(models.Task).filter(
        models.Task.owner == current_user
    ).all()

    if not tasks:
        return JSONResponse(content=[], status_code=200)

    task_list = [schemas.BaseTask.from_orm(task) for task in tasks]

    return Response(task_list)


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

    return Response(
        schemas.TaskDetail.from_orm(current_task)
    )


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

        return schemas.BaseTask.from_orm(new_task)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {e}"
        )
