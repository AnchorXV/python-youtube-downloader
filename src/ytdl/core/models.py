"""Model data for ytdl."""

from dataclasses import dataclass


@dataclass
class VideoInfo:
    """Video information from YouTube."""
    
    id: str
    title: str
    duration: int
    uploader: str
    webpage_url: str
    formats: list
    
    @property
    def duration_str(self) -> str:
        """Duration in HH:MM:SS format."""
        total = self.duration
        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"
    
    @property
    def video_formats(self) -> list:
        """Video formats (not audio-only / storyboard)."""
        return [
            f for f in self.formats
            if f.get("vcodec") not in (None, "none")
            and f.get("ext") != "mhtml"
        ]
    
    @property
    def audio_formats(self) -> list:
        """Audio formats (for MP3 downloads)."""
        return [
            f for f in self.formats
            if f.get("vcodec") in (None, "none")
            and f.get("acodec") not in (None, "none")
        ]