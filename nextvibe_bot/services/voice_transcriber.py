"""
Voice transcription service (lightweight stub)

This module provides a VoiceTranscriber class that can be extended to call
an external transcription service (OpenAI Whisper, AssemblyAI, etc.). For
now it implements a safe stub that attempts to download the voice file and
returns a helpful message if no external service is configured.
"""

import logging
import tempfile
import os
from typing import Dict, Any

from ..config import settings

logger = logging.getLogger(__name__)


class VoiceTranscriber:
    """Lightweight voice transcription service.

    Usage:
        transcriber = VoiceTranscriber()
        result = await transcriber.transcribe(message)

    Returns a dict with at least the `text` key when transcription is available.
    """

    def __init__(self):
        # Placeholder for real client initialization (e.g., OpenAI, AssemblyAI)
        self.enabled = bool(settings.openai_api_key or settings.anthropic_api_key)

    async def transcribe(self, message) -> Dict[str, Any]:
        """Transcribe a voice message.

        Args:
            message: telegram.Message instance containing .voice

        Returns:
            dict: {"text": str or None, "meta": {...}}
        """
        try:
            if not message or not getattr(message, "voice", None):
                return {"text": None, "meta": {"reason": "no_voice"}}

            # Try to download the voice file to a temporary location if the API supports it
            try:
                voice = message.voice
                file = await voice.get_file()
                tmp_dir = tempfile.mkdtemp(prefix="nextvibe_voice_")
                local_path = os.path.join(tmp_dir, f"voice_{voice.file_unique_id}.ogg")

                # download_to_drive is supported in python-telegram-bot >= 20; fall back to download
                try:
                    await file.download_to_drive(local_path)
                except Exception:
                    try:
                        # older method
                        await file.download(custom_path=local_path)
                    except Exception:
                        # If download fails, continue without the file
                        local_path = None

            except Exception as e:
                logger.debug(f"Failed to download voice file: {e}")
                local_path = None

            # If transcription service is not configured, return helpful message
            if not self.enabled:
                return {
                    "text": None,
                    "meta": {
                        "local_path": local_path,
                        "reason": "transcription_service_not_configured",
                        "hint": "Set OPENAI_API_KEY or another transcription provider in the .env to enable automatic transcription."
                    }
                }

            # Real transcription integration point
            # e.g. call OpenAI/AssemblyAI/whisper here and return the text
            # For safety we return a placeholder until a provider is implemented
            return {
                "text": "(Transcription service enabled but not implemented in this deployment)",
                "meta": {"local_path": local_path}
            }

        except Exception as e:
            logger.error(f"VoiceTranscriber error: {e}")
            return {"text": None, "meta": {"error": str(e)}}
