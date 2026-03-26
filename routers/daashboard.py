from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, or_

from database import get_db
from models.task import Task
from utils.redis_cache import get_cache, set_cache

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/tasks-advanced")
def get_tasks_advanced(
    search: str = Query(None),
    status: str = Query(None),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    limit: int = Query(10),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):

    cache_key = f"{search}-{status}-{sort_by}-{order}-{limit}-{offset}"

    cached_data = get_cache(cache_key)
    if cached_data:
        return {"source": "redis_cache", **cached_data}

    query = db.query(Task)

    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )

    if status:
        query = query.filter(Task.status == status)

    column = Task.created_at if sort_by == "created_at" else Task.status

    if order == "asc":
        query = query.order_by(asc(column))
    else:
        query = query.order_by(desc(column))

    total_count = query.count()
    tasks = query.offset(offset).limit(limit).all()

    result = [
        {
            "task_id": task.id,
            "title": task.title,
            "status": task.status,
            "created_at": task.created_at
        }
        for task in tasks
    ]

    response = {
        "total_tasks": total_count,
        "limit": limit,
        "offset": offset,
        "tasks": result
    }

    set_cache(cache_key, response, ttl=300)

    return {"source": "db", **response}
