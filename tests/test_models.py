"""Tests for ytdl.core.models."""


def test_duration_str_minutes_only(sample_video):
    """Duration under 1 hour → M:SS format."""
    sample_video.duration = 125
    assert sample_video.duration_str == "2:05"


def test_duration_str_with_hours(sample_video):
    """Duration over 1 hour → H:MM:SS format."""
    sample_video.duration = 3661
    assert sample_video.duration_str == "1:01:01"


def test_duration_str_zero(sample_video):
    """Duration 0 → 0:00."""
    sample_video.duration = 0
    assert sample_video.duration_str == "0:00"


def test_video_formats_filters_audio_only(sample_video_formats):
    """video_formats should exclude audio-only formats."""
    video_fmts = sample_video_formats.video_formats
    assert len(video_fmts) == 1
    assert video_fmts[0]["format_id"] == "137"


def test_audio_formats_filters_video_only(sample_video_formats):
    """audio_formats should only include audio-only formats."""
    audio_fmts = sample_video_formats.audio_formats
    assert len(audio_fmts) == 2
    assert {f["format_id"] for f in audio_fmts} == {"140", "251"}