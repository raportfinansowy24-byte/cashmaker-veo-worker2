#!/usr/bin/env python3
"""Fix the generate_tts_audio_narration function to use Piper instead of Kokoro."""

import re

with open('server.py', 'r') as f:
    content = f.read()

# Find and replace the entire function
old_pattern = r'def generate_tts_audio_narration\(narration_texts, job_id\):.*?return audio_files'

new_func = '''def generate_tts_audio_narration(narration_texts, job_id):
    """Create real audio files using Piper TTS with Polish language support."""
    audio_files = {}
    for scene_key, text in narration_texts.items():
        audio_file = os.path.join(tempfile.gettempdir(), f"narration_{scene_key}_{job_id}.wav")
        
        if os.path.exists(audio_file):
            logger.info(f"⏩ Audio {scene_key} już istnieje – pomijam.")
            duration = vp.get_audio_duration(audio_file)
            audio_files[scene_key] = {"path": audio_file, "duration": duration, "text": text}
            continue

        logger.info(f"🔊 Generuję TTS (Piper - polski): {scene_key}...")
        
        # Piper TTS with Polish language support
        try:
            piper_tts.generate_piper_tts(text, audio_file)
        except RuntimeError as e:
            raise RuntimeError(f"Piper TTS failed for scene '{scene_key}': {e}")
        
        duration = vp.get_audio_duration(audio_file)
        audio_files[scene_key] = {"path": audio_file, "duration": duration, "text": text}
        logger.info(f"✅ TTS {scene_key} wygenerowany: {audio_file}")

    return audio_files'''

content = re.sub(old_pattern, new_func, content, flags=re.DOTALL)

with open('server.py', 'w') as f:
    f.write(content)

print("✅ Fixed generate_tts_audio_narration function")

