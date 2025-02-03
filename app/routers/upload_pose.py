import shutil
import os
from fastapi import APIRouter, File, UploadFile
from pose_estimation.test_mediapipe import MpPose
from pose_estimation.test_yolo import YoloPose
router = APIRouter()

# Chemin absolu pour le répertoire de téléchargement
#UPLOAD_DIR = "C:/Users/jarfi/Bureau/PING/PING-35/api/app/uploads"
@router.post("/{genou}", response_description="Upload a file")
async def create_upload_file(file: UploadFile = File(...), genou: int = 0):
    base_dir = os.path.abspath('app/uploads')
    # Nettoyer le nom du fichier pour éviter les attaques
    filename = os.path.basename(file.filename)
    file_location = os.path.join(base_dir, filename)
    file_output = os.path.join(base_dir, "output.txt")
    # Créer le répertoire s'il n'existe pas
    os.makedirs(base_dir, exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Prédiction de la pose
        mp = MpPose(file_location, file_output)
        angles = mp.predict(genou=genou)
        #yolo = YoloPose(file_location, file_output)
        #yolo.predict()
        # Suppression du fichier après traitement
        os.remove(file_location) 
        return {"filename": file.filename, "saved_at": file_location, 'angles': angles}
    
    except Exception as e:
        # Supprimer le fichier en cas d'erreur
        if os.path.exists(file_location):
            os.remove(file_location)  
        return {"error": str(e)}
    
    
