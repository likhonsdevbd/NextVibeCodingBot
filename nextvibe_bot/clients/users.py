"""
User client for user-related operations
"""

import logging
from typing import List, Optional
from telegram import User

from ..types import UserId, RequestResult
from .base import BaseClient

logger = logging.getLogger(__name__)


class UserClient(BaseClient):
    """
    Client for user-related operations
    """
    
    async def get_me(self) -> RequestResult:
        """
        Get information about the bot
        
        Returns:
            RequestResult with User object containing bot information
        """
        try:
            bot_user = await self.bot.get_me()
            
            bot_info = {
                "id": bot_user.id,
                "is_bot": bot_user.is_bot,
                "first_name": bot_user.first_name,
                "username": bot_user.username,
                "can_join_groups": getattr(bot_user, 'can_join_groups', None),
                "can_read_all_group_messages": getattr(bot_user, 'can_read_all_group_messages', None),
                "supports_inline_queries": getattr(bot_user, 'supports_inline_queries', None),
                "can_connect_to_business": getattr(bot_user, 'can_connect_to_business', None),
                "has_main_web_app": getattr(bot_user, 'has_main_web_app', None)
            }
            
            logger.info(f"Retrieved bot info for @{bot_user.username}")
            return RequestResult(success=True, data=bot_info)
            
        except Exception as e:
            logger.error(f"Failed to get bot information: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def get_user_profile_photos(
        self,
        user_id: UserId,
        offset: int = 0,
        limit: int = 100
    ) -> RequestResult:
        """
        Get a list of profile pictures for a user
        
        Args:
            user_id: Unique identifier of the target user
            offset: Number of photos to skip
            limit: Number of photos to return (1-100)
            
        Returns:
            RequestResult with UserProfilePhotos object
        """
        try:
            # Validate limit
            if limit < 1 or limit > 100:
                limit = min(max(limit, 1), 100)
            
            photos = await self.bot.get_user_profile_photos(
                user_id=user_id,
                offset=offset,
                limit=limit
            )
            
            photos_data = {
                "total_count": photos.total_count,
                "photos": photos.photos
            }
            
            logger.info(f"Retrieved {len(photos.photos)} profile photos for user {user_id}")
            return RequestResult(success=True, data=photos_data)
            
        except Exception as e:
            logger.error(f"Failed to get profile photos for user {user_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def get_chat_member(
        self,
        chat_id,
        user_id: UserId
    ) -> RequestResult:
        """
        Get information about a member of a chat
        
        Args:
            chat_id: Unique identifier of the target chat
            user_id: Unique identifier of the target user
            
        Returns:
            RequestResult with ChatMember object
        """
        try:
            member = await self.bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            
            member_info = {
                "user": {
                    "id": member.user.id,
                    "is_bot": member.user.is_bot,
                    "first_name": member.user.first_name,
                    "username": member.user.username
                },
                "status": member.status,
                "until_date": getattr(member, 'until_date', None),
                "can_be_edited": getattr(member, 'can_be_edited', None),
                "can_change_info": getattr(member, 'can_change_info', None),
                "can_post_messages": getattr(member, 'can_post_messages', None),
                "can_edit_messages": getattr(member, 'can_edit_messages', None),
                "can_delete_messages": getattr(member, 'can_delete_messages', None),
                "can_invite_users": getattr(member, 'can_invite_users', None),
                "can_restrict_members": getattr(member, 'can_restrict_members', None),
                "can_pin_messages": getattr(member, 'can_pin_messages', None),
                "can_promote_members": getattr(member, 'can_promote_members', None),
                "is_anonymous": getattr(member, 'is_anonymous', None),
                "is_member": getattr(member, 'is_member', None),
                "can_send_messages": getattr(member, 'can_send_messages', None),
                "can_send_audios": getattr(member, 'can_send_audios', None),
                "can_send_documents": getattr(member, 'can_send_documents', None),
                "can_send_photos": getattr(member, 'can_send_photos', None),
                "can_send_videos": getattr(member, 'can_send_videos', None),
                "can_send_voice_notes": getattr(member, 'can_send_voice_notes', None),
                "can_send_video_notes": getattr(member, 'can_send_video_notes', None),
                "can_send_polls": getattr(member, 'can_send_polls', None),
                "can_send_other_messages": getattr(member, 'can_send_other_messages', None),
                "can_add_web_page_previews": getattr(member, 'can_add_web_page_previews', None)
            }
            
            logger.info(f"Retrieved member info for user {user_id} in chat {chat_id}")
            return RequestResult(success=True, data=member_info)
            
        except Exception as e:
            logger.error(f"Failed to get chat member for user {user_id} in chat {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))