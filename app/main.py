from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.routers import auth, tasks, tasks_ui
from app.utils.security import get_current_user_from_cookie
from app.db.session import SessionLocal, engine
from app.db.base import Base

app = FastAPI()

# Create database tables on startup
@app.on_event("startup")
def create_tables():
    # Import models to register them with SQLAlchemy
    from app.models import user, task
    Base.metadata.create_all(bind=engine)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(tasks_ui.router)

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_from_cookie(request, db)
    return templates.TemplateResponse("index.html", {"request": request, "current_user": current_user})
