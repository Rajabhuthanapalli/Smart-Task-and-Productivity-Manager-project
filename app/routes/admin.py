from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import csv
import io

from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.core.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/export-analytics")
def export_analytics(
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: Session = Depends(get_db),
    admin_user = Depends(require_admin)
):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    results = db.query(
        User.username,
        func.count(Task.id).label("total_tasks"),
        func.sum(func.case([(Task.is_completed == True, 1)], else_=0)).label("completed_tasks")
    ).join(Task, Task.owner_id == User.id) \
     .filter(Task.created_at.between(start, end)) \
     .group_by(User.username) \
     .all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Username", "Total Tasks", "Completed Tasks"])

    for row in results:
        writer.writerow([row.username, row.total_tasks, row.completed_tasks])

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=analytics_report.csv"}
    )
