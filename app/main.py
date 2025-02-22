import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from routers import consultation, kine, patient, upload_pose, stream_pose

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(kine.router, tags=["Kine"], prefix="/kine")
app.include_router(patient.router, tags=["Patient"], prefix="/patient")
app.include_router(consultation.router, tags=["Consultation"], prefix="/consultation")
app.include_router(upload_pose.router, tags=["Upload Pose"], prefix="/upload")
app.include_router(stream_pose.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "eMnia API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)