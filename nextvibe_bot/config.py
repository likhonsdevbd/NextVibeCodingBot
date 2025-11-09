"""
Configuration management for NextVibeCodingBot
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Telegram Bot Configuration
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    
    # AI Service Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    e2b_api_key: Optional[str] = Field(default=None, env="E2B_API_KEY")
    
    # Database Configuration
    database_url: str = Field(env="DATABASE_URL")
    pg_host: str = Field(env="PGHOST")
    pg_user: str = Field(env="PGUSER")
    pg_database: str = Field(env="PGDATABASE")
    pg_password: str = Field(env="PGPASSWORD")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    # Code Execution Configuration
    docker_enabled: bool = Field(default=True, env="DOCKER_ENABLED")
    code_execution_timeout: int = Field(default=30, env="CODE_EXECUTION_TIMEOUT")
    max_code_size: int = Field(default=10000, env="MAX_CODE_SIZE")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/nextvibe_bot.log", env="LOG_FILE")
    
    # Security Configuration
    max_messages_per_minute: int = Field(default=10, env="MAX_MESSAGES_PER_MINUTE")
    allowed_users: List[str] = Field(default_factory=list, env="ALLOWED_USERS")
    
    # Bot Configuration
    bot_name: str = "NextVibeCodingBot"
    bot_description: str = "An autonomous coding agent that can tackle bugs, features, and other software engineering tasks"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Supported programming languages
SUPPORTED_LANGUAGES = {
    "python": {"ext": [".py"], "image": "python:3.11"},
    "javascript": {"ext": [".js", ".mjs"], "image": "node:18"},
    "typescript": {"ext": [".ts"], "image": "node:18"},
    "java": {"ext": [".java"], "image": "openjdk:17"},
    "cpp": {"ext": [".cpp", ".cc", ".cxx"], "image": "gcc:latest"},
    "c": {"ext": [".c"], "image": "gcc:latest"},
    "go": {"ext": [".go"], "image": "golang:1.21"},
    "rust": {"ext": [".rs"], "image": "rust:1.70"},
    "php": {"ext": [".php"], "image": "php:8.2"},
    "ruby": {"ext": [".rb"], "image": "ruby:3.2"},
    "bash": {"ext": [".sh", ".bash"], "image": "ubuntu:latest"},
}

# Task type patterns for message parsing
TASK_PATTERNS = {
    "bug": [
        r"(?i)\b(bug|error|issue|problem|fix|broken|not working|exception|fail)\b",
        r"get.*error",
        r"doesn't work",
        r"broken",
        r"help.*error"
    ],
    "feature": [
        r"(?i)\b(feature|add|implement|create|build|develop|enhance|improve)\b",
        r"need.*function",
        r"want.*feature",
        r"add.*to.*project",
        r"implement.*that"
    ],
    "code_review": [
        r"(?i)\b(review|analyze|check|examine|optimize|refactor)\b",
        r"look.*at.*code",
        r"review.*this",
        r"analyze.*performance"
    ],
    "debug": [
        r"(?i)\b(debug|trace|find.*issue|diagnose|troubleshoot)\b",
        r"stuck.*on",
        r"can't.*figure.*out",
        r"help.*debug"
    ]
}