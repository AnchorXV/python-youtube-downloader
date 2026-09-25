"""Tests for ytdl.core.extractor."""

from unittest.mock import MagicMock, patch

import pytest

from ytdl.core import Extractor, ExtractorError
from ytdl.core.models import VideoInfo


# Data palsu — seperti yang dikembalikan yt-dlp
FAKE_VIDEO_DATA = {
    "id": "abc123",
    "title": "Test Video",
    "duration": 300,
    "uploader": "Test Channel",
    "webpage_url": "https://youtube.com/watch?v=abc123",
    "formats": [
        {"format_id": "137", "ext": "mp4", "vcodec": "avc1", "acodec": "none"},
        {"format_id": "140", "ext": "m4a", "vcodec": "none", "acodec": "mp4a"},
    ],
}


def test_get_info_returns_video_info():
    """Extractor.get_info should return a VideoInfo object."""
    with patch("ytdl.core.extractor.yt_dlp.YoutubeDL") as mock_ydl_class:
        # Setup mock: ydl.extract_info() → FAKE_VIDEO_DATA
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.return_value = FAKE_VIDEO_DATA
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance
        
        extractor = Extractor()
        info = extractor.get_info("https://youtu.be/abc123")
        
        assert isinstance(info, VideoInfo)
        assert info.id == "abc123"
        assert info.title == "Test Video"
        assert info.duration == 300
        assert info.uploader == "Test Channel"


def test_get_info_raises_on_download_error():
    """Extractor should wrap yt-dlp errors in ExtractorError."""
    import yt_dlp
    
    with patch("ytdl.core.extractor.yt_dlp.YoutubeDL") as mock_ydl_class:
        mock_ydl_instance = MagicMock()
        mock_ydl_instance.extract_info.side_effect = yt_dlp.utils.DownloadError("Video unavailable")
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl_instance
        
        extractor = Extractor()
        
        with pytest.raises(ExtractorError, match="Failed to fetch"):
            extractor.get_info("https://youtu.be/invalid")