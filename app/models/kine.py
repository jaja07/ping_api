from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from ..utils.model import * 

PyObjectId = Annotated[str, BeforeValidator(str)]

class KineModel(BaseModel):
    """
    KineModel: Modèle de données pour les kinés
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    nom: str = Field(...)
    prenom: str = Field(...)
    email: EmailStr = Field(...)
    mdp: str = Field(...)
    tel: str = Field(...)
    adresse: Adresse = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nom": "Doe",
                "prenom": "John",
                "email": "johndoe@example.com",
                "mdp": "securepassword",
                "tel": "+123456789",
                "adresse":{"rue":"rue de la paix","ville":"Paris","code_postal":"75000"},
            }
        },
    )

class UpdateKineModel(BaseModel):
    """
    KineModel: Modèle de données pour les kinés
    """
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    mdp: Optional[str] = None
    tel: Optional[str] = None
    adresse: Optional[Adresse] = None
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nom": "Doe",
                "prenom": "John",
                "email": "johndoe@example.com",
                "mdp": "securepassword",
                "tel": "+123456789",
                "adresse":{"rue":"rue de la paix","ville":"Paris","code_postal":"75000"},
            }
        },
    )
