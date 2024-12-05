from datetime import datetime
import os
import subprocess

from app.core.config import settings


def create_pg_backup_filenames(backup_dir: str) -> tuple[str]:
    timestamp = datetime.now().strftime("%d.%m.%Y_%H:%M:%S")
    pg_dump_file = os.path.join(backup_dir, f"pg_dump_{timestamp}.sql")
    backup_file = os.path.join(backup_dir, f"pg_backup_{timestamp}.tar.gz")
    return pg_dump_file, backup_file


def run_pg_dump(pg_dump_file: str) -> None:
    command_dump = f"PGPASSWORD={settings.DB_PASS} pg_dumpall -U {settings.DB_USER} -p {settings.DB_PORT} -h localhost > {pg_dump_file}"
    subprocess.run(command_dump, shell=True, check=True)


def archive_backup(
    backup_file: str,
    pg_dump_file: str,
    backup_dir: str,
) -> None:
    command_archive = f"tar -czf {backup_file} -C {backup_dir} {pg_dump_file}"
    subprocess.run(command_archive, shell=True, check=True)
