from langchain_google_genai import ChatGoogleGenerativeAI

from agent.prompts import SYSTEM_PROMPT
from app.config import get_settings
from db.supabase_client import supabase
from rag.retriever import retrieve_context
from tools.appointment_tool import create_appointment

import json

settings = get_settings()

llm = ChatGoogleGenerativeAI(
    model=settings.model_name,
    google_api_key=settings.gemini_api_key,
    temperature=0.2,
)


def run_agent(phone: str, text: str) -> str:

    # ==========================
    # بيانات المريض
    # ==========================

    patient = (
        supabase.table("patients")
        .select("*")
        .eq("phone", phone)
        .execute()
    )

    patient_info = ""

    if patient.data:

        p = patient.data[0]

        patient_info = f"""
اسم المريض: {p.get("name")}
العمر: {p.get("age")}
الجنس: {p.get("gender")}
"""

    # ==========================
    # سجل المحادثة
    # ==========================

    history = (
        supabase.table("conversations")
        .select("*")
        .eq("patient_phone", phone)
        .order("created_at", desc=True)
        .limit(5)
        .execute()
    )

    conversation_history = ""

    if history.data:

        for msg in reversed(history.data):

            conversation_history += f"""
المريض:
{msg["user_message"]}

المساعد:
{msg["ai_response"]}
"""

    # ==========================
    # RAG
    # ==========================

    knowledge = retrieve_context(text)

    prompt = f"""
{SYSTEM_PROMPT}

معلومات المركز الطبي:

{knowledge}

بيانات المريض:

{patient_info}

سجل المحادثات:

{conversation_history}

رسالة العميل:

{text}
"""

    # ==========================
    # استدعاء Gemini
    # ==========================

    try:

        response = llm.invoke(prompt)

        content = response.content.strip()

    except Exception as e:

        print("Gemini Error:", e)

        error = str(e).lower()

        if (
            "resource_exhausted" in error
            or "429" in error
            or "quota" in error
            or "rate limit" in error
        ):

            return (
                "عذراً، تم استهلاك الحصة المجانية الخاصة بالنظام.\n\n"
                "يرجى المحاولة بعد قليل."
            )

        return (
            "تعذر الاتصال بخدمة الذكاء الاصطناعي حالياً.\n"
            "يرجى المحاولة مرة أخرى لاحقاً."
        )

    # ==========================
    # إزالة Markdown
    # ==========================

    if content.startswith("```json"):

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    # ==========================
    # معالجة JSON
    # ==========================

    answer = content

    try:

        result = json.loads(content)

        if result.get("intent") == "appointment":

            create_appointment(
                patient_phone=phone,
                doctor_name=result.get("doctor_name"),
                appointment_date=result.get("appointment_date")
            )

            answer = (
                f"تم تأكيد حجزك مع "
                f"{result.get('doctor_name')} "
                f"بتاريخ "
                f"{result.get('appointment_date')}"
            )

        else:

            answer = result.get("answer", content)

    except Exception:

        answer = content

    # ==========================
    # حفظ المحادثة
    # ==========================

    try:

        supabase.table("conversations").insert({

            "patient_phone": phone,
            "user_message": text,
            "ai_response": answer

        }).execute()

    except Exception as e:

        print("Database Error:", e)

    return answer