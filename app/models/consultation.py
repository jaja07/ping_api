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
    bdk: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "patientid": "5f8e1b7e1c7a8f5c3c1c1e3f",
                "date_consultation": "2020-10-20",
                "flexion": "active",
                "extension": "active",
                "bdk": "bdk"
            }
        },
    )

class UpdateConsultationModel(BaseModel):
    patientid: PyObjectId = Field(...)
    date_consultation: Optional[datetime] = None
    flexion: Optional[Flexion] = None
    extension: Optional[Extension] = None
    bdk: Optional[str] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "patientid": "5f8e1b7e1c7a8f5c3c1c1e3f",
                "date_consultation": "2020-10-20",
                "flexion": "active",
                "extension": "active",
                "bdk": "bdk"
            }
        },
    )

class ConsultationCollection(BaseModel):
    """
    A container holding a list of `ConsultationModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    consultations: List[ConsultationModel]