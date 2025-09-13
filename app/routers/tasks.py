from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import SessionLocal
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.crud.task import get_task, get_tasks, create_task, update_task, delete_task
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks", response_model=TaskOut)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_task(db, task, owner_id=current_user.id)

@router.get("/tasks", response_model=List[TaskOut])
def list_tasks(skip: int = 0, limit: int = 100, completed: Optional[bool] = Query(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = get_tasks(db, owner_id=current_user.id, skip=skip, limit=limit)
    if completed is not None:
        tasks = [task for task in tasks if task.completed == completed]
    return tasks

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task_endpoint(task_id: int, updates: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = get_task(db, task_id)
    if not db_task or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task(db, db_task, updates)

@router.delete("/tasks/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_task = get_task(db, task_id)
    if not db_task or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task(db, db_task)
    return {"detail": "Task deleted"}
