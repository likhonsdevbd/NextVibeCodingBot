#!/usr/bin/env python3
"""
Main entry point for NextVibeCodingBot
"""

import asyncio
import logging
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nextvibe_bot.bot import NextVibeBot


def setup_logging():
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


async def main():
    """Main entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting NextVibeCodingBot...")
    
    # Check if bot token is configured
    from nextvibe_bot.config import settings
    if not settings.telegram_bot_token or settings.telegram_bot_token == "your_bot_token_here":
        logger.error("Bot token not configured! Please set TELEGRAM_BOT_TOKEN in .env file")
        sys.exit(1)
    
    try:
        # Create and run the bot
        bot = NextVibeBot()
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Bot failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
        sys.exit(0)