"""Tests for ytdl.core.downloader."""

import pytest

from ytdl.core.downloader import (
    VALID_QUALITIES,
    build_video_format_selector,
    validate_quality,
)


@pytest.mark.parametrize("quality,expected_substring", [
    ("best", "bestvideo+bestaudio"),
    ("1080p", "height<=1080"),
    ("720p", "height<=720"),
    ("480p", "height<=480"),
    ("360p", "height<=360"),
])
def test_build_video_format_selector(quality, expected_substring):
    """Selector should include the target height."""
    selector = build_video_format_selector(quality)
    assert expected_substring in selector


def test_build_video_format_selector_has_fallback():
    """Selector for specific quality should have fallback chain."""
    selector = build_video_format_selector("720p")
    assert "/" in selector  # ada fallback
    assert "bestvideo+bestaudio" in selector  # fallback terakhir