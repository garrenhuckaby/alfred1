"""
tts.py – Text-to-speech via Kokoro.
Call speak(text) from anywhere in the project.
"""

import sounddevice as sd
import numpy as np


def speak(text: str):
    """Synthesise text with Kokoro and play through the default output device."""
    try:
        from kokoro import KPipeline
        pipeline = KPipeline(lang_code="a")  # 'a' = American English
        audio_chunks = []
        for _, _, audio in pipeline(text, voice="af_heart", speed=1.0, split_pattern=r"\n+"):
            audio_chunks.append(audio)
        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            sd.play(full_audio, samplerate=24000)
            sd.wait()
    except ImportError:
        print("[TTS] Kokoro not installed – printing instead.")
        print(f"[TTS] {text}")
    except Exception as e:
        print(f"[TTS] Error: {e}")
        print(f"[TTS] {text}")