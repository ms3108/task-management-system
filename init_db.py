#!/usr/bin/env python3

"""
Database initialization script
This script creates all the database tables using SQLAlchemy's create_all() method
"""

import sys
import os
sys.path.append('/app')

from app.db.session import engine
from app.db.base import Base

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
