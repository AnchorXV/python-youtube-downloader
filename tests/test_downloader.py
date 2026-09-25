"""Tests for ytdl.core.downloader."""

import pytest

from ytdl.core.downloader import VALID_QUALITIES, validate_quality


@pytest.mark.parametrize("quality", VALID_QUALITIES)
def test_validate_quality_valid(quality):
    """All valid qualities should pass."""
    assert validate_quality(quality) == quality


@pytest.mark.parametrize("invalid", ["9999p", "", "HD", "720", "p720"])
def test_validate_quality_invalid(invalid):
    """Invalid qualities should raise ValueError."""
    with pytest.raises(ValueError, match=invalid if invalid else "Invalid"):
        validate_quality(invalid)