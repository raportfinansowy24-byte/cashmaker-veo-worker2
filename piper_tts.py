import os
import subprocess
import tempfile
import logging
from typing import Optional

logger = logging.getLogger(__name__)

MODEL = "pl_PL-mc_speech-medium"


def generate_piper_tts(text: str) -> Optional[bytes]:
    """Generate Polish TTS audio using Piper with the pl_PL-mc_speech-medium model.

    Calls the `piper` command-line tool via subprocess, writes the input text
    to a temporary file, and reads back the resulting WAV audio bytes.

    Args:
        text: The Polish text to synthesise.

    Returns:
        WAV audio bytes on success, or None if Piper fails.
    """
    input_file = None
    output_file = None
    try:
        # Write input text to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(text)
            input_file = f.name

        # Prepare a temporary output WAV path
        output_fd, output_file = tempfile.mkstemp(suffix=".wav")
        os.close(output_fd)

        cmd = [
            "piper",
            "--model", MODEL,
            "--output_file", output_file,
        ]

        logger.info(f"🔊 Piper TTS: synthesising with model '{MODEL}'...")

        with open(input_file, "r", encoding="utf-8") as stdin_f:
            result = subprocess.run(
                cmd,
                stdin=stdin_f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=120,
            )

        if result.returncode != 0:
            logger.error(
                f"❌ Piper TTS failed (exit {result.returncode}): "
                f"{result.stderr.decode('utf-8', errors='replace')}"
            )
            return None

        with open(output_file, "rb") as f:
            audio_bytes = f.read()

        logger.info(f"✅ Piper TTS: generated {len(audio_bytes)} bytes of WAV audio")
        return audio_bytes

    except FileNotFoundError:
        logger.error(
            "❌ Piper TTS: 'piper' executable not found. "
            "Ensure piper-tts is installed and available on PATH."
        )
        return None
    except subprocess.TimeoutExpired:
        logger.error("❌ Piper TTS: subprocess timed out after 120 seconds")
        return None
    except Exception as e:
        logger.error(f"❌ Piper TTS: unexpected error: {e}")
        return None
    finally:
        # Clean up temporary files
        for path in (input_file, output_file):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass
