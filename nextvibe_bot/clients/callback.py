"""
Callback client for callback query operations
"""

import logging
from typing import Optional, Union, List

from ..types import RequestResult
from .base import BaseClient

logger = logging.getLogger(__name__)


class CallbackClient(BaseClient):
    """
    Client for callback query operations
    """
    
    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: bool = False,
        url: Optional[str] = None,
        cache_time: Optional[int] = None
    ) -> RequestResult:
        """
        Send answer to callback query
        
        Args:
            callback_query_id: Unique identifier for the query to be answered
            text: Text of the notification. If not specified, nothing will be shown
            show_alert: If true, an alert will be shown instead of a notification
            url: URL that will be opened by the user's client
            cache_time: Maximum amount of time in seconds that the result of the callback query may be cached client-side
            
        Returns:
            RequestResult with success status
        """
        try:
            await self.bot.answer_callback_query(
                callback_query_id=callback_query_id,
                text=text,
                show_alert=show_alert,
                url=url,
                cache_time=cache_time
            )
            
            logger.info(f"Answered callback query {callback_query_id}")
            return RequestResult(success=True, data=True)
            
        except Exception as e:
            logger.error(f"Failed to answer callback query {callback_query_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def edit_message_text(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        text: str = "",
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[object] = None
    ) -> RequestResult:
        """
        Edit text and game messages
        
        Args:
            chat_id: Required if inline_message_id is not specified
            message_id: Required if inline_message_id is not specified
            inline_message_id: Required if chat_id and message_id are not specified
            text: New text of the message
            parse_mode: Mode for parsing entities
            disable_web_page_preview: Disables link previews
            reply_markup: Additional interface options
            
        Returns:
            RequestResult with edited Message object on success
        """
        try:
            message = await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup
            )
            
            logger.info(f"Edited message {message_id or inline_message_id}")
            return RequestResult(success=True, data=message)
            
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def edit_message_caption(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[dict]] = None,
        reply_markup: Optional[object] = None
    ) -> RequestResult:
        """
        Edit the caption of a message
        
        Args:
            chat_id: Required if inline_message_id is not specified
            message_id: Required if inline_message_id is not specified
            inline_message_id: Required if chat_id and message_id are not specified
            caption: New caption of the message
            parse_mode: Mode for parsing entities
            caption_entities: List of special entities that appear in the caption
            reply_markup: Additional interface options
            
        Returns:
            RequestResult with edited Message object on success
        """
        try:
            message = await self.bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                caption=caption,
                parse_mode=parse_mode,
                caption_entities=caption_entities,
                reply_markup=reply_markup
            )
            
            logger.info(f"Edited message caption {message_id or inline_message_id}")
            return RequestResult(success=True, data=message)
            
        except Exception as e:
            logger.error(f"Failed to edit message caption: {e}")
            return RequestResult(success=False, error=str(e))