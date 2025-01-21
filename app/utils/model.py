from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from datetime import date
from enum import Enum

class Lateralite(str, Enum):
    droite = "droite"
    gauche = "gauche"
    ambidextre = "ambidextre"

class Sexe(str, Enum):
    homme = "homme"
    femme = "femme"

class Adresse(BaseModel):
    rue: str = Field(...)
    ville: str = Field(...)
    code_postal: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class Anamnese(BaseModel):
    historique_maladie: str = Field(...)
    motif: str = Field(...)
    antecedents: str = Field(...)
    antecedents_familiaux: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class Morphostatique(BaseModel):
    taille: float = Field(...)
    poids: float = Field(...)
    lateralite: Lateralite = Field(...)
    remarques: str = Field(...)
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

class Travail(BaseModel):
    profession: str = Field(...)
    sport: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class Flexion(str, Enum):
    active = "active"
    passive = "passive"

class Extension(str, Enum):
    active = "active"
    passive = "passive"