from db.supabase_client import supabase


def create_appointment(
    patient_phone: str,
    doctor_name: str,
    appointment_date: str
):

    supabase.table("appointments").insert({
        "patient_phone": patient_phone,
        "doctor_name": doctor_name,
        "appointment_date": appointment_date
    }).execute()

    return "Appointment Created"