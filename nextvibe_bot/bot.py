"""
Main Telegram bot application for NextVibeCodingBot
"""

import asyncio
import logging
from typing import Dict, Any, List

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

from .config import settings
from .handlers.command_handlers import start_handler, help_handler, error_handler
from .handlers.message_handler import message_handler_func as message_handler
from .handlers import callback_handlers


class NextVibeBot:
    """Main bot application class"""
    
    def __init__(self):
        self.application = None
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, settings.log_level))
        
        # Create logs directory if it doesn't exist
        import os
        os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
        
    async def initialize(self):
        """Initialize the bot application"""
        self.logger.info("Initializing NextVibeCodingBot...")
        
        # Create application
        self.application = (
            Application.builder()
            .token(settings.telegram_bot_token)
            .build()
        )
        
        # Add handlers
        self._add_handlers()
        
        self.logger.info("Bot initialized successfully")
        
    def _add_handlers(self):
        """Add message and command handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", start_handler))
        self.application.add_handler(CommandHandler("help", help_handler))
        self.application.add_handler(CommandHandler("cancel", self._cancel_handler))
        
        # Message handlers - handle text, voice and other message types in a single handler
        # Using a broad filter so we can branch on the message content inside the handler
        self.application.add_handler(
            MessageHandler(filters.ALL & ~filters.COMMAND, message_handler)
        )
        
        # Callback query handlers
        for handler in callback_handlers:
            self.application.add_handler(handler)
        
        # Error handler
        self.application.add_error_handler(error_handler)
        
    async def start(self):
        """Start the bot"""
        try:
            await self.initialize()
            self.logger.info("Starting NextVibeCodingBot...")
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            self.logger.info("Bot is now running...")
            
            # Keep the bot running
            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                self.logger.info("Received shutdown signal")
            finally:
                await self.stop()
                
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            raise
            
    async def stop(self):
        """Stop the bot"""
        self.logger.info("Stopping NextVibeCodingBot...")
        if self.application:
            await self.application.stop()
            await self.application.shutdown()
        self.logger.info("Bot stopped")
        
    async def _cancel_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle cancel command"""
        await update.message.reply_text(
            "❌ Task cancelled. You can send me a new coding task anytime!"
        )


# Global bot instance
bot = NextVibeBot()


async def main():
    """Main entry point"""
    await bot.start()


if __name__ == "__main__":
    import sys
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Bot failed to start: {e}")
        sys.exit(1)