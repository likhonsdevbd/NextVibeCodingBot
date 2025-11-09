"""
File client for file operations
"""

import logging
from typing import Optional, Union
from telegram import InputFile

from ..types import RequestResult
from .base import BaseClient

logger = logging.getLogger(__name__)


class FileClient(BaseClient):
    """
    Client for file operations
    """
    
    async def get_file(self, file_id: str) -> RequestResult:
        """Get file information"""
        try:
            file_obj = await self.bot.get_file(file_id=file_id)
            
            file_info = {
                "file_id": file_obj.file_id,
                "file_unique_id": file_obj.file_unique_id,
                "file_size": getattr(file_obj, 'file_size', None),
                "file_path": getattr(file_obj, 'file_path', None)
            }
            
            logger.info(f"Retrieved file info for {file_id}")
            return RequestResult(success=True, data=file_info)
            
        except Exception as e:
            logger.error(f"Failed to get file {file_id}: {e}")
            return RequestResult(success=False, error=str(e))

    async def download_file(self, file_id: str, destination: Optional[str] = None) -> RequestResult:
        """Download file to local"""
        try:
            file_obj = await self.bot.get_file(file_id=file_id)
            
            if destination:
                await file_obj.download_to_drive(destination)
                logger.info(f"Downloaded file {file_id} to {destination}")
            else:
                content = await file_obj.download_as_bytearray()
                logger.info(f"Downloaded file {file_id} to memory")
            
            return RequestResult(success=True, data=True)
            
        except Exception as e:
            logger.error(f"Failed to download file {file_id}: {e}")
            return RequestResult(success=False, error=str(e))