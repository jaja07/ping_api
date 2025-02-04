# service.py
import torch
import torchaudio
import librosa
import soundfile as sf
from models.transcription import TranscriptionModel
from tempfile import NamedTemporaryFile
from fastapi import HTTPException
import os

class SpeechToTextService:
    def __init__(self):
        self.model = TranscriptionModel()

    def load_audio(self, file_path: str):
        audio, sampling_rate = torchaudio.load(file_path)
        # Convert to mono channel if not already
        if audio.shape[0] > 1:
            audio = torch.mean(audio, dim=0, keepdim=True)
        # Resample to 16kHz if needed
        if sampling_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sampling_rate, new_freq=16000)
            audio = resampler(audio)
        return audio.squeeze().numpy(), 16000

    async def process_audio(self, file):
        processed_path = None  # Définition avant utilisation pour éviter l'erreur
        try:
            # Créer un fichier temporaire sécurisé pour stocker l'audio téléchargé
            with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(await file.read())

            # Detect file format and load accordingly
            if file.filename.endswith('.wav'):
                audio_array, sampling_rate = self.load_audio(temp_file_path)
                processed_path = temp_file_path + "_processed.wav"
                sf.write(processed_path, audio_array, sampling_rate)
            elif file.filename.endswith('.mp3'):
                audio_array, sampling_rate = librosa.load(temp_file_path, sr=16000)
                processed_path = temp_file_path + "_processed.wav"
                sf.write(processed_path, audio_array, sampling_rate)
            
            # Transcrire l'audio
            result = self.model.transcribe(temp_file_path)

            # Nettoyage des fichiers temporaires
            os.remove(temp_file_path)
            if processed_path:
                os.remove(processed_path)

            return {"transcription": result["text"]}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing audio file: {str(e)}")