import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.asr import transcribe_file

router = APIRouter()

UPLOAD_DIR = "/tmp/sma_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# File validation constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.mp4', '.avi', '.mov', '.webm'}
ALLOWED_MIME_TYPES = {
    'audio/mpeg', 'audio/wav', 'audio/x-wav', 'audio/mp4', 'audio/flac', 
    'audio/ogg', 'video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/webm'
}

@router.post("/transcribe_and_analyze")
async def transcribe_and_analyze(file: UploadFile = File(...)):
    saved_path = None
    try:
        # Validate file extension
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Validate MIME type
        if file.content_type and file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid content type: {file.content_type}"
            )
        
        # Read file and validate size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Save file
        file_id = uuid.uuid4().hex
        saved_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
        
        with open(saved_path, "wb") as f:
            f.write(file_content)
        
        # Transcribe
        result = transcribe_file(saved_path)
        
        # Clean up file after processing
        try:
            if saved_path and os.path.exists(saved_path):
                os.remove(saved_path)
        except Exception as cleanup_error:
            print(f"Warning: Failed to clean up file {saved_path}: {cleanup_error}")
        
        return {
            "file_id": file_id,
            "transcript": result["text"],
            "segments": result["segments"],
            "error": result.get("error")
        }

    except HTTPException:
        # Clean up on validation errors
        if saved_path and os.path.exists(saved_path):
            try:
                os.remove(saved_path)
            except Exception:
                pass
        raise
    except Exception as e:
        # Clean up on unexpected errors
        if saved_path and os.path.exists(saved_path):
            try:
                os.remove(saved_path)
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=str(e))
