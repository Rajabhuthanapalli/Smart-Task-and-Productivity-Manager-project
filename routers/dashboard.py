from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.task import Task
from models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/user-performance")
def user_performance(db: Session = Depends(get_db)):

    results = db.query(
        User.username,
        func.count(Task.id).label("total_tasks"),
        func.sum(func.case([(Task.status == "completed", 1)], else_=0)).label("completed_tasks")
    ).join(Task, Task.owner_id == User.id) \
     .group_by(User.username) \
     .all()

    response = []

    for row in results:
        completion_rate = 0
        if row.total_tasks > 0:
            completion_rate = (row.completed_tasks / row.total_tasks) * 100

        response.append({
            "username": row.username,
            "total_tasks": row.total_tasks,
            "completed_tasks": row.completed_tasks,
            "completion_rate": round(completion_rate, 2)
        })

    return response
