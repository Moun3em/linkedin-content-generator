import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    GPT_MODEL: str = "gpt-4"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7
    
    class Config:
        env_file = ".env"

settings = Settings()
