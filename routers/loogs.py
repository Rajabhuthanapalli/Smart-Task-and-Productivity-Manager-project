from fastapi import APIRouter, Query
import json

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/advanced-search")
def advanced_search_logs(
    keyword: str = Query(None, description="Search keyword"),
    level: str = Query(None),
    limit: int = Query(50)
):
    logs = []

    try:
        with open("app.json.log", "r") as file:
            lines = file.readlines()

        for line in reversed(lines):
            log = json.loads(line.strip())

            if keyword and keyword.lower() not in log.get("message", "").lower():
                continue

            if level and log.get("level") != level:
                continue

            logs.append(log)

            if len(logs) >= limit:
                break

    except Exception as e:
        return {"error": str(e)}

    return {
        "results_count": len(logs),
        "logs": logs
    }
