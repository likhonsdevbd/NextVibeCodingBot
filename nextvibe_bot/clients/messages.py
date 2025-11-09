"""
Message client for sending and managing messages
"""

import logging
from typing import Optional, Union, List
from telegram.constants import ParseMode
from telegram import (
    Bot, Message, InputFile, InlineKeyboardMarkup, 
    ReplyKeyboardMarkup, LinkPreviewOptions, MessageEffect
)
from telegram.constants import MessageEffectType

from ..types import (
    ChatId, MessageId, ParseModeType, SendMessageParams,
    FileType, RequestResult
)
from .base import BaseClient

logger = logging.getLogger(__name__)


class MessageClient(BaseClient):
    """
    Client for message-related operations
    Provides typed wrappers for Telegram message methods
    """
    
    def __init__(self, main_client):
        super().__init__(main_client)
        self.bot = main_client.bot
    
    async def send_message(
        self,
        chat_id: ChatId,
        text: str,
        parse_mode: Optional[ParseModeType] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[MessageId] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Optional[Union[
            InlineKeyboardMarkup, 
            ReplyKeyboardMarkup, 
            "ForceReply", 
            "ReplyKeyboardRemove"
        ]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        message_effect_id: Optional[str] = None
    ) -> RequestResult:
        """
        Send a text message to a chat
        
        Args:
            chat_id: Unique identifier for the target chat
            text: Text of the message to be sent
            parse_mode: Mode for parsing entities in the message text
            disable_web_page_preview: Disables link previews for links in this message
            disable_notification: Sends the message silently
            protect_content: Protects the contents of the sent message
            reply_to_message_id: If the message is a reply, ID of the original message
            allow_sending_without_reply: Pass True to allow sending message without reply
            reply_markup: Additional interface options for the message
            link_preview_options: Link preview options for links in the message
            message_effect_id: Effect to show when user receives the message
            
        Returns:
            RequestResult with Message object on success
        """
        try:
            # Convert enum to telegram constant
            parse_mode_value = parse_mode.value if parse_mode else None
            
            # Create message effect if specified
            effect = None
            if message_effect_id:
                if message_effect_id in ['welcome', 'help', 'success', 'error', 'typing', 'loading', 'tapping', 'reaction']:
                    # Use built-in effect types
                    effect = MessageEffectType(message_effect_id)
            
            # Call the actual bot method
            message = await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode_value,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=reply_markup,
                link_preview_options=link_preview_options,
                message_effect_id=effect.value if effect else None
            )
            
            logger.info(f"Sent message to chat {chat_id}: {text[:50]}...")
            return RequestResult(success=True, data=message)
            
        except Exception as e:
            logger.error(f"Failed to send message to {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def edit_message_text(
        self,
        chat_id: Optional[ChatId] = None,
        message_id: Optional[MessageId] = None,
        inline_message_id: Optional[str] = None,
        text: str = "",
        parse_mode: Optional[ParseModeType] = None,
        disable_web_page_preview: Optional[bool] = None,
        reply_markup: Optional[Union[
            InlineKeyboardMarkup, 
            ReplyKeyboardMarkup, 
            "ForceReply", 
            "ReplyKeyboardRemove"
        ]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None
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
            parse_mode_value = parse_mode.value if parse_mode else None
            
            message = await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                inline_message_id=inline_message_id,
                text=text,
                parse_mode=parse_mode_value,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
                link_preview_options=link_preview_options
            )
            
            logger.info(f"Edited message {message_id or inline_message_id}")
            return RequestResult(success=True, data=message)
            
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def delete_message(
        self,
        chat_id: ChatId,
        message_id: MessageId
    ) -> RequestResult:
        """
        Delete a message
        
        Args:
            chat_id: Unique identifier for the target chat
            message_id: Identifier of the message to delete
            
        Returns:
            RequestResult with success status
        """
        try:
            await self.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
            
            logger.info(f"Deleted message {message_id} from chat {chat_id}")
            return RequestResult(success=True, data=True)
            
        except Exception as e:
            logger.error(f"Failed to delete message {message_id} from {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def send_photo(
        self,
        chat_id: ChatId,
        photo: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[ParseModeType] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[MessageId] = None,
        reply_markup: Optional[Union[
            InlineKeyboardMarkup, 
            ReplyKeyboardMarkup, 
            "ForceReply", 
            "ReplyKeyboardRemove"
        ]] = None
    ) -> RequestResult:
        """
        Send photos
        
        Args:
            chat_id: Unique identifier for the target chat
            photo: Photo to send
            caption: Photo caption
            parse_mode: Mode for parsing entities in the caption
            disable_notification: Sends the message silently
            protect_content: Protects the contents of the sent message
            reply_to_message_id: If the message is a reply, ID of the original message
            reply_markup: Additional interface options
            
        Returns:
            RequestResult with Message object on success
        """
        try:
            parse_mode_value = parse_mode.value if parse_mode else None
            
            message = await self.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                parse_mode=parse_mode_value,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup
            )
            
            logger.info(f"Sent photo to chat {chat_id}")
            return RequestResult(success=True, data=message)
            
        except Exception as e:
            logger.error(f"Failed to send photo to {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def send_voice(
        self,
        chat_id: ChatId,
        voice: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[ParseModeType] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[MessageId] = None,
        reply_markup: Optional[Union[
            InlineKeyboardMarkup, 
            ReplyKeyboardMarkup, 
            "ForceReply", 
            "ReplyKeyboardRemove"
        ]] = None
    ) -> RequestResult:
        """
        Send voice messages
        
        Args:
            chat_id: Unique identifier for the target chat
            voice: Audio file to send
            caption: Voice message caption
            parse_mode: Mode for parsing entities in the caption
            duration: Duration of the voice message in seconds
            disable_notification: Sends the message silently
            protect_content: Protects the contents of the sent message
            reply_to_message_id: If the message is a reply, ID of the original message
            reply_markup: Additional interface options
            
        Returns:
            RequestResult with Message object on success
        """
        try:
            parse_mode_value = parse_mode.value if parse_mode else None
            
            message = await self.bot.send_voice(
                chat_id=chat_id,
                voice=voice,
                caption=caption,
                parse_mode=parse_mode_value,
                duration=duration,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup
            )
            
            logger.info(f"Sent voice to chat {chat_id}")
            return RequestResult(success=True, data=message)
            
        except Exception as e:
            logger.error(f"Failed to send voice to {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def send_document(
        self,
        chat_id: ChatId,
        document: Union[str, InputFile],
        caption: Optional[str] = None,
        parse_mode: Optional[ParseModeType] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        reply_to_message_id: Optional[MessageId] = None,
        reply_markup: Optional[Union[
            InlineKeyboardMarkup, 
            ReplyKeyboardMarkup, 
            "ForceReply", 
            "ReplyKeyboardRemove"
        ]] = None
    ) -> RequestResult:
        """
        Send general files
        
        Args:
            chat_id: Unique identifier for the target chat
            document: File to send
            caption: Document caption
            parse_mode: Mode for parsing entities in the caption
            disable_notification: Sends the message silently
            protect_content: Protects the contents of the sent message
            reply_to_message_id: If the message is a reply, ID of the original message
            reply_markup: Additional interface options
            
        Returns:
            RequestResult with Message object on success
        """
        try:
            parse_mode_value = parse_mode.value if parse_mode else None
            
            message = await self.bot.send_document(
                chat_id=chat_id,
                document=document,
                caption=caption,
                parse_mode=parse_mode_value,
                disable_notification=disable_notification,
                protect_content=protect_content,
                reply_to_message_id=reply_to_message_id,
                reply_markup=reply_markup
            )
            
            logger.info(f"Sent document to chat {chat_id}")
            return RequestResult(success=True, data=message)
            
        except Exception as e:
            logger.error(f"Failed to send document to {chat_id}: {e}")
            return RequestResult(success=False, error=str(e))