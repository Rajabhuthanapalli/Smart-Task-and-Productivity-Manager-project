import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

logger = logging.getLogger("json_logger")
handler = logging.FileHandler("app.json.log")
handler.setFormatter(JsonFormatter())

logger.setLevel(logging.INFO)
logger.addHandler(handler)
