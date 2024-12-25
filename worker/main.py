import os
from typing import Sequence, Union

from dotenv import load_dotenv
from faststream import FastStream, Depends
from faststream.rabbit import RabbitBroker
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Task
from const import TaskStatus, Queue
from services import get_db_session, fib_async

load_dotenv()

broker: RabbitBroker = RabbitBroker(os.getenv("RABBIT_URL"))
app: FastStream = FastStream(broker)


@broker.subscriber(Queue.CREATE)
async def create_task(session: AsyncSession = Depends(get_db_session)) -> int:
    new_task: Task = Task(status=TaskStatus.CREATED)
    session.add(new_task)
    await session.flush()
    task_id: int = new_task.id
    await session.commit()
    return task_id


@broker.subscriber(Queue.START)
async def start_task(
    task_id: int, session: AsyncSession = Depends(get_db_session)
) -> None:
    await session.execute(
        update(Task).where(Task.id == task_id).values(status=TaskStatus.STARTED)
    )
    await session.commit()

    result: int = await fib_async(40)

    await session.execute(
        update(Task)
        .where(Task.id == task_id)
        .values(result=result, status=TaskStatus.DONE)
    )
    await session.commit()


@broker.subscriber(Queue.ONE_TASK)
async def get_task_state(
    task_id: int, session: AsyncSession = Depends(get_db_session)
) -> dict[str, Union[int, str]]:
    task: Task = await session.scalar(select(Task).where(Task.id == task_id))
    return {"id": task.id, "status": task.status, "result": task.result}


@broker.subscriber(Queue.ALL_TASK)
async def get_state(
    session: AsyncSession = Depends(get_db_session),
) -> list[dict[str, Union[int, str]]]:
    tasks: Sequence[Task] = (
        await session.scalars(select(Task).order_by(Task.id))
    ).all()
    return [
        {"id": task.id, "status": task.status, "result": task.result} for task in tasks
    ]
