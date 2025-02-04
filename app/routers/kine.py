from fastapi import APIRouter, HTTPException, Depends, Body, status, Query
from fastapi.responses import Response
from bson.objectid import ObjectId
from services.kine_service import KineService
from fastapi.encoders import jsonable_encoder
from models.kine import (
    KineModel,
    UpdateKineModel
)
from models.patient import (
    PatientCollection
)
from passlib.hash import bcrypt



router = APIRouter()
kineService = KineService()

#Create route
@router.post("/", response_description="New kine added", response_model=KineModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_kine(kine: KineModel = Body(...)):  #La requête doit contenir un corps JSON qui sera validé et converti en une instance du modèle KineModel. Body(...) : Indique que cette donnée est obligatoire (le ... signifie "valeur requise").
    """
    Insert a new kine record.
    """
    kine_data = kine.model_dump(by_alias=True, exclude=["id"])  #Convertit l'instance du modèle en un dictionnaire Python. by_alias=True : Utilise les alias définis dans KineModel (s'il y en a) pour les clés du dictionnaire.

    # Hacher le mot de passe avant de l'envoyer au service
    #kine_data['mdp'] = hash.bcrypt(kine_data['mdp'])
    kine_data['mdp'] = bcrypt.hash(kine_data['mdp'])
    kineid = await kineService.create(kine_data)
    if kineid is None:
        raise HTTPException(status_code=500, detail="Kine could not be created")
    else:
        created_kine = await kineService.read_one(kineid)
    return created_kine

# Authenticate kine route
@router.post("/auth", response_model=KineModel, response_model_by_alias=False)
async def authenticate_kine(
    email: str = Body(..., description="The email of the kine"),
    password: str = Body(..., description="The password of the kine")):
    """
    Retrieve a kine record with his email and password.
    Endpoint url example: http://localhost:8080/kine?email=qui@example.com&password=guillaume
    """
    read_kine = await kineService.read(email, password)
    if read_kine:
        return read_kine
    else:
        raise HTTPException(status_code=404, detail="Kine not found") 

# Read patients route
@router.get("/patients/{id}", response_description="Get patients", response_model=PatientCollection, response_model_by_alias=False)
async def read_patients(id: str):
    """
    Retrieve a list of patients for a specific kine.
    """
    read_patients = await kineService.read_all(id)
    if read_patients:
        return {"patients": read_patients}
    else:
        raise HTTPException(status_code=404, detail="Patients not found")

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
        update_result = await kineService.update(id, kine)
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Kine {id} not found")
    else: 
        if (existing_kine := kineService.read_one(id)) is not None:
            return existing_kine 
        else:
            raise HTTPException(status_code=404, detail=f"Kine {id} not found")
        
# Route pour supprimer un document
@router.delete("/{id}", response_description="Kine data deleted")
async def delete_document(id: str):
    """
    Remove a single kine record from the database.
    """
    delete_result = await kineService.delete(id)
    if delete_result == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Kine {id} not found")