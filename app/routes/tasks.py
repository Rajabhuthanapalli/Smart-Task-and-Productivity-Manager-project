from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.task import Task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=50),
    completed: Optional[bool] = None
):
    query = db.query(Task).filter(Task.is_deleted == False)

    if completed is not None:
        query = query.filter(Task.is_completed == completed)

    total_records = query.count()
    tasks = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "page": page,
        "page_size": page_size,
        "total_records": total_records,
        "tasks": tasks
    }
