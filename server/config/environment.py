import os
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()

TIMEZONE = timezone("Europe/Moscow")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        default=60
    )
)
REFRESH_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_MINUTES",
        default=720
    )
)

DATABASE_FILE = os.getenv("DATABASE_FILE")
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

ORIGINS = [
    "*"
]
