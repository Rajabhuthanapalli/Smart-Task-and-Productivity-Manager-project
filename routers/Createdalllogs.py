from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import json
import csv
import io

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/export/csv")
def export_logs_csv(
    level: str = Query(None),
    keyword: str = Query(None)
):
    output = io.StringIO()
    writer = csv.writer(output)

    # CSV Header
    writer.writerow(["time", "level", "message"])

    try:
        with open("app.json.log", "r") as file:
            lines = file.readlines()

        for line in lines:
            log = json.loads(line.strip())

            if level and log.get("level") != level:
                continue

            if keyword and keyword.lower() not in log.get("message", "").lower():
                continue

            writer.writerow([
                log.get("time"),
                log.get("level"),
                log.get("message")
            ])

    except Exception as e:
        return {"error": str(e)}

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=logs.csv"}
    )
