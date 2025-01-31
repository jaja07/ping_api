# router.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from services.transcription_service import SpeechToTextService

router = APIRouter()
service = SpeechToTextService()


@router.post("/speech-to-text/")
async def speech_to_text(file: UploadFile = File(...)):
    return await service.process_audio(file)