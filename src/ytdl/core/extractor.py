import re
import yt_dlp
from ytdl.core.models import VideoInfo


# Regex untuk ANSI escape codes
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from a string."""
    return ANSI_ESCAPE.sub("", text)


class ExtractorError(Exception):
    """Error when extracting video metadata."""
    pass


class Extractor:
    """Wrapper for yt-dlp — extract video metadata."""

    def __init__(self, quiet: bool = True):
        self.quiet = quiet

    def _build_options(self) -> dict:
        """Build yt-dlp options."""
        return {
            "quiet": self.quiet,
            "skip_download": True,
            "no_warnings": True,
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
            raise ExtractorError(
                f"Failed to fetch video info: {strip_ansi(str(e))}"
            ) from e

        # Validate: pastikan ini video tunggal, bukan playlist/channel
        info_type = raw.get("_type", "video")
        if info_type != "video":
            raise ExtractorError(
                f"URL does not point to a single video "
                f"(got '{info_type}'). Please provide a direct video URL."
            )

        # Validate: pastikan ada format
        if not raw.get("formats"):
            raise ExtractorError(
                "No video formats found. The URL may not be a valid video."
            )

        return VideoInfo(
            id=raw["id"],
            title=raw["title"],
            duration=raw.get("duration") or 0,
            uploader=raw.get("uploader") or "Unknown",
            webpage_url=raw["webpage_url"],
            formats=raw.get("formats") or [],
        )