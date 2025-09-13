from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.db.session import SessionLocal
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.task import get_task, get_tasks, create_task, update_task, delete_task
from app.utils.security import get_current_user_from_cookie

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tasks/ui", response_class=HTMLResponse)
def tasks_ui(request: Request, db: Session = Depends(get_db)):
    current_user: Optional[User] = get_current_user_from_cookie(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    tasks = get_tasks(db, owner_id=current_user.id)
    return templates.TemplateResponse("tasks_list.html", {"request": request, "tasks": tasks, "current_user": current_user})

@router.get("/tasks/create", response_class=HTMLResponse)
def create_task_form(request: Request, db: Session = Depends(get_db)):
    current_user: Optional[User] = get_current_user_from_cookie(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("task_form.html", {"request": request, "current_user": current_user})

@router.post("/tasks/create")
def create_task_submit(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    deadline: str = Form(""),
    completed: str = Form("false"),
    db: Session = Depends(get_db)
):
    current_user: Optional[User] = get_current_user_from_cookie(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Parse deadline from form
    deadline_date = None
    if deadline:
        try:
            deadline_date = date.fromisoformat(deadline)
        except ValueError:
            return RedirectResponse(url="/tasks/create?error=Invalid deadline format", status_code=303)
    
    task_data = TaskCreate(
        title=title,
        description=description if description else None,
        completed=completed.lower() == "true",
        deadline=deadline_date
    )
    
    create_task(db, task_data, owner_id=current_user.id)
    return RedirectResponse(url="/tasks/ui?msg=Task created successfully!", status_code=303)

@router.get("/tasks/{task_id}", response_class=HTMLResponse)
def view_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    current_user: Optional[User] = get_current_user_from_cookie(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    task = get_task(db, task_id)
    if not task:
        return RedirectResponse(url="/tasks/ui?error=Task not found", status_code=303)
    
    # Validate ownership
    if task.owner_id != current_user.id:
        return RedirectResponse(url="/tasks/ui?error=Access denied", status_code=303)
    
    return templates.TemplateResponse("task_view.html", {"request": request, "task": task, "current_user": current_user})

@router.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
def edit_task_form(request: Request, task_id: int, db: Session = Depends(get_db)):
    current_user: Optional[User] = get_current_user_from_cookie(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    task = get_task(db, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return templates.TemplateResponse("task_form.html", {"request": request, "task": task, "current_user": current_user})

@router.post("/tasks/{task_id}/edit")
def edit_task_submit(
    request: Request,
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    deadline: str = Form(""),
    completed: str = Form("false"),
    db: Session = Depends(get_db)
):
    current_user: Optional[User] = get_current_user_from_cookie(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    db_task = get_task(db, task_id)
    if not db_task or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Parse deadline from string
    deadline_date = None
    if deadline:
        try:
            deadline_date = date.fromisoformat(deadline)
        except ValueError:
            # Handle invalid date format - could add flash message here
            pass
    
    task_updates = TaskUpdate(
        title=title,
        description=description if description else None,
        deadline=deadline_date,
        completed=completed.lower() == "true"
    )
    
    update_task(db, db_task, task_updates)
    return RedirectResponse(url=f"/tasks/{task_id}?msg=Task updated successfully!", status_code=303)

@router.post("/tasks/{task_id}/delete")
def delete_task_submit(request: Request, task_id: int, db: Session = Depends(get_db)):
    current_user: Optional[User] = get_current_user_from_cookie(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    db_task = get_task(db, task_id)
    if not db_task or db_task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    delete_task(db, db_task)
    return RedirectResponse(url="/tasks/ui?msg=Task deleted successfully!", status_code=303)
