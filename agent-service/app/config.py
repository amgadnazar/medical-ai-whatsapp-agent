from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str
    model_name: str

    supabase_url: str
    supabase_key: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()