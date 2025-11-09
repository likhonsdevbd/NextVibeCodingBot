"""
Message handler for processing coding tasks
"""

import asyncio
import logging
import re
from typing import Dict, Any, Optional
import json
import hashlib

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from ..config import settings, TASK_PATTERNS
from ..services import (
    TaskParser, 
    CodeAnalyzer, 
    CodeExecutor, 
    ResponseFormatter
)
from ..utils.rate_limiter import RateLimiter


logger = logging.getLogger(__name__)


class MessageHandler:
    """Main message handler for coding tasks"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.task_parser = TaskParser()
        self.code_analyzer = CodeAnalyzer()
        self.code_executor = CodeExecutor()
        self.response_formatter = ResponseFormatter()
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main message handler"""
        user_id = update.effective_user.id
        message_text = update.message.text
        user = update.effective_user
        
        # Check rate limiting
        if not await self.rate_limiter.is_allowed(user_id):
            await update.message.reply_text(
                "⏰ You're sending messages too quickly. Please wait a moment before sending another request."
            )
            return
            
        # Log the incoming message
        logger.info(f"Processing message from {user.username or user.id}: {message_text[:100]}...")
        
        # Send initial processing message
        processing_msg = await update.message.reply_text(
            "🤖 *Processing your request...*",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            # Parse the message to identify task type and details
            task_info = await self.task_parser.parse_message(message_text)
            logger.info(f"Parsed task: {task_info}")
            
            # Update processing message
            await processing_msg.edit_text(
                f"🔍 *Analyzing your request...*\\n"
                f"Task type: {task_info['task_type']}\\n"
                f"Language: {task_info.get('language', 'auto-detect')}",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Analyze the task
            analysis = await self.code_analyzer.analyze_task(task_info)
            
            # Update processing message  
            await processing_msg.edit_text(
                f"💭 *Thinking about the solution...*\\n"
                f"Task: {task_info['task_type']}\\n"
                f"Status: Analysis complete",
                parse_mode=ParseMode.MARKDOWN
            )
            
            # Execute the task (if applicable)
            if analysis.get('executable'):
                execution_result = await self.code_executor.execute(analysis)
                analysis['execution_result'] = execution_result
                
                await processing_msg.edit_text(
                    "⚡ *Executing and testing...*",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                analysis['execution_result'] = None
                
            # Format and send the response
            response = await self.response_formatter.format_response(analysis)
            await processing_msg.delete()
            await update.message.reply_text(response, parse_mode=ParseMode.MARKDOWN)
            
            # Log successful completion
            logger.info(f"Successfully processed task for user {user.id}")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            await processing_msg.edit_text(
                f"❌ *Error processing your request*\\n\\n"
                f"```\\n{str(e)}\\n```\\n\\n"
                f"Please try again or contact support if the problem persists.",
                parse_mode=ParseMode.MARKDOWN
            )


# Global message handler instance
message_handler = MessageHandler()


# Message handler function for the bot
async def message_handler_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main message handler function"""
    await message_handler.handle_message(update, context)