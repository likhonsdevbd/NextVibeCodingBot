"""
Telegram TL method to friendly name mapping for NextVibeBot
This file provides a mapping between Telegram's TL (Type Language) method names
and the friendly, developer-friendly function names used in the client library.
"""

from typing import Dict, Any, List, Optional

# Main mapping of Telegram TL methods to friendly names
TELEGRAM_TL_MAPPING = {
    # Message methods
    "sendMessage": {
        "friendly_name": "send_message",
        "module": "messages",
        "description": "Send a text message to a chat",
        "parameters": {
            "chat_id": "Unique identifier for the target chat",
            "text": "Text of the message to be sent",
            "parse_mode": "Mode for parsing entities in the message text",
            "disable_web_page_preview": "Disables link previews for links in this message",
            "disable_notification": "Sends the message silently",
            "protect_content": "Protects the contents of the sent message",
            "reply_to_message_id": "If the message is a reply, ID of the original message",
            "allow_sending_without_reply": "Pass True to allow sending message without reply",
            "reply_markup": "Additional interface options for the message",
            "link_preview_options": "Link preview options for links in the message",
            "message_effect_id": "Effect to show when user receives the message"
        }
    },
    
    "editMessageText": {
        "friendly_name": "edit_message_text",
        "module": "messages",
        "description": "Edit text and game messages",
        "parameters": {
            "chat_id": "Required if inline_message_id is not specified",
            "message_id": "Required if inline_message_id is not specified",
            "inline_message_id": "Required if chat_id and message_id are not specified",
            "text": "New text of the message",
            "parse_mode": "Mode for parsing entities",
            "disable_web_page_preview": "Disables link previews",
            "reply_markup": "Additional interface options"
        }
    },
    
    "deleteMessage": {
        "friendly_name": "delete_message",
        "module": "messages",
        "description": "Delete a message",
        "parameters": {
            "chat_id": "Unique identifier for the target chat",
            "message_id": "Identifier of the message to delete"
        }
    },
    
    "sendPhoto": {
        "friendly_name": "send_photo",
        "module": "messages",
        "description": "Send photos",
        "parameters": {
            "chat_id": "Unique identifier for the target chat",
            "photo": "Photo to send",
            "caption": "Photo caption",
            "parse_mode": "Mode for parsing entities in the caption",
            "disable_notification": "Sends the message silently",
            "protect_content": "Protects the contents of the sent message",
            "reply_to_message_id": "If the message is a reply, ID of the original message",
            "reply_markup": "Additional interface options"
        }
    },
    
    "sendVoice": {
        "friendly_name": "send_voice",
        "module": "messages",
        "description": "Send voice messages",
        "parameters": {
            "chat_id": "Unique identifier for the target chat",
            "voice": "Audio file to send",
            "caption": "Voice message caption",
            "parse_mode": "Mode for parsing entities in the caption",
            "duration": "Duration of the voice message in seconds",
            "disable_notification": "Sends the message silently",
            "protect_content": "Protects the contents of the sent message",
            "reply_to_message_id": "If the message is a reply, ID of the original message",
            "reply_markup": "Additional interface options"
        }
    },
    
    "sendDocument": {
        "friendly_name": "send_document",
        "module": "messages",
        "description": "Send general files",
        "parameters": {
            "chat_id": "Unique identifier for the target chat",
            "document": "File to send",
            "caption": "Document caption",
            "parse_mode": "Mode for parsing entities in the caption",
            "disable_notification": "Sends the message silently",
            "protect_content": "Protects the contents of the sent message",
            "reply_to_message_id": "If the message is a reply, ID of the original message",
            "reply_markup": "Additional interface options"
        }
    },
    
    # User methods
    "getMe": {
        "friendly_name": "get_me",
        "module": "users",
        "description": "Get information about the bot",
        "parameters": {}
    },
    
    "getUserProfilePhotos": {
        "friendly_name": "get_user_profile_photos",
        "module": "users",
        "description": "Get a list of profile pictures for a user",
        "parameters": {
            "user_id": "Unique identifier of the target user",
            "offset": "Number of photos to skip",
            "limit": "Number of photos to return (1-100)"
        }
    },
    
    "getChatMember": {
        "friendly_name": "get_chat_member",
        "module": "users",
        "description": "Get information about a member of a chat",
        "parameters": {
            "chat_id": "Unique identifier of the target chat",
            "user_id": "Unique identifier of the target user"
        }
    },
    
    # Chat methods
    "getChat": {
        "friendly_name": "get_chat",
        "module": "chats",
        "description": "Get basic information about a chat",
        "parameters": {
            "chat_id": "Unique identifier of the target chat"
        }
    },
    
    "getChatAdministrators": {
        "friendly_name": "get_chat_administrators",
        "module": "chats",
        "description": "Get a list of administrators in a chat",
        "parameters": {
            "chat_id": "Unique identifier of the target chat"
        }
    },
    
    "getChatMemberCount": {
        "friendly_name": "get_chat_member_count",
        "module": "chats",
        "description": "Get the number of members in a chat",
        "parameters": {
            "chat_id": "Unique identifier of the target chat"
        }
    },
    
    # Callback query methods
    "answerCallbackQuery": {
        "friendly_name": "answer_callback_query",
        "module": "callback",
        "description": "Send answer to callback query",
        "parameters": {
            "callback_query_id": "Unique identifier for the query to be answered",
            "text": "Text of the notification",
            "show_alert": "If true, an alert will be shown instead of a notification",
            "url": "URL that will be opened by the user's client",
            "cache_time": "Maximum amount of time in seconds that the result of the callback query may be cached"
        }
    },
    
    # File methods
    "getFile": {
        "friendly_name": "get_file",
        "module": "files",
        "description": "Get basic information about files and prepare for downloading",
        "parameters": {
            "file_id": "File identifier to get info about"
        }
    },
    
    # Keyboard methods (these are client-side operations, not API calls)
    "InlineKeyboardMarkup": {
        "friendly_name": "create_inline_keyboard",
        "module": "keyboards",
        "description": "Create an inline keyboard markup",
        "parameters": {
            "buttons": "2D list of button definitions"
        }
    },
    
    "ReplyKeyboardMarkup": {
        "friendly_name": "create_reply_keyboard",
        "module": "keyboards",
        "description": "Create a reply keyboard markup",
        "parameters": {
            "buttons": "2D list of button text",
            "resize_keyboard": "Resize keyboard vertically for optimal fit",
            "one_time_keyboard": "Hide keyboard after use",
            "selective": "Show keyboard only for mentioned users"
        }
    },
    
    "ForceReply": {
        "friendly_name": "create_force_reply",
        "module": "keyboards",
        "description": "Create a force reply markup",
        "parameters": {
            "selective": "Show force reply only for mentioned users"
        }
    },
    
    "ReplyKeyboardRemove": {
        "friendly_name": "remove_keyboard",
        "module": "keyboards",
        "description": "Create a reply keyboard remove markup",
        "parameters": {
            "selective": "Remove keyboard only for mentioned users"
        }
    },
    
    # Payment methods
    "sendInvoice": {
        "friendly_name": "send_invoice",
        "module": "payments",
        "description": "Send invoices",
        "parameters": {
            "chat_id": "Unique identifier for the target chat",
            "title": "Product name",
            "description": "Product description",
            "payload": "Bot-defined invoice payload",
            "provider_token": "Payments provider token",
            "currency": "Three-letter ISO 4217 currency code",
            "prices": "Price breakdown, a list of components"
        }
    },
    
    # Game methods
    "sendGame": {
        "friendly_name": "send_game",
        "module": "games",
        "description": "Send a game",
        "parameters": {
            "chat_id": "Unique identifier for the target chat",
            "game_short_name": "Short name of the game"
        }
    },
    
    # Webhook methods
    "setWebhook": {
        "friendly_name": "set_webhook",
        "module": "webhooks",
        "description": "Specify a url and receive incoming updates via an outgoing webhook",
        "parameters": {
            "url": "HTTPS url to send updates to",
            "certificate": "Upload your public key certificate",
            "max_connections": "Maximum allowed number of simultaneous HTTPS connections to the webhook",
            "allowed_updates": "List the types of updates you want your bot to receive"
        }
    },
    
    "deleteWebhook": {
        "friendly_name": "delete_webhook",
        "module": "webhooks",
        "description": "Remove webhook integration",
        "parameters": {
            "drop_pending_updates": "Pass True to drop all pending updates"
        }
    },
    
    "getWebhookInfo": {
        "friendly_name": "get_webhook_info",
        "module": "webhooks",
        "description": "Get current webhook status",
        "parameters": {}
    },
    
    # Custom NextVibeBot methods (not part of Telegram API)
    "auth.signIn": {
        "friendly_name": "sign_in",
        "module": "auth",
        "description": "Authenticate a user and issue access token",
        "parameters": {
            "user_id": "User's Telegram user ID",
            "username": "User's Telegram username",
            "additional_data": "Additional user data"
        }
    },
    
    "help.getConfig": {
        "friendly_name": "get_config",
        "module": "help",
        "description": "Get bot configuration and settings",
        "parameters": {}
    }
}

