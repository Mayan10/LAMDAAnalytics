from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    google_maps_api_key: str = Field(..., alias="GOOGLE_MAPS_API_KEY")
    serp_api_key: str = Field(..., alias="SERP_API_KEY")
    weather_api_key: str = Field(..., alias="WEATHER_API_KEY")
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")

    weather_provider: str = Field("openweather", alias="WEATHER_PROVIDER")
    http_timeout_seconds: int = Field(30, alias="HTTP_TIMEOUT_SECONDS")
    agent_timeout_seconds: int = Field(40, alias="AGENT_TIMEOUT_SECONDS")
    scoring_state_path: str = Field("./data/scoring_state.json", alias="SCORING_STATE_PATH")
    log_level: str = Field("INFO", alias="LOG_LEVEL")

    enable_gdelt: bool = Field(False, alias="ENABLE_GDELT")
    enable_comtrade: bool = Field(False, alias="ENABLE_COMTRADE")
    allow_gemini_fallback: bool = Field(True, alias="ALLOW_GEMINI_FALLBACK")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
