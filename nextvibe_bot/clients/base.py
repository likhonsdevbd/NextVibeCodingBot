"""
Base client class for NextVibeBot clients
"""

import logging
from typing import Optional, Any
from telegram import Bot

from ..types import RequestResult

logger = logging.getLogger(__name__)


class BaseClient:
    """
    Base client class that provides common functionality for all NextVibeBot client modules
    """
    
    def __init__(self, main_client: 'NextVibeClient'):
        """
        Initialize base client
        
        Args:
            main_client: The main NextVibeClient instance
        """
        self.main_client = main_client
        self.bot = main_client.bot
        self.token = main_client.token
        
    async def _handle_request(self, operation: str, callable_func, *args, **kwargs) -> RequestResult:
        """
        Handle API requests with consistent error handling and logging
        
        Args:
            operation: Name of the operation being performed
            callable_func: The function to call
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            RequestResult with success status and data/error
        """
        try:
            logger.debug(f"Executing {operation} with args: {args}, kwargs: {kwargs}")
            result = await callable_func(*args, **kwargs)
            logger.debug(f"Successfully completed {operation}")
            return RequestResult(success=True, data=result)
            
        except Exception as e:
            logger.error(f"Failed to execute {operation}: {e}", exc_info=True)
            return RequestResult(success=False, error=str(e))
    
    def _validate_required_params(self, operation: str, **kwargs) -> Optional[RequestResult]:
        """
        Validate that all required parameters are provided
        
        Args:
            operation: Name of the operation for error messages
            **kwargs: Parameters to validate
            
        Returns:
            RequestResult with error if validation fails, None if valid
        """
        for param_name, param_value in kwargs.items():
            if param_value is None:
                error_msg = f"{operation} requires '{param_name}' parameter"
                logger.error(error_msg)
                return RequestResult(success=False, error=error_msg)
        return None
    
    def _normalize_chat_id(self, chat_id: Any) -> Any:
        """
        Normalize chat ID for consistent usage
        
        Args:
            chat_id: Chat ID to normalize
            
        Returns:
            Normalized chat ID
        """
        # Convert integer user IDs to proper format
        if isinstance(chat_id, int) and chat_id > 0:
            return chat_id
        return chat_id
    
    def _normalize_message_id(self, message_id: Any) -> int:
        """
        Normalize message ID for consistent usage
        
        Args:
            message_id: Message ID to normalize
            
        Returns:
            Normalized message ID as int
        """
        try:
            return int(message_id)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid message ID: {message_id}. Must be an integer.")
    
    def _normalize_user_id(self, user_id: Any) -> int:
        """
        Normalize user ID for consistent usage
        
        Args:
            user_id: User ID to normalize
            
        Returns:
            Normalized user ID as int
        """
        try:
            return int(user_id)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid user ID: {user_id}. Must be an integer.")
    
    def _build_url(self, method: str) -> str:
        """
        Build Telegram API URL for a given method
        
        Args:
            method: Telegram API method name
            
        Returns:
            Full API URL
        """
        return f"https://api.telegram.org/bot{self.token}/{method}"
    
    async def health_check(self) -> RequestResult:
        """
        Perform a health check to verify the bot connection
        
        Returns:
            RequestResult with bot info on success, error on failure
        """
        try:
            bot_info = await self.bot.get_me()
            return RequestResult(
                success=True, 
                data={
                    "id": bot_info.id,
                    "first_name": bot_info.first_name,
                    "username": bot_info.username,
                    "is_bot": bot_info.is_bot
                }
            )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def get_bot_info(self) -> RequestResult:
        """
        Get detailed bot information
        
        Returns:
            RequestResult with bot information
        """
        return await self.health_check()
    
    def get_supported_features(self) -> dict:
        """
        Get information about supported features
        
        Returns:
            Dictionary with feature support information
        """
        return {
            "api_version": "9.2",
            "features": {
                "link_previews": True,
                "message_effects": True,
                "voice_messages": True,
                "web_apps": True,
                "inline_keyboards": True,
                "reply_keyboards": True,
                "webhooks": True,
                "payments": True,
                "games": True,
                "commands": True
            },
            "client_modules": [
                "messages", "keyboards", "users", "chats", 
                "callback", "files", "payments", "games", 
                "webhooks", "auth", "help"
            ]
        }