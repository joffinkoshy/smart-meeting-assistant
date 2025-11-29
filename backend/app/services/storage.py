# backend/app/services/storage.py
from pathlib import Path
import time
import uuid
import shutil
from typing import Dict

# Directory where uploads will be stored (ensure this is writable)
UPLOAD_DIR = Path("/tmp/sma_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def _make_unique_filename(original_name: str) -> str:
    """
    Create a unique filename preserving extension.
    Format: <timestamp>_<uuid4><ext>
    """
    ext = Path(original_name).suffix or ".bin"
    unique = f"{int(time.time())}_{uuid.uuid4().hex}{ext}"
    return unique


def save_upload(file_bytes: bytes, original_filename: str) -> Dict[str, str]:
    """
    Save uploaded bytes to disk with a unique name.

    Returns a dict:
      {
        "file_id": "<uuid>",
        "path": "/tmp/sma_uploads/....",
        "original_filename": "some.wav"
      }
    """
    file_id = uuid.uuid4().hex
    filename = _make_unique_filename(original_filename)
    target = UPLOAD_DIR / filename

    # write bytes
    with open(target, "wb") as fh:
        fh.write(file_bytes)

    # create a small metadata file alongside (optional)
    meta = {
        "file_id": file_id,
        "path": str(target),
        "original_filename": original_filename,
    }
    return meta


def delete_file(path: str) -> bool:
    """
    Delete saved file (safer cleanup).
    Returns True if deleted or False otherwise.
    """
    try:
        p = Path(path)
        if p.exists() and p.is_file():
            p.unlink()
            return True
        return False
    except Exception:
        return False


def move_file(src: str, dst_dir: str) -> str:
    """
    Move a saved file to another directory (returns new path).
    Useful to archive processed audio.
    """
    src_p = Path(src)
    dst_p = Path(dst_dir)
    dst_p.mkdir(parents=True, exist_ok=True)
    new_path = dst_p / src_p.name
    shutil.move(str(src_p), str(new_path))
    return str(new_path)
