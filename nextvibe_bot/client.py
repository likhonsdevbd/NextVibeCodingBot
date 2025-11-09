"""
Main client library for NextVibeBot
"""

import logging
from typing import Optional, Dict, Any
from telegram import Bot
from telegram.ext import Application

from .messages import MessageClient
from .keyboards import KeyboardClient
from .users import UserClient
from .chats import ChatClient
from .callback import CallbackClient
from .files import FileClient
from .payments import PaymentClient
from .games import GameClient
from .webhooks import WebhookClient
from .auth import AuthClient
from .help import HelpClient

logger = logging.getLogger(__name__)


class NextVibeClient:
    """
    Main client for NextVibeBot that provides access to all Telegram Bot API methods
    through organized, typed client modules.
    """
    
    def __init__(self, token: str, application: Optional[Application] = None):
        """
        Initialize the NextVibe client
        
        Args:
            token: Bot token from @BotFather
            application: Optional pre-configured application instance
        """
        self.token = token
        self._application = application
        self._bot = None
        
        # Initialize client modules
        self.messages = MessageClient(self)
        self.keyboards = KeyboardClient(self)
        self.users = UserClient(self)
        self.chats = ChatClient(self)
        self.callback = CallbackClient(self)
        self.files = FileClient(self)
        self.payments = PaymentClient(self)
        self.games = GameClient(self)
        self.webhooks = WebhookClient(self)
        self.auth = AuthClient(self)
        self.help = HelpClient(self)
        
        logger.info("NextVibeClient initialized")
    
    @property
    def bot(self) -> Bot:
        """Get or create bot instance"""
        if self._bot is None:
            self._bot = Bot(token=self.token)
        return self._bot
    
    @property
    def application(self) -> Optional[Application]:
        """Get the underlying application instance"""
        return self._application
    
    async def close(self) -> None:
        """Close the client and clean up resources"""
        logger.info("Closing NextVibeClient")
        if self._application:
            await self._application.stop()
            await self._application.shutdown()
        logger.info("NextVibeClient closed")
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    def get_config(self) -> Dict[str, Any]:
        """Get current client configuration"""
        return {
            "token_set": bool(self.token),
            "has_application": self._application is not None,
            "modules": {
                "messages": hasattr(self.messages, 'send_message'),
                "keyboards": hasattr(self.keyboards, 'create_inline_keyboard'),
                "users": hasattr(self.users, 'get_me'),
                "chats": hasattr(self.chats, 'get_chat'),
                "callback": hasattr(self.callback, 'answer_callback_query'),
                "files": hasattr(self.files, 'get_file'),
                "payments": hasattr(self.payments, 'send_invoice'),
                "games": hasattr(self.games, 'send_game'),
                "webhooks": hasattr(self.webhooks, 'set_webhook'),
                "auth": hasattr(self.auth, 'sign_in'),
                "help": hasattr(self.help, 'get_config')
            }
        }