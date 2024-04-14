import os
from datetime import datetime
import shutil

DB_CONTAINER = "postgres_songs"
WEB_CONTAINER = "backend_songs"
MAX_BACKUPS = 3

BACKUP_DB_DIR = "backup_db"
BACKUP_FILES_DIR = "backup_files"
os.makedirs(BACKUP_DB_DIR, exist_ok=True)
os.makedirs(BACKUP_FILES_DIR, exist_ok=True)

TIME_FORMAT = "%Y%m%d_%H%M%S"
TIMESTAMP = datetime.now().strftime(format=TIME_FORMAT)
BACKUP_DB_PATH = os.path.join(BACKUP_DB_DIR, f"backup_{TIMESTAMP}.sql")
BACKUP_FILES_PATH = os.path.join(BACKUP_FILES_DIR, f"media_{TIMESTAMP}")

env_file_path = ".env"
config = dict()
if os.path.exists(env_file_path):
    with open(env_file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key] = value


POSTGRES_USER = config.get("POSTGRES_USER")
POSTGRES_PASSWORD = config.get("POSTGRES_PASSWORD")
POSTGRES_HOST = config.get("POSTGRES_HOST")
POSTGRES_PORT = config.get("POSTGRES_PORT")
POSTGRES_DB = config.get("POSTGRES_DB")
DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

cmd_db = f"docker exec {DB_CONTAINER} pg_dump {DATABASE_URI} > {BACKUP_DB_PATH}"
cmd_static = f"docker cp {WEB_CONTAINER}:/backend_app/static/media {BACKUP_FILES_PATH}"

os.system(cmd_db)
os.system(cmd_static)

backup_db_list = os.listdir(BACKUP_DB_DIR)
if len(backup_db_list) > MAX_BACKUPS:
    old_backup = sorted(
        backup_db_list,
        key=lambda item: datetime.strptime(item, f"backup_{TIME_FORMAT}.sql"),
    )[0]
    os.remove(os.path.join(BACKUP_DB_DIR, old_backup))

backup_files_list = os.listdir(BACKUP_FILES_DIR)
if len(backup_files_list) > MAX_BACKUPS:
    old_static_backup = sorted(
        backup_files_list,
        key=lambda item: datetime.strptime(item, f"media_{TIME_FORMAT}"),
    )[0]
    shutil.rmtree(os.path.join(BACKUP_FILES_DIR, old_static_backup))
