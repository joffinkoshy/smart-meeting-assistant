# Smart Meeting Assistant (MVP)

A web application for transcribing meeting audio/video files using OpenAI's Whisper model.

## Features

- Audio/Video transcription using Whisper (small model)
- Support for multiple formats: MP3, WAV, M4A, FLAC, OGG, MP4, AVI, MOV, WebM
- File validation and size limits (100MB max)
- Automatic file cleanup after processing
- React-based frontend with error handling
- FastAPI backend with CORS support

## Prerequisites

### System Requirements
- Python 3.11+
- Node.js 20+
- ffmpeg (required by Whisper)

### macOS Installation
```bash
brew install ffmpeg
```

### Linux Installation
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

## Quick Start (Development)

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The backend will be available at http://localhost:8000

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000

## Docker Setup

### Using Docker Compose (Recommended)
```bash
# Build and run both services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Individual Docker Builds

**Backend:**
```bash
cd backend
docker build -t sma-backend .
docker run -p 8000:8000 sma-backend
```

**Frontend:**
```bash
cd frontend
docker build -t sma-frontend .
docker run -p 3000:3000 sma-frontend
```

## Project Structure

```
smart-meeting-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── routers/
│   │   │   └── asr_router.py    # Transcription API endpoints
│   │   └── services/
│   │       ├── asr.py           # Whisper transcription service
│   │       ├── embeddings.py    # Embeddings service (unused)
│   │       ├── storage.py       # File storage utilities
│   │       └── summarize.py     # Summarization service (unused)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example            # Environment configuration template
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── index.jsx           # React entry point
│   │   └── index.css           # Styles
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## API Endpoints

### POST /api/transcribe_and_analyze
Transcribes an audio/video file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (audio/video file)

**Response:**
```json
{
  "file_id": "abc123...",
  "transcript": "The transcribed text...",
  "segments": [...],
  "error": null
}
```

**Error Codes:**
- 400: Invalid file type, file too large, or empty file
- 500: Server error during transcription

### GET /
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "smart-meeting-assistant"
}
```

## Configuration

### Backend Environment Variables

Create a `.env` file in the backend directory (see `.env.example`):

```env
PORT=8000
HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000
UPLOAD_DIR=/tmp/sma_uploads
MAX_FILE_SIZE_MB=100
WHISPER_MODEL=small
DEVICE=auto
ENV=development
```

## File Validation

### Allowed File Types
- Audio: MP3, WAV, M4A, FLAC, OGG
- Video: MP4, AVI, MOV, WebM

### File Size Limits
- Maximum file size: 100MB
- Empty files are rejected

### Security Features
- File extension validation
- MIME type validation
- File size validation
- Automatic cleanup after processing
- Unique file naming to prevent conflicts

## Troubleshooting

### Backend Issues

**Problem:** ModuleNotFoundError or import errors
**Solution:** Ensure you're in the virtual environment and dependencies are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Problem:** ffmpeg not found
**Solution:** Install ffmpeg using your system's package manager

**Problem:** Whisper model download fails
**Solution:** Ensure you have a stable internet connection. The model will download on first use.

**Problem:** Out of memory errors
**Solution:** The small model requires ~2GB RAM. Close other applications or use a machine with more RAM.

### Frontend Issues

**Problem:** Cannot connect to backend
**Solution:** Ensure backend is running on port 8000 and CORS is properly configured

**Problem:** npm install fails
**Solution:** Clear npm cache and try again:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

**Problem:** Docker build fails on COPY commands
**Solution:** Ensure you're running `docker-compose up` from the project root directory

**Problem:** Port already in use
**Solution:** Change ports in docker-compose.yml or stop conflicting services

## Performance Notes

- First transcription will be slower as it downloads the Whisper model (~1.5GB)
- Transcription time varies based on audio length and system performance
- GPU acceleration is supported (CUDA/MPS) if available
- CPU-only mode works but is slower

## Known Limitations

- Maximum file size: 100MB
- Only supports Whisper small model currently
- No persistent storage of transcriptions
- No user authentication
- Embeddings and summarization services are not yet integrated

## Development

### Running Tests
```bash
# Backend tests (when implemented)
cd backend
pytest

# Frontend tests (when implemented)
cd frontend
npm test
```

### Code Quality
- Backend uses FastAPI with type hints
- Frontend uses React with hooks
- File validation and error handling implemented
- Automatic cleanup of uploaded files

## Future Enhancements

- [ ] Integrate embeddings service for semantic search
- [ ] Integrate summarization service
- [ ] Add user authentication
- [ ] Persistent storage with database
- [ ] Support for larger Whisper models
- [ ] Real-time transcription
- [ ] Export transcriptions to various formats
- [ ] Multi-language support configuration

## License

[Your License Here]

## Contributors

[Your Name/Team]

## Support

For issues and questions, please open an issue on the GitHub repository.
