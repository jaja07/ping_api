from fastapi import APIRouter, HTTPException, Depends, Body, status
from fastapi.responses import Response
from bson.objectid import ObjectId
from services.kine_service import KineService
from fastapi.encoders import jsonable_encoder
from models.kine import (
    KineModel,
    UpdateKineModel
)

router = APIRouter()
kineService = KineService()

#Create route
@router.post("/", response_description="New kine added", response_model=KineModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False, tags=["Kiné"])
async def add_kine(kine: KineModel = Body(...)):  #La requête doit contenir un corps JSON qui sera validé et converti en une instance du modèle KineModel. Body(...) : Indique que cette donnée est obligatoire (le ... signifie "valeur requise").
    """
    Insert a new kine record.
    """
    kine_data = kine.model_dump(by_alias=True, exclude=["id"])  #Convertit l'instance du modèle en un dictionnaire Python. by_alias=True : Utilise les alias définis dans StudentModel (s'il y en a) pour les clés du dictionnaire.
    kineid = await kineService.create(kine_data)
    if kineid is None:
        raise HTTPException(status_code=500, detail="Project could not be created")
    else:
        created_kine = await kineService.read_one(kineid)
    return created_kine

# Read route
@router.get("/{id}", response_description="Get a single kine", response_model=KineModel, response_model_by_alias=False, tags=["Kiné"])
async def read_kine(id: str):
    """
    Retrieve a kine record.
    """
    read_kine = await kineService.read_one(id)
    if read_kine:
        return read_kine
    else:
        raise HTTPException(status_code=404, detail="Kine not found")   


# Update route
@router.put("/{id}", response_description="Kine data updated", response_model=KineModel)
async def update_kine(id: str, kine: UpdateKineModel = Body(...)):
    """
    Update individual fields of an existing kine record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    kine = {
        k: v for k, v in kine.model_dump(by_alias=True).items() if v is not None
    }
    if len(kine) >= 1:
        update_result = kineService.update(id, kine)
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")
    else: 
        if (existing_kine := kineService.read_one(id)) is not None:
            return existing_kine 
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")
        
# Route pour supprimer un document
@router.delete("/{id}", response_description="Kine data deleted")
async def delete_document(id: str):
    """
    Remove a single kine record from the database.
    """
    delete_result = kineService.delete(id)
    if delete_result == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Student {id} not found")