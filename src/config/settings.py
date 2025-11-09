"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Bot Configuration
    telegram_token: str
    
    # OpenAI Configuration
    openai_api_key: str
    
    # Logging Configuration
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"