from sqlalchemy.orm import Session
from . import models

def get_tasks(db: Session, completed: bool | None = None, skip: int = 0, limit: int = 10):
    query = db.query(models.Task)

    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    return query.offset(skip).limit(limit).all()
