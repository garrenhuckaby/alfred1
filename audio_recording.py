"""
audio_recording.py – Handles microphone recording and Whisper transcription.
Exposes: callback(), start_recording(), stop_recording()
Depends on: router.py, and a shared `assistant_active` flag passed in from main.
"""

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# ── Whisper setup ──────────────────────────────────────────────────────────────
FS = 16000
CHANNELS = 1
MODEL_SIZE = "base"

print(f"Loading Whisper model ({MODEL_SIZE})...")
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")

# ── Module-level state ─────────────────────────────────────────────────────────
recording_data = []
is_recording = False

# Set by main.py so the router is only called when the assistant is active
_get_assistant_active = lambda: False  # replaced at init


def init(get_active_fn):
    """
    Call this once from main.py, passing a callable that returns the current
    assistant_active boolean.  e.g. init(lambda: state['assistant_active'])
    """
    global _get_assistant_active
    _get_assistant_active = get_active_fn


def callback(indata, frames, time, status):
    """sounddevice InputStream callback – appends audio while recording."""
    if status:
        print(status)
    if is_recording:
        recording_data.append(indata.copy())


def start_recording():
    global is_recording, recording_data
    if not is_recording:
        print("\n● RECORDING… (Release 'R' to transcribe)")
        recording_data = []
        is_recording = True


def stop_recording():
    global is_recording
    if is_recording:
        is_recording = False
        print("○ Processing…")
        if recording_data:
            audio_array = np.concatenate(recording_data, axis=0).ravel().astype(np.float32)
            segments, info = model.transcribe(audio_array, beam_size=5, vad_filter=True)

            last_line = ""
            with open("transcription_log.txt", "a", encoding="utf-8") as f:
                for segment in segments:
                    text = segment.text.strip()
                    print(f" >> {text}")
                    f.write(text + "\n")
                    last_line = text

            print(f"Detected language: {info.language} ({info.language_probability:.2f})")

            if _get_assistant_active() and last_line:
                from router import handle_last_transcript_line
                handle_last_transcript_line(last_line)
        else:
            print("No audio captured.")