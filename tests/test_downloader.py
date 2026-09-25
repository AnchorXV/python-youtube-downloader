import pytest

from ytdl.core.downloader import (
    VALID_FORMATS,
    VALID_QUALITIES,
    build_video_format_selector,
    validate_format,
    validate_quality,
)


@pytest.mark.parametrize("fmt", VALID_FORMATS)
def test_validate_format_valid(fmt):
    """All valid formats should pass."""
    assert validate_format(fmt) == fmt


def test_validate_format_strips_dot():
    """Leading dot should be stripped."""
    assert validate_format(".mp4") == "mp4"
    assert validate_format(".mkv") == "mkv"


def test_validate_format_case_insensitive():
    """Should accept uppercase."""
    assert validate_format("MP4") == "mp4"
    assert validate_format("MkV") == "mkv"


@pytest.mark.parametrize("invalid", ["xyz", "", "mp5", "vid"])
def test_validate_format_invalid(invalid):
    """Invalid formats should raise ValueError."""
    with pytest.raises(ValueError, match=invalid if invalid else "Invalid"):
        validate_format(invalid)