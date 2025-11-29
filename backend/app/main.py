from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.asr_router import router as asr_router

app = FastAPI(title="Smart Meeting Assistant - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(asr_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "ok", "service": "smart-meeting-assistant"}
