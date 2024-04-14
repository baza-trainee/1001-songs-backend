from datetime import datetime
import os

DB_CONTAINER = "postgres_songs"
WEB_CONTAINER = "backend_songs"

BACKUP_DB_DIR = "backup_db"
BACKUP_FILES_DIR = "backup_files"

TIME_FORMAT = "%Y%m%d_%H%M%S"

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

if not os.path.exists(BACKUP_DB_DIR):
    print("Backup directory does not exist. Exiting.")
    exit(1)

BACKUP_DB_LIST = sorted(
    os.listdir(BACKUP_DB_DIR),
    key=lambda item: datetime.strptime(item, f"backup_{TIME_FORMAT}.sql"),
    reverse=True,
)
BACKUP_FILES_LIST = sorted(
    os.listdir(BACKUP_FILES_DIR),
    key=lambda item: datetime.strptime(item, f"media_{TIME_FORMAT}"),
    reverse=True,
)

if not BACKUP_DB_LIST:
    print("No backup files found in the directory. Exiting.")
    exit(1)

print(
    "Оберіть backup-файл зі списку, для відновлення бази даних та файлів. Введіть цифру:"
)
for i, backup in enumerate(BACKUP_DB_LIST, start=1):
    print(f"{i} - {backup}")

choice = int(input("Ваш вибір: "))

# db
os.system(
    f"docker exec {DB_CONTAINER} psql {DATABASE_URI} -c 'DROP SCHEMA public CASCADE;'"
)
os.system(f"docker exec {DB_CONTAINER} psql {DATABASE_URI} -c 'CREATE SCHEMA public;'")
os.system(
    f"docker exec -i {DB_CONTAINER} psql {DATABASE_URI} < {BACKUP_DB_DIR}/{BACKUP_DB_LIST[choice - 1]}"
)

# media
os.system(
    f"cd {BACKUP_FILES_DIR}/{BACKUP_FILES_LIST[choice - 1]} && docker cp . {WEB_CONTAINER}:/backend_app/static/media/"
)
