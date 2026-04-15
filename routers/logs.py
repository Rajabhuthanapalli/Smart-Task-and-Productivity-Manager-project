from fastapi import APIRouter, Query
import json

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/recent")
def get_recent_logs(limit: int = Query(20)):
    logs = []

    try:
        with open("app.json.log", "r") as file:
            lines = file.readlines()

        for line in lines[-limit:]:
            logs.append(json.loads(line.strip()))
    except Exception as e:
        return {"error": str(e)}

    return {
        "total_logs": len(logs),
        "logs": logs
    }
