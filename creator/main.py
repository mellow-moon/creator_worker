import json
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from faststream.rabbit.fastapi import RabbitRouter, RabbitMessage

from const import Queue
from schema import MessageSchema, TaskState

load_dotenv()

router: RabbitRouter = RabbitRouter(
    os.getenv("RABBIT_URL"), prefix="/creator", tags=["Creator"]
)
app: FastAPI = FastAPI(title="Creator")


@router.post("/create", response_model=MessageSchema)
async def create_task() -> MessageSchema:
    res: RabbitMessage = await router.broker.request(queue=Queue.CREATE)
    return MessageSchema(message=f"Created task with id: {res.body.decode('utf-8')}")


@router.post("/start", response_model=MessageSchema)
async def start_task(task_id: int) -> MessageSchema:
    await router.broker.publish(message=task_id, queue=Queue.START)
    return MessageSchema(message="Task started")


@router.get("/get_task_state", response_model=TaskState)
async def get_task_state(task_id: int) -> TaskState:
    res: RabbitMessage = await router.broker.request(message=task_id, queue=Queue.ONE_TASK)
    json_string: str = res.body.decode("utf-8")
    return TaskState(**json.loads(json_string))


@router.get("/get_state", response_model=list[TaskState])
async def get_state() -> list[TaskState]:
    res: RabbitMessage = await router.broker.request(queue=Queue.ALL_TASK)
    json_string: str = res.body.decode("utf-8")
    return [TaskState(**task) for task in json.loads(json_string)]


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
