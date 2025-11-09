"""
Main bot module that handles the core Telegram bot functionality.
"""
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from loguru import logger
from config.settings import Settings

class NextVibeBot:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.app = Application.builder().token(settings.telegram_token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up message and command handlers"""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self._start_command))
        self.app.add_handler(CommandHandler("help", self._help_command))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        welcome_message = (
            "👋 Welcome to NextVibe Coding Bot!\n\n"
            "I'm your autonomous coding assistant. I can help with:\n"
            "• 🐛 Bug fixes\n"
            "• ✨ Feature implementations\n"
            "• 🛠 Code improvements\n\n"
            "Just send me your coding task and I'll help you out!"
        )
        await update.message.reply_text(welcome_message)

    async def _help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_message = (
            "🔍 NextVibe Bot Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n\n"
            "To submit a coding task, simply send me a message describing:\n"
            "1. The type of task (bug/feature/improvement)\n"
            "2. Description of what needs to be done\n"
            "3. Any relevant code or context\n"
        )
        await update.message.reply_text(help_message)

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        try:
            # Log incoming message
            logger.info(f"Received message: {update.message.text}")
            
            # TODO: Implement task parsing and routing
            await update.message.reply_text(
                "I've received your message. Task processing functionality coming soon!"
            )
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await update.message.reply_text(
                "Sorry, I encountered an error while processing your request. Please try again."
            )

    def run(self):
        """Start the bot"""
        logger.info("Starting NextVibe Bot...")
        self.app.run_polling()