"""
Command handlers for NextVibeCodingBot
"""

import logging
from typing import Any

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..config import settings


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_text = f"""
🤖 *Welcome to {settings.bot_name}!*

I'm an autonomous coding agent that can help you with:

• 🐛 **Bug fixes** - Find and fix errors in your code
• ⚡ **Feature development** - Implement new functionality  
• 🔍 **Code analysis** - Review and optimize your code
• 🛠️ **Debugging** - Help troubleshoot issues
• 📚 **General coding** - Answer questions and provide guidance

*How to use:*
Simply send me a message describing your coding task. I'll analyze it and provide a solution!

*Supported languages:* Python, JavaScript, TypeScript, Java, C++, Go, Rust, PHP, Ruby, and more.

Type /help for more information or just tell me what you need help with! 💻
"""
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = f"""
📚 *{settings.bot_name} Help*

*What I can do:*
• Fix bugs and errors in your code
• Add new features and functionality  
• Analyze and review your code
• Debug and troubleshoot issues
• Answer programming questions
• Execute and test code safely

*How to get started:*
1. Send me your code or describe your problem
2. I'll analyze it and propose a solution
3. I can execute the code to verify it works
4. I'll provide a complete response

*Example messages:*
• "My Python script is throwing a TypeError, help me fix it"
• "Add a login feature to my Flask app"
• "Optimize this JavaScript function for better performance"  
• "Debug why my API calls are failing"

*Commands:*
• /start - Welcome message
• /help - This help message
• /cancel - Cancel current task

Ready to help! Just send me your coding task! 🚀
"""
    
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger = logging.getLogger(__name__)
    
    # Log the error
    logger.error(
        f"Exception while handling an update: {context.error}",
        exc_info=context.error
    )
    
    # Send error message to user if update exists
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ Sorry, I encountered an error while processing your request. "
                "Please try again or contact support if the problem persists."
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")