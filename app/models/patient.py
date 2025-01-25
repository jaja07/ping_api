from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from datetime import datetime
from utils.model import * 

PyObjectId = Annotated[str, BeforeValidator(str)]

# Faire un modèle pour l'insertion de données dans la collection patient

class PatientModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    kineid: PyObjectId = Field(...)
    nom: str = Field(...)
    prenom: str = Field(...)
    date_naissance: datetime = Field(...)
    email: EmailStr = Field(...)
    tel: str = Field(...)
    adresse: Adresse = Field(...)
    sexe: Sexe = Field(...)
    carte_vitale: int = Field(...)
    anamnese: Anamnese = Field(...)
    morphostatique: Morphostatique = Field(...)
    travail: Travail = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "kineid": "64c3e5c82db9c3c33d56789a",
                "nom": "CAPO-CHCHI",
                "prenom": "Ken",
                "date_naissance": "1990-01-01",
                "email": "ken@example.com",
                "tel": "+123456789",
                "adresse":{"rue":"13 rue Lafayette","ville":"Rouen","code_postal":"76000"},
                "sexe": "homme",
                "carte_vitale": 123456789,
                "anamnese": {"historique_maladie":"maladie","motif":"motif","antecedents":"antecedents","antecedents_familiaux":"antecedents_familiaux"},
                "morphostatique": {"taille": 1.80,"poids": 80,"lateralite":"droite","remarques":"remarques"},
                "travail": {"profession":"data scientist","sport":"sport"},
            }
        },
    )

class UpdatePatientModel(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_naissance: Optional[datetime] = None
    email: Optional[EmailStr] = None
    tel: Optional[str] = None
    adresse: Optional[Adresse] = None
    sexe: Optional[Sexe] = None
    carte_vitale: Optional[int] = None
    anamnese: Optional[Anamnese] = None
    morphostaique: Optional[Morphostatique] = None
    travail: Optional[Travail] = None
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "kineid": "64c3e5c82db9c3c33d56789a",
                "nom": "HOUENOU",
                "prenom": "Wilfried",
                "date_naissance": "1990-01-01",
                "email": "will@example.com",
                "tel": "+123456789",
                "adresse":{"rue":"rue de la guerre","ville":"Paris","code_postal":"75000"},
                "sexe": "homme",
                "carte_vitale": 123456789,
                "anamnese": {"historique_maladie":"maladie","motif":"motif","antecedents":"antecedents","antecedents_familiaux":"antecedents_familiaux"},
                "morphostatique": {"taille": 1.80,"poids": 80,"lateralite":"droite","remarques":"remarques"},
                "travail": {"profession":"profession","sport":"sport"},
            }
        },
    )

class PatientCollection(BaseModel):
    """
    A container holding a list of `PatientModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    patients: List[PatientModel]