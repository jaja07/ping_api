from fastapi import APIRouter, HTTPException, Depends, Body, status
from fastapi.responses import Response
from bson.objectid import ObjectId
from services.patient_service import PatientService
from fastapi.encoders import jsonable_encoder
from models.patient import (
    PatientModel,
    UpdatePatientModel
)
from models.consultation import ConsultationCollection

router = APIRouter()
patientService = PatientService()

#Create route
@router.post("/", response_description="New patient added", response_model=PatientModel, status_code=status.HTTP_201_CREATED, response_model_by_alias=False)
async def add_patient(patient: PatientModel = Body(...)):  #La requête doit contenir un corps JSON qui sera validé et converti en une instance du modèle PatientModel. Body(...) : Indique que cette donnée est obligatoire (le ... signifie "valeur requise").
    """
    Insert a new patient record.
    """
    patient_data = patient.model_dump(by_alias=True, exclude=["id"])  #Convertit l'instance du modèle en un dictionnaire Python. by_alias=True : Utilise les alias définis dans PatientModel (s'il y en a) pour les clés du dictionnaire.
    patientid = await patientService.create(patient_data)
    if patientid is None:
        raise HTTPException(status_code=500, detail="Patient could not be created")
    else:
        created_patient = await patientService.read_one(patientid)
    return created_patient

# Read route
@router.get("/{id}", response_description="Get a single patient", response_model=PatientModel, response_model_by_alias=False)
async def read_patient(id: str):
    """
    Retrieve a patient record.
    """
    read_patient = await patientService.read_one(id)
    if read_patient:
        return read_patient
    else:
        raise HTTPException(status_code=404, detail="patient not found")   

# Read consultations route
@router.get("/consultations/{id}", response_description="Get consultations", response_model=ConsultationCollection, response_model_by_alias=False)
async def read_patients(id: str):
    """
    Retrieve a list of consultations for a specific consultation.
    """
    read_consultations = await PatientService.read_all(id)
    if read_consultations:
        return read_consultations
    else:
        raise HTTPException(status_code=404, detail="Consultation not found")

# Update route
@router.put("/{id}", response_description="Patient data updated", response_model=PatientModel)
async def update_patient(id: str, patient: UpdatePatientModel = Body(...)):
    """
    Update individual fields of an existing patient record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    patient = {
        k: v for k, v in patient.model_dump(by_alias=True).items() if v is not None
    }
    if len(patient) >= 1:
        update_result = await patientService.update(id, patient)
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Patient {id} not found")
    else: 
        if (existing_patient := patientService.read_one(id)) is not None:
            return existing_patient 
        else:
            raise HTTPException(status_code=404, detail=f"Patient {id} not found")
        
# Route pour supprimer un document
@router.delete("/{id}", response_description="patient data deleted")
async def delete_document(id: str):
    """
    Remove a single patient record from the database.
    """
    delete_result = await patientService.delete(id)
    if delete_result == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Patient {id} not found")