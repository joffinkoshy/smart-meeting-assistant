# backend/app/services/asr.py

import whisper
import torch
from functools import lru_cache
from typing import Dict, Any

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
    device = get_device()
    print(f"[ASR] Loading Whisper Small on device: {device}")
    model = whisper.load_model("small", device="cpu")
    return model


# -----------------------------
# TRANSCRIPTION FUNCTION
# -----------------------------
def transcribe_file(path: str) -> Dict[str, Any]:
    """
    Transcribes an audio file using Whisper Small.
    Returns:
    {
        "text": "...",
        "segments": [...]
    }
    """
    model = get_model()
    print(f"[ASR] Transcribing file: {path}")

    try:
        result = model.transcribe(path, verbose=False)
    except Exception as e:
        print(f"[ASR] Error transcribing: {e}")
        return {
            "text": "",
            "segments": [],
            "error": str(e)
        }

    return {
        "text": result.get("text", ""),
        "segments": result.get("segments", []),
    }
