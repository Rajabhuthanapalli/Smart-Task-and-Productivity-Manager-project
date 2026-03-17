from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models.task import Task

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/tasks-paginated")
def get_tasks_paginated(
    limit: int = Query(10, description="Number of records to fetch"),
    offset: int = Query(0, description="Number of records to skip"),
    db: Session = Depends(get_db)
):

    query = db.query(Task)

    total_count = query.count()

    tasks = query.offset(offset).limit(limit).all()

    result = []

    for task in tasks:
        result.append({
            "task_id": task.id,
            "title": task.title,
            "status": task.status,
            "created_at": task.created_at
        })

    return {
        "total_tasks": total_count,
        "limit": limit,
        "offset": offset,
        "tasks": result
    }
