"""Application configuration loading utilities."""
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Weights(BaseModel):
    """Weights used when blending standardized indices."""

    GLI_G4_CB: float = Field(0.5, ge=0.0)
    GLI_Credit: float = Field(0.5, ge=0.0)

    def to_dict(self) -> Dict[str, float]:
        """Return weights as a dictionary."""

        return self.model_dump()


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env."""

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env", extra="ignore")

    env: str = Field("development", validation_alias="ENV")
    database_url: str = Field("sqlite+pysqlite:///:memory:", validation_alias="DATABASE_URL")
    redis_url: str = Field("redis://localhost:6379/0", validation_alias="REDIS_URL")
    fred_api_key: str | None = Field(None, validation_alias="FRED_API_KEY")

    default_z_window: int = Field(120, ge=12, validation_alias="DEFAULT_Z_WINDOW")
    use_fed_net: bool = Field(True, validation_alias="USE_FED_NET")
    step_hold_gli: bool = Field(True, validation_alias="STEP_HOLD_GLI")
    smooth_ma_months: int = Field(0, ge=0, validation_alias="SMOOTH_MA_MONTHS")
    index_scale: float = Field(100.0, validation_alias="INDEX_SCALE")
    index_multiplier: float = Field(10.0, validation_alias="INDEX_MULTIPLIER")
    rebase_date: str = Field("2015-01-31", validation_alias="REBASE_DATE")
    weights_json: Weights = Field(default_factory=Weights, validation_alias="WEIGHTS_JSON")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()


def get_settings_dict() -> Dict[str, Any]:
    """Convenience helper for serialising settings in APIs."""

    settings = get_settings()
    data = settings.model_dump()
    data["weights_json"] = settings.weights_json.to_dict()
    return data
