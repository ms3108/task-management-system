from pydantic import BaseModel
from typing import Optional
from datetime import date

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    deadline: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    deadline: Optional[date] = None

class TaskOut(TaskBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
