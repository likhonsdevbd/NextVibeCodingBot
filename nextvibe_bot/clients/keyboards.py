"""
Keyboard client for creating and managing keyboards
"""

import logging
from typing import List, Union, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from ..types import RequestResult
from .base import BaseClient

logger = logging.getLogger(__name__)


class KeyboardClient(BaseClient):
    """
    Client for keyboard operations - creating inline keyboards, reply keyboards, etc.
    """
    
    async def create_inline_keyboard(
        self,
        buttons: List[List[dict]]
    ) -> RequestResult:
        """
        Create an inline keyboard markup from button definitions
        
        Args:
            buttons: 2D list of button definitions. Each button dict should contain:
                - text: Button text
                - callback_data: For callback buttons
                - url: For URL buttons
                - switch_inline_query: For inline query switch
                
        Returns:
            RequestResult with InlineKeyboardMarkup on success
        """
        try:
            keyboard_rows = []
            
            for row in buttons:
                keyboard_row = []
                for button_def in row:
                    if 'callback_data' in button_def:
                        keyboard_row.append(
                            InlineKeyboardButton(
                                text=button_def['text'],
                                callback_data=button_def['callback_data']
                            )
                        )
                    elif 'url' in button_def:
                        keyboard_row.append(
                            InlineKeyboardButton(
                                text=button_def['text'],
                                url=button_def['url']
                            )
                        )
                    elif 'switch_inline_query' in button_def:
                        keyboard_row.append(
                            InlineKeyboardButton(
                                text=button_def['text'],
                                switch_inline_query=button_def['switch_inline_query']
                            )
                        )
                    else:
                        # Default to callback button
                        keyboard_row.append(
                            InlineKeyboardButton(
                                text=button_def['text'],
                                callback_data=button_def.get('callback_data', button_def['text'])
                            )
                        )
                keyboard_rows.append(keyboard_row)
            
            reply_markup = InlineKeyboardMarkup(keyboard_rows)
            logger.info("Created inline keyboard successfully")
            return RequestResult(success=True, data=reply_markup)
            
        except Exception as e:
            logger.error(f"Failed to create inline keyboard: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def create_reply_keyboard(
        self,
        buttons: List[List[str]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False
    ) -> RequestResult:
        """
        Create a reply keyboard markup
        
        Args:
            buttons: 2D list of button text
            resize_keyboard: Resize keyboard vertically for optimal fit
            one_time_keyboard: Hide keyboard after use
            selective: Show keyboard only for mentioned users
            
        Returns:
            RequestResult with ReplyKeyboardMarkup on success
        """
        try:
            reply_markup = ReplyKeyboardMarkup(
                keyboard=buttons,
                resize_keyboard=resize_keyboard,
                one_time_keyboard=one_time_keyboard,
                selective=selective
            )
            
            logger.info("Created reply keyboard successfully")
            return RequestResult(success=True, data=reply_markup)
            
        except Exception as e:
            logger.error(f"Failed to create reply keyboard: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def create_force_reply(
        self,
        selective: bool = False
    ) -> RequestResult:
        """
        Create a force reply markup
        
        Args:
            selective: Show force reply only for mentioned users
            
        Returns:
            RequestResult with ForceReply on success
        """
        try:
            from telegram import ForceReply
            reply_markup = ForceReply(selective=selective)
            
            logger.info("Created force reply successfully")
            return RequestResult(success=True, data=reply_markup)
            
        except Exception as e:
            logger.error(f"Failed to create force reply: {e}")
            return RequestResult(success=False, error=str(e))
    
    async def remove_keyboard(
        self,
        selective: bool = False
    ) -> RequestResult:
        """
        Create a reply keyboard remove markup
        
        Args:
            selective: Remove keyboard only for mentioned users
            
        Returns:
            RequestResult with ReplyKeyboardRemove on success
        """
        try:
            from telegram import ReplyKeyboardRemove
            reply_markup = ReplyKeyboardRemove(selective=selective)
            
            logger.info("Created keyboard remove successfully")
            return RequestResult(success=True, data=reply_markup)
            
        except Exception as e:
            logger.error(f"Failed to create keyboard remove: {e}")
            return RequestResult(success=False, error=str(e))