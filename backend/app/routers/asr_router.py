import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.asr import transcribe_file

router = APIRouter()

UPLOAD_DIR = "/tmp/sma_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/transcribe_and_analyze")
async def transcribe_and_analyze(file: UploadFile = File(...)):
    try:
        file_id = uuid.uuid4().hex
        ext = os.path.splitext(file.filename)[1]
        saved_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")

        with open(saved_path, "wb") as f:
            f.write(await file.read())

        result = transcribe_file(saved_path)

        return {
            "file_id": file_id,
            "saved_path": saved_path,
            "transcript": result["text"],
            "segments": result["segments"],
            "error": result.get("error")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # new update
