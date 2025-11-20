from pathlib import Path
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    photovault_root: Path = Field(Path("/Volumes/PhotoVault"), env="PB_PHOTOVAULT_ROOT")
    db_path: Path = Field(Path("/Volumes/PhotoVault/metadata/db/photobrain.db"), env="PB_DB_PATH")
    raw_processor: str = Field("darktable", env="PB_RAW_PROCESSOR")
    api_base_url: str = Field("http://localhost:8000", env="NEXT_PUBLIC_API_BASE_URL")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
