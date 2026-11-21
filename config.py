import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "cambiar-esta-clave-en-desarrollo")
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "biblioteca"),
    "user": os.getenv("POSTGRES_USER", "biblioteca"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}
