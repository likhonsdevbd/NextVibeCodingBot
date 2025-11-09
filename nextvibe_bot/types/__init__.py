"""
Type definitions for NextVibeBot client library
"""

from typing import Optional, List, Union, Dict, Any, Callable
from enum import Enum
from datetime import datetime
from telegram.constants import ParseMode
from telegram import (
    Update, Message, User, Chat, InlineKeyboardButton, 
    InlineKeyboardMarkup, ReplyKeyboardMarkup, File,
    LinkPreviewOptions, MessageEffect
)

# Base types
ChatId = Union[int, str]
MessageId = int
UserId = int

# Parse mode enum
class ParseModeType(Enum):
    MARKDOWN = ParseMode.MARKDOWN
    HTML = ParseMode.HTML
    NONE = None

# File types
class FileType(Enum):
    PHOTO = "photo"
    DOCUMENT = "document"
    AUDIO = "audio"
    VOICE = "voice"
    VIDEO = "video"
    ANIMATION = "animation"

# Message effect types
class MessageEffectType(Enum):
    WELCOME = "welcome"
    HELP = "help"
    SUCCESS = "success"
    ERROR = "error"
    TYPING = "typing"
    LOADING = "loading"
    TAPPING = "tapping"
    REACTION = "reaction"

# Request result types
class RequestResult:
    """Base result for API requests"""
    def __init__(self, success: bool, data: Any = None, error: str = None):
        self.success = success
        self.data = data
        self.error = error

# Message request parameters
class SendMessageParams:
    """Parameters for sending messages"""
    def __init__(
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
    ):
        self.chat_id = chat_id
        self.text = text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self.protect_content = protect_content
        self.reply_to_message_id = reply_to_message_id
        self.allow_sending_without_reply = allow_sending_without_reply
        self.reply_markup = reply_markup
        self.link_preview_options = link_preview_options
        self.message_effect_id = message_effect_id

# Keyboard button types
class KeyboardButton:
    """Represents a keyboard button"""
    def __init__(
        self,
        text: str,
        request_contact: Optional[bool] = None,
        request_location: Optional[bool] = None,
        web_app: Optional[Dict[str, Any]] = None
    ):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.web_app = web_app

# Inline keyboard button
class InlineKeyboardButton:
    """Represents an inline keyboard button"""
    def __init__(
        self,
        text: str,
        callback_data: Optional[str] = None,
        url: Optional[str] = None,
        login_url: Optional[Dict[str, Any]] = None,
        switch_inline_query: Optional[str] = None,
        switch_inline_query_current_chat: Optional[str] = None,
        game: Optional[str] = None,
        pay: Optional[bool] = None,
        web_app: Optional[Dict[str, Any]] = None
    ):
        self.text = text
        self.callback_data = callback_data
        self.url = url
        self.login_url = login_url
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.game = game
        self.pay = pay
        self.web_app = web_app

# Chat member types
class ChatMember:
    """Represents a chat member"""
    def __init__(
        self,
        user: User,
        status: str,
        until_date: Optional[datetime] = None,
        can_be_edited: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        is_anonymous: Optional[bool] = None,
        is_member: Optional[bool] = None,
        can_send_messages: Optional[bool] = None,
        can_send_audios: Optional[bool] = None,
        can_send_documents: Optional[bool] = None,
        can_send_photos: Optional[bool] = None,
        can_send_videos: Optional[bool] = None,
        can_send_voice_notes: Optional[bool] = None,
        can_send_video_notes: Optional[bool] = None,
        can_send_polls: Optional[bool] = None,
        can_send_other_messages: Optional[bool] = None,
        can_add_web_page_previews: Optional[bool] = None
    ):
        self.user = user
        self.status = status
        self.until_date = until_date
        self.can_be_edited = can_be_edited
        self.can_change_info = can_change_info
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_invite_users = can_invite_users
        self.can_restrict_members = can_restrict_members
        self.can_pin_messages = can_pin_messages
        self.can_promote_members = can_promote_members
        self.is_anonymous = is_anonymous
        self.is_member = is_member
        self.can_send_messages = can_send_messages
        self.can_send_audios = can_send_audios
        self.can_send_documents = can_send_documents
        self.can_send_photos = can_send_photos
        self.can_send_videos = can_send_videos
        self.can_send_voice_notes = can_send_voice_notes
        self.can_send_video_notes = can_send_video_notes
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews

# User profile photos
class UserProfilePhotos:
    """Represents user profile photos"""
    def __init__(self, total_count: int, photos: List[List[File]]):
        self.total_count = total_count
        self.photos = photos

# File info
class FileInfo:
    """File information"""
    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        file_size: Optional[int] = None,
        file_path: Optional[str] = None
    ):
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_path = file_path

# Webhook info
class WebhookInfo:
    """Webhook information"""
    def __init__(
        self,
        url: str,
        has_custom_certificate: bool,
        pending_update_count: int,
        last_error_date: Optional[datetime] = None,
        last_error_message: Optional[str] = None,
        last_synchronization_error_date: Optional[datetime] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None
    ):
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.last_synchronization_error_date = last_synchronization_error_date
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates

# Callback query
class CallbackQuery:
    """Represents a callback query"""
    def __init__(
        self,
        id: str,
        from_user: User,
        message: Optional[Message] = None,
        inline_message_id: Optional[str] = None,
        chat_instance: Optional[str] = None,
        data: Optional[str] = None,
        game_short_name: Optional[str] = None
    ):
        self.id = id
        self.from_user = from_user
        self.message = message
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.data = data
        self.game_short_name = game_short_name

# Bot info
class BotInfo:
    """Bot information"""
    def __init__(
        self,
        id: int,
        is_bot: bool,
        first_name: str,
        username: Optional[str] = None,
        can_join_groups: Optional[bool] = None,
        can_read_all_group_messages: Optional[bool] = None,
        supports_inline_queries: Optional[bool] = None,
        can_connect_to_business: Optional[bool] = None,
        has_main_web_app: Optional[bool] = None
    ):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.username = username
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries
        self.can_connect_to_business = can_connect_to_business
        self.has_main_web_app = has_main_web_app