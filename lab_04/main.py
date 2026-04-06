from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import time

# Небольшая задержка, чтобы база успела подняться
time.sleep(5)

DB_USER = os.getenv("DB_USER", "student")
DB_PASSWORD = os.getenv("DB_PASSWORD", "studentpass")
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "task_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    priority = Column(String)


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Tracker API")


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: str


@app.get("/tasks")
def get_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    result = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority
        }
        for task in tasks
    ]
    db.close()
    return result


@app.post("/tasks")
def add_task(task: TaskCreate):
    db = SessionLocal()
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    result = {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "priority": new_task.priority
    }
    db.close()
    return result
