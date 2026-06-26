from fastapi import FastAPI

from schemas.patient import PatientCreate
from schemas.chat import ChatRequest
from schemas.appointment import AppointmentCreate

from db.supabase_client import supabase
from agent.agent import run_agent

app = FastAPI()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/chat")
def chat(request: ChatRequest):

    try:

        answer = run_agent(
            request.phone,
            request.text
        )

    except Exception as e:

        print("CHAT ERROR:", e)

        answer = (
            "عذراً، حدث خطأ في النظام."
            "\nيرجى المحاولة مرة أخرى بعد قليل."
        )

    return {
        "reply": answer
    }


@app.post("/patient")
def create_patient(patient: PatientCreate):

    supabase.table("patients").insert({
        "phone": patient.phone,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender
    }).execute()

    return {
        "message": "Patient created successfully"
    }


@app.post("/appointment")
def create_appointment(request: AppointmentCreate):

    supabase.table("appointments").insert({
        "patient_phone": request.patient_phone,
        "doctor_name": request.doctor_name,
        "appointment_date": request.appointment_date
    }).execute()

    return {
        "message": "Appointment created successfully"
    }