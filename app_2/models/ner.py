from pydantic import BaseModel, Field

class ExtractionEntity(BaseModel):
    text: str = Field(...)