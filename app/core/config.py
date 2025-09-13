import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/simpletaskdb")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
