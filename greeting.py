"""
greeting.py – Generates a butler-style greeting via Qwen.
Call generate_greeting() to get a greeting string.
"""

import datetime


def generate_greeting() -> str:
    """Ask Qwen to craft a personalised butler-style greeting."""
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch

        model_id = "Qwen/Qwen2.5-1.5B-Instruct"  # swap for larger model as needed
        print("[Qwen] Loading model for greeting (first run may download weights)…")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        qwen = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32)

        hour = datetime.datetime.now().hour
        if hour < 12:
            time_of_day = "morning"
        elif hour < 17:
            time_of_day = "afternoon"
        else:
            time_of_day = "evening"

        prompt = (
            f"You are a wise, softspoken British AI butler assistant. You understand your employer well, "
            f"and view him as a family member, not just an employer. "
            f"Generate a single short, warm greeting for your master for this {time_of_day}. "
            f"You know he has unread emails and you want to remind him specifically about the emails. "
            f"He is prone to forget them, so you are firm, but polite. "
            f"Example style: 'Good morning, Master Bruce. Would you like to run through your unread emails?' "
            f"Keep it under 30 words. Output only the greeting, nothing else."
        )

        messages = [{"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text], return_tensors="pt")
        with torch.no_grad():
            output = qwen.generate(**inputs, max_new_tokens=60, do_sample=True, temperature=0.7)
        greeting = tokenizer.decode(
            output[0][inputs.input_ids.shape[-1]:], skip_special_tokens=True
        ).strip()
        return greeting

    except ImportError:
        print("[Qwen] transformers not installed – using fallback greeting.")
    except Exception as e:
        print(f"[Qwen] Error: {e}")

    # Fallback
    hour = datetime.datetime.now().hour
    tod = "morning" if hour < 12 else ("afternoon" if hour < 17 else "evening")
    return f"Good {tod}, Master Bruce. Would you like to review your unread emails while you have a moment?"