# Reverse mapping for easy lookup
FRIENDLY_TO_TL_MAPPING = {
    info["friendly_name"]: {
        "tl_name": tl_name,
        "module": info["module"],
        "description": info["description"],
        "parameters": info["parameters"]
    }
    for tl_name, info in TELEGRAM_TL_MAPPING.items()
}

# Grouped by module for easy navigation
MODULE_GROUPINGS = {
    "messages": [
        "sendMessage", "editMessageText", "deleteMessage", 
        "sendPhoto", "sendVoice", "sendDocument"
    ],
    "users": [
        "getMe", "getUserProfilePhotos", "getChatMember"
    ],
    "chats": [
        "getChat", "getChatAdministrators", "getChatMemberCount"
    ],
    "callback": [
        "answerCallbackQuery", "editMessageText", "editMessageCaption"
    ],
    "keyboards": [
        "InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ForceReply", "ReplyKeyboardRemove"
    ],
    "files": [
        "getFile"
    ],
    "payments": [
        "sendInvoice"
    ],
    "games": [
        "sendGame"
    ],
    "webhooks": [
        "setWebhook", "deleteWebhook", "getWebhookInfo"
    ],
    "auth": [
        "auth.signIn"
    ],
    "help": [
        "help.getConfig"
    ]
}

