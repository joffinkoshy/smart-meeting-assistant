# backend/app/services/summarizer.py
import os
import openai
from typing import Dict, List

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    # allow app to run but raise at call-time with helpful error
    openai.api_key = None
else:
    openai.api_key = API_KEY

# Simple helper to call OpenAI chat completion
def call_llm_system(prompt: str, model: str = "gpt-4o-mini") -> str:
    if not openai.api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment.")
    client = openai.OpenAI(api_key=openai.api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system", "content": "You are an assistant that extracts concise meeting summaries, key points, and action items from transcripts."},
            {"role":"user", "content": prompt}
        ],
        max_tokens=700,
        temperature=0.0,
    )
    return resp.choices[0].message.content.strip()

def make_prompt(transcript_text: str) -> str:
    # Prompt asks the model for three structured outputs.
    return f"""
Transcript:
{transcript_text}

Please produce a JSON object with three keys: "summary", "key_points", and "action_items".

- "summary": A 1-2 sentence concise summary of the meeting.
- "key_points": A JSON array containing up to 8 short bullet points (strings) of the most important takeaways.
- "action_items": A JSON array of objects; each object must have:
    - "task": short description
    - "owner": who was assigned (or "unassigned")
    - "due": due date if mentioned, otherwise empty string

Important: Output ONLY valid JSON (no explanation). Keep responses concise.
"""

def analyze_transcript(transcript_text: str, model: str = "gpt-4o-mini") -> Dict:
    prompt = make_prompt(transcript_text)
    text = call_llm_system(prompt, model=model)
    # The LLM is instructed to return JSON; parse it.
    import json
    try:
        return json.loads(text)
    except Exception as e:
        # If parsing fails, return fallback with the raw LLM text
        return {
            "error": "LLM returned non-JSON or unparsable output",
            "raw": text
        }
