from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


class TaskState(BaseModel):
    id: int
    status: str
    result: int
