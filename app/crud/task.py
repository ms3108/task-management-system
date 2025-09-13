from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional

def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    return db.query(Task).filter(Task.owner_id == owner_id).offset(skip).limit(limit).all()

def create_task(db: Session, task: TaskCreate, owner_id: int) -> Task:
    db_task = Task(**task.dict(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, db_task: Task, updates: TaskUpdate) -> Task:
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: Task) -> None:
    db.delete(db_task)
    db.commit()
