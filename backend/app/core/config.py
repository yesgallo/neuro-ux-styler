import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Neuro UX Styler API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()