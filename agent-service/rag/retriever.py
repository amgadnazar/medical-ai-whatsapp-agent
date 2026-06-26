from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_DIR = BASE_DIR / "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vectordb = Chroma(
    persist_directory=str(CHROMA_DIR),
    embedding_function=embeddings
)

KEYWORDS = {
    "واتساب": ["واتساب"],
    "whatsapp": ["واتساب"],
    "الهاتف": ["الهاتف"],
    "رقم": ["الهاتف"],
    "التواصل": ["التواصل"],
    "العنوان": ["العنوان"],
    "عنوان": ["العنوان"],
    "موقع": ["العنوان"],
    "مواعيد": ["مواعيد العمل"],
    "دوام": ["مواعيد العمل"],
    "ساعات العمل": ["مواعيد العمل"],
    "كشف أطفال": ["service: كشف أطفال"],
    "كشف الباطنية": ["service: كشف باطنية"],
    "كشف جلدية": ["service: كشف جلدية"],

    # الأطباء
    "الأطباء": ["د."],
    "الدكاترة": ["د."],
    "اطباء": ["د."],
    "طبيب": ["د."],
    "من هم الأطباء": ["د."],
    "من هم اطباؤكم": ["د."],
}

DOCTOR_QUERIES = [
    "الأطباء",
    "الدكاترة",
    "اطباء",
    "اطباؤكم",
    "من هم الأطباء",
    "من هم اطباؤكم",
    "من الدكاترة",
    "طبيب الأطفال",
    "طبيب القلب",
    "طبيب الجلدية",
    "طبيب الأسنان",
    "طبيب النساء",
    "طبيب العظام",
]


def retrieve_context(query: str) -> str:

    query_lower = query.lower()

    # ==========================
    # لو السؤال عن الأطباء
    # رجع الملف كاملاً مباشرة
    # ==========================

    if any(word in query_lower for word in DOCTOR_QUERIES):

        doctors_file = BASE_DIR / "knowledge" / "doctors.txt"

        if doctors_file.exists():

            return doctors_file.read_text(
                encoding="utf-8"
            )

    # ==========================
    # البحث العادي
    # ==========================

    results = vectordb.similarity_search_with_score(
        query,
        k=20
    )

    ranked = []

    for doc, score in results:

        content = doc.page_content

        boost = 0

        for trigger, targets in KEYWORDS.items():

            if trigger.lower() in query_lower:

                for target in targets:

                    if target in content:
                        boost += 1000

        ranked.append(
            (
                boost - float(score),
                content
            )
        )

    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    seen = set()
    final_docs = []

    for _, content in ranked:

        content = content.strip()

        if content in seen:
            continue

        seen.add(content)

        final_docs.append(content)

    return "\n\n".join(final_docs[:5])