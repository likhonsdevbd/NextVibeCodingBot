"""
Rate limiter for preventing spam and abuse
"""

import asyncio
import time
from typing import Dict, Any, Optional
from collections import defaultdict
import logging

from ..config import settings


logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple rate limiter for user messages"""
    
    def __init__(self):
        self.max_messages = settings.max_messages_per_minute
        self.message_counts = defaultdict(list)
        self.lock = asyncio.Lock()
        
    async def is_allowed(self, user_id: int) -> bool:
        """
        Check if a user is allowed to send another message
        
        Args:
            user_id: The Telegram user ID
            
        Returns:
            True if the user can send a message, False if rate limited
        """
        async with self.lock:
            current_time = time.time()
            minute_ago = current_time - 60
            
            # Clean up old timestamps
            self.message_counts[user_id] = [
                timestamp for timestamp in self.message_counts[user_id]
                if timestamp > minute_ago
            ]
            
            # Check if user has exceeded the limit
            if len(self.message_counts[user_id]) >= self.max_messages:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                return False
                
            # Add current message timestamp
            self.message_counts[user_id].append(current_time)
            return True
            
    async def get_remaining_messages(self, user_id: int) -> int:
        """Get remaining messages for a user in the current minute"""
        async with self.lock:
            current_time = time.time()
            minute_ago = current_time - 60
            
            # Clean up old timestamps
            self.message_counts[user_id] = [
                timestamp for timestamp in self.message_counts[user_id]
                if timestamp > minute_ago
            ]
            
            return max(0, self.max_messages - len(self.message_counts[user_id]))
            
    async def get_reset_time(self, user_id: int) -> Optional[float]:
        """
        Get the time when a user's rate limit will reset
        
        Args:
            user_id: The Telegram user ID
            
        Returns:
            Unix timestamp when the limit resets, or None if not rate limited
        """
        async with self.lock:
            current_time = time.time()
            minute_ago = current_time - 60
            
            if len(self.message_counts[user_id]) < self.max_messages:
                return None
                
            # Return the time when the oldest message will expire
            if self.message_counts[user_id]:
                oldest_message = min(self.message_counts[user_id])
                return oldest_message + 60
                
            return None