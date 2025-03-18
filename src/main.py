from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Sample data for doctors and their availability
doctors = {
    "John Smith": ["2025-03-10", "2025-03-11", "2025-03-13"],
    "Emily Johnson": ["2025-03-10", "2025-03-12"],
    "Michael Williams": ["2025-03-09", "2025-03-10", "2025-03-11"],
    "Sarah Brown": ["2025-03-12", "2025-03-13"],
    "David Jones": ["2025-03-09", "2025-03-13"]
}

class AppointmentData(BaseModel):
    first_name: str
    last_name: str
    date: str
    time: str
    doctor_fname: str
    doctor_lname: str
    reason: str

@app.post("/check_availability")
async def check_availability(data: AppointmentData):
    doctor_name = f"{data.doctor_fname} {data.doctor_lname}"
    appointment_date = data.date

    if doctor_name in doctors:
        if appointment_date in doctors[doctor_name]:
            return {"status": "success", "available": True, "message": f"{doctor_name} is available on {appointment_date}."}
        else:
            return {"status": "success", "available": False, "message": f"{doctor_name} is not available on {appointment_date}."}
    else:
        return {"status": "error", "message": "Doctor not found."}



