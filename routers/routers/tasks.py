from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task
from utils.redis_cache import clear_cache

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.put("/{task_id}")
def update_task(task_id: int, status: str, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    task.status = status
    db.commit()

    # 🔥 Clear cache after update
    clear_cache()

    return {"message": "Task updated successfully"}


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()

    # 🔥 Clear cache after delete
    clear_cache()

    return {"message": "Task deleted successfully"}
