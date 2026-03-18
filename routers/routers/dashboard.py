from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from database import get_db
from models.task import Task

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/tasks-sorted")
def get_tasks_sorted(
    sort_by: str = Query("created_at", description="Field to sort by"),
    order: str = Query("desc", description="asc or desc"),
    db: Session = Depends(get_db)
):

    query = db.query(Task)

    if sort_by == "created_at":
        sort_column = Task.created_at
    elif sort_by == "status":
        sort_column = Task.status
    else:
        sort_column = Task.created_at

    if order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

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
