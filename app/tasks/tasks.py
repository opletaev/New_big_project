from subprocess import CalledProcessError
import os

from app.adapters import backup_helpers
from app.core.config import settings
from app.core.logger import celery_log
from app.tasks.celery import celery


@celery.task
def pg_backup() -> bool:
    backup_dir = settings.DB_BACKUP_DIR
    try:
        celery_log.info("Creating a backup file name with the current date and time")
        pg_dump_file, backup_file = backup_helpers.create_pg_backup_filenames(
            backup_dir
        )

        celery_log.info("Backing up all databases")
        backup_helpers.run_pg_dump(pg_dump_file)

        celery_log.info("Backup archiving")
        backup_helpers.archive_backup(backup_file, pg_dump_file, backup_dir)

        celery_log.info("Deleting pg_dump_file")
        os.remove(pg_dump_file)

        celery_log.info(
            "Backup completed successfully",
            extra={"backup_file": backup_file},
        )
        return True

    except CalledProcessError as e:
        return celery_log.error(
            f"An error occurred while backing up the database", exc_info=True
        )
    except Exception as e:
        return celery_log.error(f"An unexpected error occurred", exc_info=True)
