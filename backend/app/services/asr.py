# backend/app/services/asr.py

import whisper
import torch
import logging
from functools import lru_cache
from typing import Dict, Any
from ..services.summarize import analyze_transcript

logger = logging.getLogger(__name__)

# -----------------------------
# DEVICE SELECTION (CPU / MPS)
# -----------------------------
def get_device():
    """
    Automatically pick the best available device:
    - MPS (Apple Silicon)
    - CUDA (NVIDIA)
    - CPU (fallback)
    """
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


# -----------------------------
# LOAD MODEL ONLY ONCE
# -----------------------------
@lru_cache(maxsize=1)
def get_model():
    """
    Loads Whisper Small model once.
    Cached using lru_cache so it stays in memory.
    """
    device = "cpu"  # Force CPU due to MPS compatibility issues
    logger.info(f"Loading Whisper Small on device: {device}")
    model = whisper.load_model("small", device=device)
    return model


# -----------------------------
# TRANSCRIPTION FUNCTION
# -----------------------------

def transcribe_file(path: str) -> Dict[str, Any]:
    model = get_model()
    logger.info(f"Transcribing file: {path}")

    try:
        result = model.transcribe(path, verbose=False)
    except Exception as e:
        logger.error(f"Error transcribing: {e}")
        return {
            "text": "",
            "segments": [],
            "intelligence": None,
            "error": str(e)
        }

    transcript_text = result.get("text", "")

    # Call the summarizer (LLM) - consider async later for speed.
    try:
        intelligence = analyze_transcript(transcript_text)
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        intelligence = {"error": str(e)}

    return {
        "text": transcript_text,
        "segments": result.get("segments", []),
        "intelligence": intelligence,
    }
