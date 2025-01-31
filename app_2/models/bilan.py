from pydantic import BaseModel
from typing import List

class Test(BaseModel):
    nom: str
    valeur: str
    ref: str

class BilanKineData(BaseModel):
    date_bilan: str
    patient_nom: str
    patient_dob: str
    patient_age: int
    douleur_zone: str
    douleur_duree: str
    douleur_niveau: int
    douleur_description: str
    kine_nom: str
    kine_adresse: str
    kine_ville: str
    medecin_nom: str
    medecin_ville: str
    nb_seances: int
    frequence_seances: str
    tests: List[Test]