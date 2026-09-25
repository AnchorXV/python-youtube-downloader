"""Tests for ytdl.services.config."""

import pytest
from pydantic import ValidationError

from ytdl.services.config import AppConfig, DownloadConfig, load_config


def test_default_config():
    """Default config should have expected values."""
    cfg = DownloadConfig()
    assert cfg.quality == "best"
    assert cfg.output_dir == "downloads"
    assert cfg.audio_only is False
    assert cfg.format is None


def test_config_invalid_quality():
    """Invalid quality should raise ValidationError."""
    with pytest.raises(ValidationError, match="Invalid quality"):
        DownloadConfig(quality="9999p")


def test_config_invalid_format():
    """Invalid format should raise ValidationError."""
    with pytest.raises(ValidationError, match="Invalid format"):
        DownloadConfig(format="mp5")


def test_load_config_missing_file(tmp_path):
    """Missing file should return defaults."""
    cfg = load_config(tmp_path / "nonexistent.yaml")
    assert cfg.download.quality == "best"


def test_load_config_from_yaml(tmp_path):
    """Config should load from YAML file."""
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text("""
download:
  quality: 720p
  format: mp4
""")
    cfg = load_config(cfg_file)
    assert cfg.download.quality == "720p"
    assert cfg.download.format == "mp4"