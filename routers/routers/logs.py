from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import json
import io

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/export/json")
def export_logs_json(
    level: str = Query(None),
    keyword: str = Query(None)
):
    logs = []

    try:
        with open("app.json.log", "r") as file:
            lines = file.readlines()

        for line in lines:
            log = json.loads(line.strip())

            if level and log.get("level") != level:
                continue

            if keyword and keyword.lower() not in log.get("message", "").lower():
                continue

            logs.append(log)

    except Exception as e:
        return {"error": str(e)}

    output = io.StringIO()
    json.dump(logs, output, indent=2)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=logs.json"}
    )
