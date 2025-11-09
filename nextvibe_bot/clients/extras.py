"""
Payment, game, and webhook client modules for NextVibeBot
"""

import logging
from typing import Optional, Dict, Any, List

from ..types import RequestResult
from .base import BaseClient

logger = logging.getLogger(__name__)


class PaymentClient(BaseClient):
    """Client for payment operations"""
    
    async def send_invoice(
        self,
        chat_id,
        title: str,
        description: str,
        payload: str,
        provider_token: str = None,
        currency: str = "USD",
        prices: List[Dict] = None
    ) -> RequestResult:
        """Send invoice (stub implementation)"""
        try:
            # Stub implementation
            logger.info(f"Invoice sent to {chat_id}: {title}")
            return RequestResult(success=True, data={"invoice_sent": True})
        except Exception as e:
            return RequestResult(success=False, error=str(e))


class GameClient(BaseClient):
    """Client for game operations"""
    
    async def send_game(
        self,
        chat_id,
        game_short_name: str
    ) -> RequestResult:
        """Send game (stub implementation)"""
        try:
            # Stub implementation
            logger.info(f"Game sent to {chat_id}: {game_short_name}")
            return RequestResult(success=True, data={"game_sent": True})
        except Exception as e:
            return RequestResult(success=False, error=str(e))


class WebhookClient(BaseClient):
    """Client for webhook operations"""
    
    async def set_webhook(
        self,
        url: str,
        certificate: Optional[str] = None,
        max_connections: Optional[int] = None,
        allowed_updates: Optional[List[str]] = None
    ) -> RequestResult:
        """Set webhook URL"""
        try:
            result = await self.bot.set_webhook(
                url=url,
                certificate=certificate,
                max_connections=max_connections,
                allowed_updates=allowed_updates
            )
            logger.info(f"Webhook set to {url}")
            return RequestResult(success=True, data=result)
        except Exception as e:
            logger.error(f"Failed to set webhook: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def delete_webhook(
        self,
        drop_pending_updates: bool = False
    ) -> RequestResult:
        """Delete webhook"""
        try:
            result = await self.bot.delete_webhook(drop_pending_updates=drop_pending_updates)
            logger.info("Webhook deleted")
            return RequestResult(success=True, data=result)
        except Exception as e:
            logger.error(f"Failed to delete webhook: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def get_webhook_info(self) -> RequestResult:
        """Get webhook info"""
        try:
            webhook_info = await self.bot.get_webhook_info()
            logger.info("Retrieved webhook info")
            return RequestResult(success=True, data=webhook_info)
        except Exception as e:
            logger.error(f"Failed to get webhook info: {e}")
            return RequestResult(success=False, error=str(e))