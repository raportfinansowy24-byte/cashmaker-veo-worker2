"""
Kokoro TTS client using the official free Hugging Face Space by hexgrad.
Space: https://huggingface.co/spaces/hexgrad/Kokoro-82M
No API credits required.
"""

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

KOKORO_SPACE_URL = "https://hexgrad-kokoro-82m.hf.space/api/predict"


def generate_kokoro_tts(text: str, voice: str = "af_bella") -> Optional[bytes]:
    """
    Generate speech audio using the free Kokoro-82M HuggingFace Space.

    Args:
        text: The text to synthesise.
        voice: Kokoro voice ID (default: "af_bella").

    Returns:
        Raw WAV audio bytes, or None if the request fails.
    """
    payload = {
        "text": text,
        "voice": voice,
        "speed": 1.0,
    }

    try:
        logger.info(f"🔊 Calling Kokoro-82M HF Space for TTS ({len(text)} chars)...")
        response = requests.post(
            KOKORO_SPACE_URL,
            json=payload,
            timeout=120,
        )
        response.raise_for_status()

        audio_bytes = response.content
        if not audio_bytes:
            logger.error("❌ Kokoro TTS returned empty response body.")
            return None

        logger.info(f"✅ Kokoro TTS generated {len(audio_bytes)} bytes of audio.")
        return audio_bytes

    except requests.exceptions.Timeout:
        logger.error("❌ Kokoro TTS request timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ Kokoro TTS HTTP error: {e} – status {e.response.status_code}")
        return None
    except Exception as e:
        logger.error(f"❌ Kokoro TTS unexpected error: {e}")
        return None
