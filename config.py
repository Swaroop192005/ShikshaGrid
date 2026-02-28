import os
from urllib.parse import quote_plus as urlquote

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "Aditi0307")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ShikshaGrid")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{DB_USER}:{urlquote(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-to-a-secure-random-value")
