from fastapi import APIRouter, HTTPException
from models.ner import ExtractionEntity
from services.ner_service import extraction

router = APIRouter()

@router.post("/extract_entities")
async def extract(request: ExtractionEntity):
    try:
        cleaned_text = request.text.replace("\n", " ")
        print(cleaned_text)
        ent = extraction(cleaned_text)
        return ent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

