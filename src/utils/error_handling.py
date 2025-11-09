"""
Error handling utilities for the NextVibe bot.
"""
from functools import wraps
from loguru import logger
from telegram import Update
from telegram.ext import ContextTypes

def handle_errors(func):
    """
    Decorator for handling errors in bot handlers.
    """
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            # Log the error
            logger.error(f"Error in {func.__name__}: {str(e)}")
            
            # Send error message to user
            error_message = "Sorry, I encountered an error while processing your request. Please try again."
            if update.message:
                await update.message.reply_text(error_message)
            
            # Re-raise for global error handler
            raise
            
    return wrapper