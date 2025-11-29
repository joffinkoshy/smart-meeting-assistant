# backend/app/routers/asr_router.py  (or similar)
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from ..services.asr import transcribe_file  # your existing function

router = APIRouter()

ALLOWED_CONTENT_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/mpeg",
    "audio/mp3",
    "audio/x-mp3",
    "audio/ogg",
    "audio/webm",
    "application/octet-stream",
}

@router.post("/api/transcribe_and_analyze")
async def transcribe_and_analyze(file: UploadFile = File(...)):
    # Defensive: check content type but allow generic octet-stream
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid content type: {content_type}")

    # Save to a temp file (synchronous save is fine for small files)
    import tempfile, shutil, os
    suffix = ".wav" if "wav" in content_type else ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp_path = tmp.name
        # UploadFile.file is a SpooledTemporaryFile (file-like) — copy it
        shutil.copyfileobj(file.file, tmp)

    try:
        result = transcribe_file(tmp_path)
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

    return JSONResponse(result)
