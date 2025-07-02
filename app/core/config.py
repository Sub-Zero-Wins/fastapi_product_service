import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_URL: str = os.getenv("DB_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD")
    USER_USERNAME: str = os.getenv("USER_USERNAME")
    USER_PASSWORD: str = os.getenv("USER_PASSWORD")

settings = Settings()
