from app.database import supabase

response = supabase.table("patients").select("*").execute()

print(response.data)