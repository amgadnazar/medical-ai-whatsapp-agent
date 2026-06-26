# 🩺 AI Medical WhatsApp Assistant

An AI-powered medical assistant that enables patients to communicate with a healthcare center directly through WhatsApp.

The system uses Google's Gemini AI together with Retrieval-Augmented Generation (RAG) to answer patient questions, provide healthcare information, and book appointments automatically.

---

# Features

- 🤖 AI-powered medical assistant
- 💬 WhatsApp integration
- 🧠 Google Gemini AI
- 📚 Retrieval-Augmented Generation (RAG)
- 📅 Appointment booking
- 👤 Patient management
- 🏥 Medical knowledge base
- 💾 Supabase database
- ⚡ FastAPI backend
- 🔍 Conversation history

---

# Tech Stack

## Backend

- Python
- FastAPI
- LangChain
- Google Gemini API

## Database

- Supabase

## Vector Database

- ChromaDB

## Messaging

- WhatsApp Web.js
- Node.js

---

# Project Structure

```
medical-ai-whatsapp-agent/

├── agent-service/
│   ├── agent/
│   ├── app/
│   ├── rag/
│   ├── tools/
│   ├── schemas/
│   ├── knowledge/
│   └── requirements.txt
│
├── whatsapp-service/
│   ├── index.js
│   ├── package.json
│   └── package-lock.json
│
└── README.md
```

---

# System Workflow

1. Patient sends a WhatsApp message.
2. WhatsApp Service receives the message.
3. FastAPI backend processes the request.
4. RAG retrieves medical knowledge.
5. Gemini AI generates a response.
6. Patient receives the answer instantly.
7. If needed, an appointment is automatically created and stored in Supabase.

---

# Technologies

- Python
- FastAPI
- LangChain
- Google Gemini
- ChromaDB
- Supabase
- WhatsApp Web.js
- Node.js

---

# Installation

## Clone the repository

```bash
git clone https://github.com/amgadnazar/medical-ai-whatsapp-agent.git
```

## Backend

```bash
cd agent-service

pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```

---

## WhatsApp Service

```bash
cd whatsapp-service

npm install

node index.js
```

---

# Environment Variables

Create a `.env` file inside `agent-service`

```
GEMINI_API_KEY=YOUR_API_KEY

SUPABASE_URL=YOUR_SUPABASE_URL

SUPABASE_KEY=YOUR_SUPABASE_KEY

MODEL_NAME=gemini-2.5-flash
```

---

# Screenshots

## WhatsApp Conversation

![WhatsApp Chat](screenshots/whatsapp-chat.png)

---

## Appointment Booking

![Appointment Booking](screenshots/appointment-booking.png)

---

## Supabase Database

![Supabase Database](screenshots/supabase-tables.png)

# System Architecture

```mermaid
flowchart LR

    U[Patient]

    W[WhatsApp]

    N[WhatsApp Service<br/>Node.js]

    A[FastAPI Backend]

    G[Google Gemini]

    C[ChromaDB]

    S[(Supabase)]

    U --> W
    W --> N
    N --> A

    A --> G
    A --> C
    A --> S

    G --> A
    C --> A
    S --> A

    A --> N
    N --> W
    W --> U
```

# Future Improvements

- Voice messages
- Arabic speech recognition
- Doctor dashboard
- Patient dashboard
- Docker deployment
- Cloud deployment
- Multi-language support

---

# Author

**Amgad Nazar**

LinkedIn:
https://linkedin.com/in/amjad-nazar

Portfolio:
https://amgadnazar.github.io

GitHub:
https://github.com/amgadnazar
