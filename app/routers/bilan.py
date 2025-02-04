from fastapi import APIRouter, HTTPException
from models.bilan import BilanKineData
from services.bilan_service import generate_pdf
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/generate-pdf")
async def create_pdf(data: BilanKineData):
    try:
        # Convertir les données Pydantic en dictionnaire
        data_dict = data.dict()
        # Générer le PDF
        pdf_path = generate_pdf(data_dict)
        
        # Retourner le fichier PDF en réponse
        return FileResponse(pdf_path, media_type="application/pdf", filename="bilan_kine.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
