from pydantic import BaseModel


class ChatRequest(BaseModel):
    phone: str
    name: str | None = None
    text: str