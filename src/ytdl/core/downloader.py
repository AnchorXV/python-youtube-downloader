"""Video downloader using yt-dlp."""

from pathlib import Path
from typing import Callable

import yt_dlp

from ytdl.core.models import VideoInfo

VALID_QUALITIES = ["best", "1080p", "720p", "480p", "360p", "240p", "144p"]


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
        progress_hook: Callable | None = None,
    ) -> dict:
        """Build yt-dlp options for downloading."""
        validate_quality(quality)
        # Format selector
        if audio_only:
            fmt = "bestaudio/best"
        elif quality == "best":
            fmt = "bestvideo+bestaudio/best"
        else:
            # quality = "720p" → height <= 720
            height = quality.replace("p", "")
            fmt = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
        
        # Output template: downloads/<title>.<ext>
        outtmpl = str(self.output_dir / "%(title)s.%(ext)s")
        
        opts = {
            "quiet": self.quiet,
            "no_warnings": False,
            "format": fmt,
            "outtmpl": outtmpl,
            "progress_hooks": [progress_hook] if progress_hook else [],
            "noprogress": True,  # kita pakai rich, bukan progress yt-dlp
            "restrictfilenames": True,  # for safe filenames
        }
        
        # Audio only: convert to mp3
        if audio_only:
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        
        return opts
    
    def download(
        self,
        url: str,
        quality: str = "best",
        audio_only: bool = False,
        progress_hook: Callable | None = None,
    ) -> Path:
        """Download video from URL.
        
        Args:
            url: YouTube video URL.
            quality: "best", "1080p", "720p", etc.
            audio_only: if True, download audio only (mp3).
            progress_hook: callback for progress updates.
        
        Returns:
            Path to downloaded file.
        
        Raises:
            DownloaderError: if download fails.
        """
        opts = self._build_options(quality, audio_only, progress_hook)
        
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
        except yt_dlp.utils.DownloadError as e:
            raise DownloaderError(f"Download failed: {e}") from e
        
        # Search for the downloaded file path
        filename = ydl.prepare_filename(info)
        
        # For audio-only downloads, change extension to .mp3
        if audio_only:
            filename = str(Path(filename).with_suffix(".mp3"))
        
        return Path(filename)