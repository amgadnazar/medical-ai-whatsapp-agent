from pydantic import BaseModel

class PatientCreate(BaseModel):
    phone: str
    name: str
    age: int
    gender: str