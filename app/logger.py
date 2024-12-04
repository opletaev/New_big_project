from datetime import datetime
import logging
from pythonjsonlogger import jsonlogger

from app.core.config import settings


repository_log = logging.getLogger("repository_log")

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()


class RepositoryJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(RepositoryJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )
        if not log_record.get("timestamp"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = RepositoryJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s")
logHandler.setFormatter(formatter)

repository_log.addHandler(logHandler)
repository_log.setLevel(settings.LOG_LEVEL)
