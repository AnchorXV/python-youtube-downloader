"""Video metadata extractor from YouTube."""

import yt_dlp

from ytdl.core.models import VideoInfo


class ExtractorError(Exception):
    """Error when extracting video metadata."""
    pass


class Extractor:
    """Wrapper for yt-dlp extract video metadata."""
    
    def __init__(self, quiet: bool = True):
        self.quiet = quiet
    
    def _build_options(self) -> dict:
        """Build yt-dlp options."""
        return {
            "quiet": self.quiet,
            "skip_download": True,
            "no_warnings": False,
        }
    
    def get_info(self, url: str) -> VideoInfo:
        """Extract video metadata from a URL.
        
        Args:
            url: YouTube video URL.
        
        Returns:
            VideoInfo with video metadata.
        
        Raises:
            ExtractorError: if URL is invalid, video is private, or another error occurs.
        """
        try:
            with yt_dlp.YoutubeDL(self._build_options()) as ydl:
                raw = ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            raise ExtractorError(f"Failed to fetch video info: {e}") from e
        
        return VideoInfo(
            id=raw["id"],
            title=raw["title"],
            duration=raw.get("duration") or 0,
            uploader=raw.get("uploader") or "Unknown",
            webpage_url=raw["webpage_url"],
            formats=raw.get("formats") or [],
        )