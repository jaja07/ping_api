from fastapi import APIRouter, HTTPException, Body, status
from fastapi.responses import Response, FileResponse
from services.consultation_service import ConsultationService
from services.bilan_service import generate_pdf
from datetime import datetime
from models.consultation import (
    ConsultationModel,
    UpdateConsultationModel
)

router = APIRouter()
consultationService = ConsultationService()

# Download bdk file
@router.get("/download/{id}", response_description="Download the BDK file")
async def download_bdk(id: str):
    """
    Download the BDK file.

    Args: id (str): The consultation id.
    """
    consultation = await consultationService.read_one(id)
    if consultation is not None:
        bdk_path = "/code/app/bdk/" + consultation["bdk"]
        return FileResponse(bdk_path, media_type="application/pdf", filename=consultation['bdk'])
    else:
        raise HTTPException(status_code=404, detail="BDK file not found")

async def update_bdk_path(patient_id: str, consultation_id: str):
    current_date = datetime.now().strftime("%Y-%m-%d")
    consultation_data = {
        "bdk": f"{consultation_id}_bdk_{current_date}.pdf"
    }
    try:
        update_result = await consultationService.update(consultation_id, consultation_data)
        return update_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour de la consultation: {str(e)}")
    
#Create route
@router.post("/", response_description="New consultation added", response_model=ConsultationModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_consulation(consulation: ConsultationModel = Body(...)):  #La requête doit contenir un corps JSON qui sera validé et converti en une instance du modèle ConsultationModel. Body(...) : Indique que cette donnée est obligatoire (le ... signifie "valeur requise").
    """
    Insert a new consulation record.
    Update the bdk path in the consultation record.
    Generate the PDF.
    """
    consultation_data = consulation.model_dump(by_alias=True, exclude=["id"])  #Convertit l'instance du modèle en un dictionnaire Python. by_alias=True : Utilise les alias définis dans ConsultationModel (s'il y en a) pour les clés du dictionnaire.
    try:
        consultationid = await consultationService.create(consultation_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de la consultation: {str(e)}")
    
    if consultationid is not None:
        created_consultation = await consultationService.read_one(consultationid)
        # Mettre à jour le chemin du fichier BDK dans la consultation
        await update_bdk_path(created_consultation["patientid"], consultationid)
        # Générer le PDF
        await generate_pdf(created_consultation["patientid"], consultationid)
    else:
        raise HTTPException(status_code=500, detail="Consulation could not be created")

    return created_consultation

# Read route
@router.get("/{id}", response_description="Get a single consulation", response_model=ConsultationModel, response_model_by_alias=False)
async def read_consulation(id: str):
    """
    Retrieve a consulation record.
    """
    read_consultation = await consultationService.read_one(id)
    if read_consultation:
        return read_consultation
    else:
        raise HTTPException(status_code=404, detail="consultation not found")   

# Update route
@router.put("/{id}", response_description="consulation data updated", response_model=ConsultationModel)
async def update_consulation(id: str, consultation: UpdateConsultationModel = Body(...)):
    """
    Update individual fields of an existing consulation record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    consultation = {
        k: v for k, v in consultation.model_dump(by_alias=True).items() if v is not None
    }
    if len(consultation) >= 1:
        update_result = await consultationService.update(id, consultation)
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"consulation {id} not found")
    else: 
        if (existing_consulation := consultationService.read_one(id)) is not None:
            return existing_consulation 
        else:
            raise HTTPException(status_code=404, detail=f"consulation {id} not found")
        
# Route pour supprimer un document
@router.delete("/{id}", response_description="consulation data deleted")
async def delete_document(id: str):
    """
    Remove a single consulation record from the database.
    """
    delete_result = await consultationService.delete(id)
    if delete_result == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"consulation {id} not found")