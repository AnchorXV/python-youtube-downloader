"""Video downloader using yt-dlp."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import yt_dlp

from ytdl.core.models import VideoInfo


VALID_QUALITIES = ["best", "1080p", "720p", "480p", "360p", "240p", "144p"]
VALID_FORMATS = ["mp4", "mkv", "webm", "mov", "avi", "wmv"]


def validate_quality(quality: str) -> str:
    """Validate quality string.

    Args:
        quality: quality string like "best", "720p".

    Returns:
        The validated quality string.

    Raises:
        ValueError: if quality is not recognized.
    """
    if quality not in VALID_QUALITIES:
        raise ValueError(
            f"Invalid quality: {quality!r}. "
            f"Valid options: {', '.join(VALID_QUALITIES)}"
        )
    return quality


def validate_format(fmt: str) -> str:
    """Validate output format.

    Args:
        fmt: format extension like "mp4", "mkv".

    Returns:
        The validated format (lowercase, no dot).

    Raises:
        ValueError: if format is not recognized.
    """
    fmt = fmt.lower().lstrip(".")
    if fmt not in VALID_FORMATS:
        raise ValueError(
            f"Invalid format: {fmt!r}. "
            f"Valid options: {', '.join(VALID_FORMATS)}"
        )
    return fmt


def build_video_format_selector(quality: str) -> str:
    """Build yt-dlp format selector for a given quality.

    Uses fallback chains: if the requested quality isn't available,
    yt-dlp will try the next best option.

    Args:
        quality: "best", "1080p", "720p", etc.

    Returns:
        yt-dlp format selector string.
    """
    if quality == "best":
        return "bestvideo+bestaudio/best"

    height = quality.rstrip("p")

    return (
        f"bestvideo[height<={height}]+bestaudio/"
        f"best[height<={height}]/"
        f"bestvideo+bestaudio/best"
    )


@dataclass
class DownloadResult:
    """Result of a download."""

    path: Path
    title: str
    quality: str
    format_id: str
    ext: str


class DownloaderError(Exception):
    """Error when downloading video."""
    pass


class Downloader:
    """Wrapper for yt-dlp to download videos."""

    def __init__(
        self,
        output_dir: Path | str = "downloads",
        quiet: bool = True,
    ):
        self.output_dir = Path(output_dir)
        self.quiet = quiet
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _build_options(
        self,
        quality: str = "best",
        audio_only: bool = False,
        output_format: str | None = None,
        progress_hook: Callable | None = None,
    ) -> dict:
        """Build yt-dlp options for downloading."""
        validate_quality(quality)
        if output_format:
            output_format = validate_format(output_format)

        # Format selector
        if audio_only:
            fmt = "bestaudio/best"
        else:
            fmt = build_video_format_selector(quality)

        outtmpl = str(self.output_dir / "%(title)s.%(ext)s")

        opts = {
            "quiet": self.quiet,
            "no_warnings": False,
            "format": fmt,
            "outtmpl": outtmpl,
            "progress_hooks": [progress_hook] if progress_hook else [],
            "noprogress": True,
            "restrictfilenames": True,
        }

        # Postprocessors
        postprocessors = []

        if audio_only:
            postprocessors.append({
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            })

        if output_format and not audio_only:
            postprocessors.append({
                "key": "FFmpegVideoConvertor",
                "preferedformat": output_format,   # yes, "prefered" (1 'r') is correct
            })

        if postprocessors:
            opts["postprocessors"] = postprocessors

        return opts

    def download(
        self,
        url: str,
        quality: str = "best",
        audio_only: bool = False,
        output_format: str | None = None,
        progress_hook: Callable | None = None,
    ) -> DownloadResult:
        """Download video from URL."""
        opts = self._build_options(
            quality, audio_only, output_format, progress_hook
        )

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
        except yt_dlp.utils.DownloadError as e:
            raise DownloaderError(f"Download failed: {e}") from e

        # Filename
        filename = ydl.prepare_filename(info)

        # Postprocessor might change extension
        if audio_only:
            filename = str(Path(filename).with_suffix(".mp3"))
        elif output_format:
            filename = str(Path(filename).with_suffix(f".{output_format}"))

        return DownloadResult(
            path=Path(filename),
            title=info.get("title", "Unknown"),
            quality=info.get("resolution") or info.get("format_note") or quality,
            format_id=str(info.get("format_id", "?")),
            ext=Path(filename).suffix.lstrip("."),
        )