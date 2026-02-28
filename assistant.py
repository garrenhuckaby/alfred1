"""
assistant.py – Wake-key activation flow.
Call activate(get_active_fn, set_active_fn) when the 'i' key is pressed.
"""

from greeting import generate_greeting
from tts import speak


def activate(get_active_fn, set_active_fn):
    """
    Generates and speaks the butler greeting, then marks the assistant as active
    so that the next recording is routed through the transcript handler.

    Args:
        get_active_fn: callable returning current assistant_active bool
        set_active_fn: callable(bool) to update assistant_active
    """
    if get_active_fn():
        return  # already active, prevent re-entrancy

    set_active_fn(True)
    print("\n[Assistant] Wake key pressed – generating greeting…")

    greeting = generate_greeting()
    print(f"[Assistant] Greeting: {greeting}")
    speak(greeting)

    print("[Assistant] Now listening for your response. Hold 'R' to speak.")