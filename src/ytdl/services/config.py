"""Configuration management for ytdl."""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, field_validator

from ytdl.core.downloader import VALID_FORMATS, VALID_QUALITIES


class DownloadConfig(BaseModel):
    """Download settings."""

    output_dir: str = "downloads"
    quality: str = "best"
    format: str | None = None
    audio_only: bool = False

    @field_validator("quality")
    @classmethod
    def validate_quality(cls, v: str) -> str:
        if v not in VALID_QUALITIES:
            raise ValueError(
                f"Invalid quality: {v!r}. "
                f"Valid: {', '.join(VALID_QUALITIES)}"
            )
        return v

    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.lower().lstrip(".")
        if v not in VALID_FORMATS:
            raise ValueError(
                f"Invalid format: {v!r}. "
                f"Valid: {', '.join(VALID_FORMATS)}"
            )
        return v


class AppConfig(BaseModel):
    """Top-level application config."""

    download: DownloadConfig = Field(default_factory=DownloadConfig)


DEFAULT_CONFIG_PATH = Path("config.yaml")


def load_config(path: Path | str = DEFAULT_CONFIG_PATH) -> AppConfig:
    """Load config from YAML file.
    
    Args:
        path: path to config file. If not exists, returns defaults.
    
    Returns:
        AppConfig instance.
    
    Raises:
        ValueError: if config file has invalid values.
    """
    path = Path(path)
    if not path.exists():
        return AppConfig()
    
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    
    return AppConfig(**data)