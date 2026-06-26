from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    patient_phone: str
    doctor_name: str
    appointment_date: str