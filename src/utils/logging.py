"""
Logging configuration module.
"""
import sys
from loguru import logger
from typing import Dict, Any

def setup_logging(config: Dict[str, Any]) -> None:
    """
    Configure logging for the application.
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        level=config.get("log_level", "INFO"),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Add file handler
    logger.add(
        "logs/nextvibe.log",
        rotation="1 day",
        retention="7 days",
        level=config.get("log_level", "INFO"),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )