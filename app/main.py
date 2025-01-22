import uvicorn
from fastapi import FastAPI
from routers import consultation, kine, patient

app = FastAPI()
app.include_router(kine.router, tags=["Kine"], prefix="/kine")
#app.include_router(patient.router, tags=["Patient"], prefix="/patient")
#app.include_router(consultation.router, tags=["Consultation"], prefix="/consultation")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "eMnia API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)