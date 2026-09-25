"""Shared fixtures for all tests."""

import pytest

from ytdl.core.models import VideoInfo


@pytest.fixture
def sample_video():
    """Basic VideoInfo for testing."""
    return VideoInfo(
        id="test",
        title="Test Video",
        duration=125,
        uploader="Test",
        webpage_url="https://test.com",
        formats=[],
    )


@pytest.fixture
def sample_video_formats():
    """VideoInfo with mixed formats for filter testing."""
    return VideoInfo(
        id="test",
        title="Test Video",
        duration=300,
        uploader="Test",
        webpage_url="https://test.com",
        formats=[
            {"format_id": "137", "ext": "mp4", "vcodec": "avc1", "acodec": "none"},
            {"format_id": "140", "ext": "m4a", "vcodec": "none", "acodec": "mp4a"},
            {"format_id": "251", "ext": "webm", "vcodec": "none", "acodec": "opus"},
            {"format_id": "sb0", "ext": "mhtml", "vcodec": "none", "acodec": "none"},
        ],
    )