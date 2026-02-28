"""
main.py – Entry point. Wires together all modules and starts the keyboard listener.

Project layout:
    main.py
    tts.py              – Kokoro text-to-speech
    greeting.py         – Qwen greeting generation
    assistant.py        – Wake-key ('i') activation flow
    audio_recording.py  – Microphone capture + Whisper transcription
    router.py           – Routes transcript lines to actions
"""

import sounddevice as sd
from pynput import keyboard

import audio_recording
import assistant

# ── Shared state ───────────────────────────────────────────────────────────────
state = {"assistant_active": False}

get_active  = lambda: state["assistant_active"]
set_active  = lambda v: state.__setitem__("assistant_active", v)

# Wire the active-flag accessor into audio_recording
audio_recording.init(get_active)


# ── Keyboard handlers ──────────────────────────────────────────────────────────

def on_press(key):
    try:
        if key.char == 'r':
            audio_recording.start_recording()
        elif key.char == 'i':
            assistant.activate(get_active, set_active)
    except AttributeError:
        pass


def on_release(key):
    try:
        if key.char == 'r':
            audio_recording.stop_recording()
    except AttributeError:
        if key == keyboard.Key.esc:
            return False  # stop listener


# ── Run ────────────────────────────────────────────────────────────────────────

print("Ready.")
print("  Press 'i'   → wake assistant (generates greeting, then listens)")
print("  Hold 'R'    → speak a command (release to transcribe)")
print("  Press 'Esc' → exit")

with sd.InputStream(
    samplerate=audio_recording.FS,
    channels=audio_recording.CHANNELS,
    callback=audio_recording.callback,
):
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()