"""
Chat client for chat-related operations
"""

import logging
from typing import List, Optional
from telegram import Chat

from ..types import ChatId, RequestResult
from .base import BaseClient

logger = logging.getLogger(__name__)


class ChatClient(BaseClient):
    """
    Client for chat-related operations
    """
    
    async def get_chat(self, chat_id: ChatId) -> RequestResult:
        """
        Get basic information about a chat
        
        Args:
            chat_id: Unique identifier of the target chat
            
        Returns:
            RequestResult with Chat object
        """
        try:
            chat = await self.bot.get_chat(chat_id=chat_id)
            
            chat_info = {
                "id": chat.id,
                "type": chat.type,
                "title": getattr(chat, 'title', None),
                "username": getattr(chat, 'username', None),
                "first_name": getattr(chat, 'first_name', None),
                "photo": getattr(chat, 'photo', None),
                "description": getattr(chat, 'description', None),
                "invite_link": getattr(chat, 'invite_link', None),
                "pinned_message": getattr(chat, 'pinned_message', None),
                "permissions": getattr(chat, 'permissions', None),
                "slow_mode_delay": getattr(chat, 'slow_mode_delay', None),
                "message_auto_delete_time": getattr(chat, 'message_auto_delete_time', None),
                "has_hidden_forwards": getattr(chat, 'has_hidden_forwards', None),
                "has_protected_content": getattr(chat, 'has_protected_content', None),
                "sticker_set_name": getattr(chat, 'sticker_set_name', None),
                "can_set_sticker_set": getattr(chat, 'can_set_sticker_set', None),
                "linked_chat_id": getattr(chat, 'linked_chat_id', None),
                "location": getattr(chat, 'location', None)
            }
            
            logger.info(f"Retrieved chat info for {chat_id}")
            return RequestResult(success=True, data=chat_info)
            
        except Exception as e:
            logger.error(f"Failed to get chat {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def get_chat_administrators(self, chat_id: ChatId) -> RequestResult:
        """
        Get a list of administrators in a chat
        
        Args:
            chat_id: Unique identifier of the target chat
            
        Returns:
            RequestResult with list of ChatMember objects
        """
        try:
            administrators = await self.bot.get_chat_administrators(chat_id=chat_id)
            
            admin_list = []
            for admin in administrators:
                admin_info = {
                    "user": {
                        "id": admin.user.id,
                        "is_bot": admin.user.is_bot,
                        "first_name": admin.user.first_name,
                        "username": admin.user.username
                    },
                    "status": admin.status,
                    "until_date": getattr(admin, 'until_date', None),
                    "can_be_edited": getattr(admin, 'can_be_edited', None),
                    "can_change_info": getattr(admin, 'can_change_info', None),
                    "can_post_messages": getattr(admin, 'can_post_messages', None),
                    "can_edit_messages": getattr(admin, 'can_edit_messages', None),
                    "can_delete_messages": getattr(admin, 'can_delete_messages', None),
                    "can_invite_users": getattr(admin, 'can_invite_users', None),
                    "can_restrict_members": getattr(admin, 'can_restrict_members', None),
                    "can_pin_messages": getattr(admin, 'can_pin_messages', None),
                    "can_promote_members": getattr(admin, 'can_promote_members', None),
                    "is_anonymous": getattr(admin, 'is_anonymous', None)
                }
                admin_list.append(admin_info)
            
            logger.info(f"Retrieved {len(admin_list)} administrators for chat {chat_id}")
            return RequestResult(success=True, data=admin_list)
            
        except Exception as e:
            logger.error(f"Failed to get administrators for chat {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def get_chat_member_count(self, chat_id: ChatId) -> RequestResult:
        """
        Get the number of members in a chat
        
        Args:
            chat_id: Unique identifier of the target chat
            
        Returns:
            RequestResult with member count (int)
        """
        try:
            count = await self.bot.get_chat_member_count(chat_id=chat_id)
            
            logger.info(f"Retrieved member count for chat {chat_id}: {count}")
            return RequestResult(success=True, data=count)
            
        except Exception as e:
            logger.error(f"Failed to get member count for chat {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))