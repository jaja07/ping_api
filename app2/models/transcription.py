# transcription.py
import whisper

class TranscriptionModel:
    def __init__(self):
        self.model = whisper.load_model("turbo")

    def transcribe(self, audio_path: str):
        return self.model.transcribe(audio_path, fp16=False)