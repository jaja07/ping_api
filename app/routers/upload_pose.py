import shutil
import os
from fastapi import APIRouter, File, UploadFile, Body, HTTPException
from models_ml.test_mediapipe import MpPose
from utils.dependencies import patientid, consultationid
from services.consultation_service import ConsultationService
from services.bilan_service import generate_pdf
from datetime import datetime
from models.consultation import (
    ConsultationModel,
    UpdateConsultationModel
)

router = APIRouter()
consultationService = ConsultationService()

def save_file(uploaded_file: UploadFile, destination: str):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

def predict_pose(file_path: str, output_path: str, genou: int):
    mp = MpPose(file_path, output_path)
    return mp.predict(genou=genou)

def clean_up(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)

async def create_consultation(angles: dict, patient_id: str):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    consultation_data = {
        "patientid": patient_id,
        "date_consultation": current_date,
        "flexion": {"active": 0.0, "passive": angles["Flexion"]},
        "extension": {"active": 0.0, "passive": angles["Extension"]},
        "bdk": f"{patient_id}_bdk_{current_date}.pdf"
    }
    try:
        consulationid = await consultationService.create(consultation_data)
        return consulationid
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de la consultation: {str(e)}")
    
  
@router.post("/{genou}/{patient_id}", response_description="Upload a file")
async def create_upload_file(
    file: UploadFile = File(...),
    genou: int = 0,
    patient_id: str = None
):  
    base_dir = os.path.abspath('app/uploads')

    # Nettoyer le nom du fichier pour éviter les attaques
    filename = os.path.basename(file.filename)
    file_location = os.path.join(base_dir, filename)
    file_output = os.path.join(base_dir, "output.txt")

    # Créer le répertoire s'il n'existe pas
    os.makedirs(base_dir, exist_ok=True)
    
    # Sauvegarder le fichier
    save_file(file, file_location)
    
    try:
        # Prédiction de la pose
        angles = predict_pose(file_location, file_output, genou)
    
    except Exception as e:
        # Supprimer le fichier en cas d'erreur
        clean_up(file_location)
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement du fichier: {str(e)}")
    
    finally:
        # Suppression du fichier après traitement
        clean_up(file_location)

    """     # Création de la consultation
    await create_consultation(angles, patient_id)

    # Générer le PDF
    pdf_path = generate_pdf(angles, patient_id) """

    return {"filename": file.filename, "saved_at": file_location, 'angles': angles}
