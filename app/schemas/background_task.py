from pydantic import BaseModel


class TaskStatus(BaseModel):
    task_status: int
