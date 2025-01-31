import uvicorn
from fastapi import FastAPI
from routers import transcription
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(transcription.router, tags=["Transcription"], prefix="/transcription")
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "eMnia API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)