from fastapi import APIRouter, HTTPException, Depends, Body, status
from fastapi.responses import Response
from bson.objectid import ObjectId
from services.consultation_service import ConsultationService
from fastapi.encoders import jsonable_encoder
from models.consultation import (
    ConsultationModel,
    UpdateConsultationModel
)

router = APIRouter()
consultationService = ConsultationService()

#Create route
@router.post("/", response_description="New consultation added", response_model=ConsultationModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_consulation(consulation: ConsultationModel = Body(...)):  #La requête doit contenir un corps JSON qui sera validé et converti en une instance du modèle ConsultationModel. Body(...) : Indique que cette donnée est obligatoire (le ... signifie "valeur requise").
    """
    Insert a new consulation record.
    """
    consulation_data = consulation.model_dump(by_alias=True, exclude=["id"])  #Convertit l'instance du modèle en un dictionnaire Python. by_alias=True : Utilise les alias définis dans ConsultationModel (s'il y en a) pour les clés du dictionnaire.
    consulationid = await consultationService.create(consulation_data)
    if consulationid is None:
        raise HTTPException(status_code=500, detail="Consulation could not be created")
    else:
        created_consulation = await consultationService.read_one(consulationid)
    return created_consulation

# Read route
@router.get("/{id}", response_description="Get a single consulation", response_model=ConsultationModel, response_model_by_alias=False)
async def read_consulation(id: str):
    """
    Retrieve a consulation record.
    """
    read_consulation = await consultationService.read_one(id)
    if read_consulation:
        return read_consulation
    else:
        raise HTTPException(status_code=404, detail="consulation not found")   

# Update route
@router.put("/{id}", response_description="consulation data updated", response_model=ConsultationModel)
async def update_consulation(id: str, consulation: UpdateConsultationModel = Body(...)):
    """
    Update individual fields of an existing consulation record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    consulation = {
        k: v for k, v in consulation.model_dump(by_alias=True).items() if v is not None
    }
    if len(consulation) >= 1:
        update_result = await consultationService.update(id, consulation)
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