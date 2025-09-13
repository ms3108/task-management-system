from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User, Base
from app.utils.security import hash_password, verify_password, create_access_token, get_current_user_from_cookie
from pydantic import BaseModel

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# GET endpoints for rendering templates
@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_from_cookie(request, db)
    return templates.TemplateResponse("register.html", {"request": request, "current_user": current_user})

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_from_cookie(request, db)
    return templates.TemplateResponse("login.html", {"request": request, "current_user": current_user})

# POST endpoints for form data
@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    db_user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Redirect to login after successful registration
    return RedirectResponse(url="/login?msg=Account created successfully! Please log in.", status_code=303)

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": db_user.username})
    
    # Set cookie and redirect to tasks
    resp = RedirectResponse(url="/tasks/ui?msg=Welcome back!", status_code=303)
    resp.set_cookie("access_token", f"Bearer {access_token}", httponly=True)
    return resp

@router.get("/logout")
def logout():
    resp = RedirectResponse(url="/?msg=Logged out successfully!", status_code=303)
    resp.delete_cookie("access_token")
    return resp