# Method aliases for common operations
METHOD_ALIASES = {
    "send": "sendMessage",
    "edit": "editMessageText", 
    "delete": "deleteMessage",
    "photo": "sendPhoto",
    "voice": "sendVoice",
    "document": "sendDocument",
    "me": "getMe",
    "chat": "getChat",
    "admin": "getChatAdministrators",
    "count": "getChatMemberCount",
    "answer": "answerCallbackQuery",
    "file": "getFile",
    "webhook": "setWebhook"
}


def get_tl_method_info(tl_method_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a Telegram TL method
    
    Args:
        tl_method_name: The TL method name (e.g., 'sendMessage')
        
    Returns:
        Dictionary with method information or None if not found
    """
    return TELEGRAM_TL_MAPPING.get(tl_method_name)


def get_friendly_method_info(friendly_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a friendly method name
    
    Args:
        friendly_name: The friendly method name (e.g., 'send_message')
        
    Returns:
        Dictionary with method information or None if not found
    """
    return FRIENDLY_TO_TL_MAPPING.get(friendly_name)


def get_method_by_alias(alias: str) -> Optional[str]:
    """
    Get TL method name by alias
    
    Args:
        alias: The method alias
        
    Returns:
        TL method name or None if not found
    """
    return METHOD_ALIASES.get(alias)


def list_methods_by_module(module: str) -> List[str]:
    """
    List all methods in a specific module
    
    Args:
        module: The module name
        
    Returns:
        List of TL method names in the module
    """
    return MODULE_GROUPINGS.get(module, [])


def get_all_modules() -> List[str]:
    """
    Get list of all available modules
    
    Returns:
        List of module names
    """
    return list(MODULE_GROUPINGS.keys())


def get_method_summary() -> Dict[str, Any]:
    """
    Get a summary of all available methods
    
    Returns:
        Dictionary with method counts and module breakdown
    """
    return {
        "total_methods": len(TELEGRAM_TL_MAPPING),
        "modules": {module: len(methods) for module, methods in MODULE_GROUPINGS.items()},
        "aliases": len(METHOD_ALIASES)
    }