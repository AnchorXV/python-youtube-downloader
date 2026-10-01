from PySide6.QtCore import QThread, Signal
from ytdl.core import Extractor, ExtractorError
from ytdl.core.models import VideoInfo


class FetchInfoWorker(QThread):
    """Worker thread to fetch video info without blocking UI."""

    success = Signal(VideoInfo)
    error = Signal(str)

    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        """Run in background thread — called by QThread.start()."""
        try:
            extractor = Extractor()
            info = extractor.get_info(self.url)
            self.success.emit(info)
        except ExtractorError as e:
            self.error.emit(str(e))
        except Exception as e:
            self.error.emit(f"Unexpected error: {e}")