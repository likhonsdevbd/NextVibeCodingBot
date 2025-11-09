"""
Enhanced Message handler for processing coding tasks with Telegram Bot API 9.2 features
"""

import asyncio
import logging
import re
class MessageHandler:
    """Main message handler for coding tasks"""

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.task_parser = TaskParser()
        self.code_analyzer = CodeAnalyzer()
        self.code_executor = CodeExecutor()
        self.response_formatter = ResponseFormatter()
        self.voice_transcriber = VoiceTranscriber()
        self.ai_client = AIClient()

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main message handler"""
        user_id = update.effective_user.id
        user = update.effective_user
        message = update.message

        # Determine message content type
        message_text = message.text if message and message.text else None

        # Check rate limiting
        if not await self.rate_limiter.is_allowed(user_id):
            await update.message.reply_text(
                "⏰ You're sending messages too quickly. Please wait a moment before sending another request."
            )
            return

        # Log the incoming message
        logger.info(f"Processing message from {user.username or user.id}: { (message_text or str(getattr(message,'chat_id', user_id)))[:100]}...")

        try:
            # If message contains a voice note, handle transcription flow
            if message and getattr(message, "voice", None):
                await self._handle_voice_message(update, context)
                return

            # If message contains web app data (from Mini App), handle it
            if message and getattr(message, "web_app_data", None):
                await self._handle_web_app_data(update, context)
                return

            # If the incoming message is not text, acknowledge and proceed
            if not message_text:
                await message.reply_text(
                    "Received your message — I currently process text and voice. "
                    "If you sent a file or web app data, please describe what you'd like me to do with it."
                )
                return

            # Send initial processing message
            processing_msg = await update.message.reply_text(
                "🤖 *Processing your request...*",
                parse_mode=ParseMode.MARKDOWN
            )

            # Parse the message to identify task type and details
            task_info = await self.task_parser.parse_message(message_text)
            logger.info(f"Parsed task: {task_info}")

            # Update processing message
            await processing_msg.edit_text(
                f"� *Analyzing your request...*\\n"
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

                prefer_large_media=False,
                show_above_text=False
            ),
            # API 9.2: Message effects for better user experience
            message_effect_id=MessageEffectType.typing
        )
        
        try:
            # Parse the message to identify task type and details
            task_info = await self.task_parser.parse_message(message_text)
            logger.info(f"Parsed task: {task_info}")
            
            # Update processing message with enhanced feedback
            await processing_msg.edit_text(
                f"🔍 *Analyzing your request...*\n"
                f"Task type: {task_info['task_type']}\n"
                f"Language: {task_info.get('language', 'auto-detect')}",
                parse_mode=ParseMode.MARKDOWN,
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
            
            # Analyze the task
            analysis = await self.code_analyzer.analyze_task(task_info)
            
            # Update processing message  
            await processing_msg.edit_text(
                f"💭 *Thinking about the solution...*\n"
                f"Task: {task_info['task_type']}\n"
                f"Status: Analysis complete",
                parse_mode=ParseMode.MARKDOWN,
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
            
            # Execute the task (if applicable)
            if analysis.get('executable'):
                execution_result = await self.code_executor.execute(analysis)
                analysis['execution_result'] = execution_result
                
                await processing_msg.edit_text(
                    "⚡ *Executing and testing...*",
                    parse_mode=ParseMode.MARKDOWN,
                    message_effect_id=MessageEffectType.success
                )
            else:
                analysis['execution_result'] = None
                
            # Format and send the response with API 9.2 enhancements
            response = await self.response_formatter.format_response(analysis)
            await processing_msg.delete()
            
            # API 9.2: Enhanced response with link preview options for code sharing
            if 'http' in response:
                await message.reply_text(
                    response, 
                    parse_mode=ParseMode.MARKDOWN,
                    link_preview_options=LinkPreviewOptions(
                        is_disabled=False,
                        prefer_small_media=True,
                        show_above_text=False
                    )
                )
            else:
                await message.reply_text(
                    response, 
                    parse_mode=ParseMode.MARKDOWN,
                    link_preview_options=LinkPreviewOptions(is_disabled=True)
                )
            
            # Log successful completion
            logger.info(f"Successfully processed task for user {user.id}")
            
        except Exception as e:
            logger.error(f"Error processing text message: {e}", exc_info=True)
            await processing_msg.edit_text(
                f"❌ *Error processing your request*\n\n"
                f"```\n{str(e)}\n```\n\n"
                f"Please try again or contact support if the problem persists.",
                parse_mode=ParseMode.MARKDOWN
            )
            
    async def _handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages with API 9.2 enhancements"""
        message = update.message
        user = update.effective_user
        
        logger.info(f"Processing voice message from {user.username or user.id}")
        
        # Acknowledge receipt with API 9.2 features
        ack = await message.reply_text(
            "🎧 Received your voice message — transcribing now...",
            message_effect_id=MessageEffectType.typing
        )
        
        try:
            # Voice transcription logic would go here
            # For now, just provide a placeholder response
            await ack.edit_text(
                "🎤 *Voice message received!*\n\n"
                "I'm currently processing your voice message. "
                "Voice transcription and code analysis will be available soon!\n\n"
                "💡 *Tip:* You can also send me text messages with your coding questions.",
                parse_mode=ParseMode.MARKDOWN,
                message_effect_id=MessageEffectType.success
            )
            
        except Exception as e:
            logger.error(f"Voice message processing failed: {e}", exc_info=True)
            await ack.edit_text(
                "❌ Failed to process the voice message. Please try again later.",
                message_effect_id=MessageEffectType.error
            )
            
    async def _handle_web_app_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle web app data (API 9.2 feature)"""
        message = update.message
        web_app_data = message.web_app_data
        
        try:
            if web_app_data and hasattr(web_app_data, 'data'):
                # Process web app data
                data = web_app_data.data
                logger.info(f"Received web app data: {data}")
                
                await message.reply_text(
                    f"🌐 *Web app data received!*\n\n"
                    f"```\n{data}\n```\n\n"
                    f"Thanks for using the web interface!",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await message.reply_text(
                    "🌐 Web app interaction received! Please try again or use text messaging.",
                    message_effect_id=MessageEffectType.typing
                )
                
        except Exception as e:
            logger.error(f"Failed to handle web app data: {e}")
            await message.reply_text(
                "❌ Failed to process web app data. Please try again.",
                message_effect_id=MessageEffectType.error
            )
            
    async def _handle_direct_message_topic(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle direct messages in channels (API 9.2 feature)"""
        message = update.message
        topic = message.direct_messages_topic
        
        logger.info(f"Processing direct message topic: {topic.topic_id if topic else 'Unknown'}")
        
        await message.reply_text(
            "📨 *Direct message in channel received!*\n\n"
            "I'm currently processing your request through the direct messages channel. "
            "I'll get back to you shortly!",
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def _handle_suggested_post(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle suggested posts (API 9.2 feature)"""
        message = update.message
        suggested_info = message.suggested_post_info
        
        logger.info(f"Processing suggested post: {suggested_info.state if suggested_info else 'Unknown'}")
        
        # This would typically be handled by channel administrators
        await message.reply_text(
            "📋 *Suggested post received!*\n\n"
            "This appears to be a suggested post for a channel. "
            "Please contact a channel administrator to process this request.",
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def _handle_checklist_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle checklist messages (API 9.2 feature)"""
        message = update.message
        checklist = message.checklist
        
        logger.info(f"Processing checklist: {checklist.title if checklist else 'Unknown'}")
        
        await message.reply_text(
            "✅ *Checklist received!*\n\n"
            f"Title: {checklist.title if checklist else 'Unknown'}\n"
            f"Tasks: {len(checklist.tasks) if checklist and hasattr(checklist, 'tasks') else 0}\n\n"
            "I'm currently processing your checklist. Feature support coming soon!",
            parse_mode=ParseMode.MARKDOWN
        )


# Global message handler instance
message_handler = MessageHandler()


# Message handler function for the bot
async def message_handler_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main message handler function"""
    await message_handler.handle_message(update, context)