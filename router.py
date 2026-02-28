"""
router.py – Routes the last transcribed line to the appropriate action.
Call handle_last_transcript_line(line) after transcription completes.
"""

from tts import speak


def handle_last_transcript_line(line: str):
    """
    Decide what to do based on the last transcribed line.
    Extend the keyword lists to suit your workflow.
    """
    line_lower = line.lower()
    print(f"[Router] Last transcript: '{line}'")

    # ── Email ──────────────────────────────────────────────────────────────
    if any(w in line_lower for w in ["email", "inbox", "messages", "mail"]):
        print("[Action] Opening email client…")
        speak("Opening your email now.")
        # import os; os.system("xdg-open https://mail.google.com")

    # ── Calendar / schedule ───────────────────────────────────────────────
    elif any(w in line_lower for w in ["calendar", "schedule", "appointments", "meetings"]):
        print("[Action] Opening calendar…")
        speak("Pulling up your calendar.")
        # import os; os.system("xdg-open https://calendar.google.com")

    # ── News / headlines ──────────────────────────────────────────────────
    elif any(w in line_lower for w in ["news", "headlines", "weather"]):
        print("[Action] Fetching news or weather…")
        speak("Let me get the latest headlines for you.")

    # ── Music / playback ──────────────────────────────────────────────────
    elif any(w in line_lower for w in ["music", "play", "song", "playlist"]):
        print("[Action] Starting music playback…")
        speak("Starting music now.")

    # ── Reminders / notes ─────────────────────────────────────────────────
    elif any(w in line_lower for w in ["reminder", "remind", "note", "todo", "task", "remember"]):
        print("[Action] Adding a reminder…")
        speak("I'll make a note of that.")

    # ── Affirmative / yes ─────────────────────────────────────────────────
    elif any(w in line_lower for w in ["yes", "sure", "please", "okay", "ok", "yep", "yeah", "fine", "do it", "go ahead"]):
        print("[Action] Affirmative response detected – continuing default workflow.")
        speak("Very well.")

    # ── Negative / no ─────────────────────────────────────────────────────
    elif any(w in line_lower for w in ["no", "nope", "never mind", "cancel", "stop", "nah", "not now", "later", "don't"]):
        print("[Action] Negative response – standing by.")
        speak("Understood. Just let me know if you need anything, Sir.")

    # ── Fallback ──────────────────────────────────────────────────────────
    else:
        print("[Action] No matching action found. Echoing back.")
        speak(f"You said: {line}. I'm not sure what to do with that yet.")