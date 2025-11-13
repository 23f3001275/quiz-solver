# src/app/config.py
import os

class Settings:
    EXPECTED_SECRET: str = os.getenv("EXPECTED_SECRET", "")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

settings = Settings()
