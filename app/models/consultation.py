from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from utils.model import * 
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]


class ConsultationModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    patientid: PyObjectId = Field(...)
    date_consultation: datetime = Field(...)
    flexion: Flexion = Field(...)
    extension: Extension = Field(...)
    bdk: str = "bdk"
    douleur_duree: str = Field(...)
    douleur_niveau: int = Field(...)
    nb_seances: int = Field(...)
    frequence_seances: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "patientid": "679b4cbc402485831ef448f3",
                "date_consultation": "2020-10-20",
                "flexion": {"active": 0.0, "passive": 0.0},
                "extension": {"active": 0.0, "passive": 0.0},
                "bdk": "bdk",
                "douleur_duree": "1 semaine",
                "douleur_niveau": 5,
                "nb_seances": 5,
                "frequence_seances": "1 fois par semaine"
            }
        },
    )

class UpdateConsultationModel(BaseModel):
    date_consultation: Optional[datetime] = None
    flexion: Optional[Flexion] = None
    extension: Optional[Extension] = None
    bdk: Optional[str] = None
    douleur_duree: Optional[str] = None
    douleur_niveau: Optional[int] = None
    nb_seances: Optional[int] = None
    frequence_seances: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "patientid": "5f8e1b7e1c7a8f5c3c1c1e3f",
                "date_consultation": "2020-10-20",
                "flexion": "active",
                "extension": "active",
                "bdk": "bdk",
                "douleur_duree": "1 semaine",
                "douleur_niveau": 5,
                "nb_seances": 5,
                "frequence_seances": "1 fois par semaine"
            }
        },
    )

class ConsultationFromPatient(BaseModel):
    id: PyObjectId = Field(alias="_id")  # L'ObjectId est converti en chaîne
    date_consultation: datetime = Field(...)
    flexion: Flexion = Field(...)
    extension: Extension = Field(...)

class ConsultationCollection(BaseModel):
    """
    A container holding a list of `ConsultationModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    consultations: List[ConsultationFromPatient]