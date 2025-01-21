from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from datetime import date
from ..utils.model import * 

PyObjectId = Annotated[str, BeforeValidator(str)]



class PatientModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    kineid: PyObjectId = Field(...)
    nom: str = Field(...)
    prenom: str = Field(...)
    date_naissance: date = Field(...)
    email: EmailStr = Field(...)
    tel: str = Field(...)
    adresse: Adresse = Field(...)
    sexe: Sexe = Field(...)
    carte_vitale: int = Field(...)
    anamnese: Anamnese = Field(...)
    morphostaique: Morphostatique = Field(...)
    travail: Travail = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "kineid": "5fc6b3f0d3e5c7b6b1b1f6f0",
                "nom": "Doe",
                "prenom": "John",
                "date_naissance": "1990-01-01",
                "email": "patient@example.com",
                "tel": "+123456789",
                "adresse":{"rue":"rue de la paix","ville":"Paris","code_postal":"75000"},
                "sex": True,
                "carte_vitale": 123456789,
                "anamnese": {"historique_maladie":"maladie","motif":"motif","antecedents":"antecedents","antecedents_familiaux":"antecedents_familiaux"},
                "morphostatique": {"taille": 1.80,"poids": 80,"lateralite":"droite","remarques":"remarques"},
                "travail": {"profession":"profession","sport":"sport"},
            }
        },
    )

class UpdatePatientModel(BaseModel):
    kineid: PyObjectId = Field(...)
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_naissance: Optional[date] = None
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
                "kineid": "5fc6b3f0d3e5c7b6b1b1f6f0",
                "nom": "Doe",
                "prenom": "John",
                "date_naissance": "1990-01-01",
                "email": "patient@example.com",
                "tel": "+123456789",
                "adresse":{"rue":"rue de la paix","ville":"Paris","code_postal":"75000"},
                "sex": True,
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

    students: List[PatientModel]