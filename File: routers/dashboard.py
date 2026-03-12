from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.task import Task

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/tasks-by-status")
def tasks_by_status(
    status: str = Query(None, description="Filter by task status"),
    db: Session = Depends(get_db)
):

    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    tasks = query.all()

    result = []

    for task in tasks:
        result.append({
            "task_id": task.id,
            "title": task.title,
            "status": task.status,
            "created_at": task.created_at
        })

    return {
        "total_tasks": len(result),
        "tasks": result
    }
