from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select

from app.models import User
from app.models.task import Task
from app.schemas.task import TaskCreateResponse, TaskCreateRequest, TaskUpdateRequest, TasksRequest, TaskResponse
from app.core.db import session


def create_new_task(task: TaskCreateRequest) -> TaskCreateResponse:
    db_user_id = session.execute(
        select(User).where(User.user_id == task.user_id)
    )
    db_user = db_user_id.scalars().first()
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail='Такого пользователя не существует!',
        )

    db_task_model = Task(
        name=task.name,
        description=task.description,
        status=task.status,
        urgency=task.urgency,
        user_id=task.user_id,
    )

    session.add(db_task_model)
    session.commit()

    created_task_data: TaskCreateResponse = TaskCreateResponse(
        name=db_task_model.name,
        description=db_task_model.description,
        status=db_task_model.status,
        urgency=db_task_model.urgency,
        created_at=db_task_model.created_at,
        last_notification=db_task_model.last_notification,
        user_id=db_task_model.user_id,
    )
    return created_task_data


# def get_tasks_userid(user_id):
#     tasks = session.execute(
#         select(Task).where(Task.user_id == user_id))
#     all_tasks = tasks.scalars().all()
#     return all_tasks


def get_task_id(task_id: int):
    task_db = session.execute(
        select(Task).where(Task.id == task_id)
    )
    task = task_db.scalars().first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail='Такой задачи не существует!',
        )
    return task


def update_task(task_id: int, task: TaskUpdateRequest) -> TaskResponse:
    task_model = get_task_id(task_id)
    obj_data = jsonable_encoder(task_model)

    update_data = task.dict(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(task_model, field, update_data[field])

    session.add(task_model)
    session.commit()

    change_task: TaskResponse = TaskResponse(
        name=task_model.name,
        description=task_model.description,
        status=task_model.status,
        user_id=task_model.user_id,
        urgency=task_model.urgency,
        last_notification=task_model.last_notification,
        created_at=task_model.created_at,
        id=task_model.id,
    )
    return change_task


def task_delete(task_id: int):
    task_id = get_task_id(task_id)
    if task_id is None:
        raise HTTPException(
            status_code=404,
            detail='Такой задачи не существует!',
        )
    session.delete(task_id)
    session.commit()
    return task_id


def list_tasks(params: TasksRequest):
    sql_query = select(Task)

    if params.user_id is not None:
        sql_query = sql_query.where(Task.user_id == params.user_id)
    if params.task_id is not None:
        sql_query = sql_query.where(Task.id == params.task_id)
    if params.status is not None:
        sql_query = sql_query.where(Task.status == params.status)

    tasks = session.execute(sql_query)
    all_tasks = tasks.scalars().all()
    return all_tasks
