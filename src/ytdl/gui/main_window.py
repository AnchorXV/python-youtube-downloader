from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ytdl.core.models import VideoInfo
from ytdl.gui.widgets.info_panel import InfoPanel
from ytdl.gui.widgets.log_panel import LogPanel
from ytdl.gui.widgets.options_panel import OptionsPanel
from ytdl.gui.widgets.progress_panel import ProgressPanel
from ytdl.gui.widgets.url_bar import UrlBar
from ytdl.gui.workers import FetchInfoWorker


STYLES_PATH = Path(__file__).parent / "styles" / "main.qss"


class MainWindow(QMainWindow):
    """Main window of the ytdl application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)

        self._worker: FetchInfoWorker | None = None

        self._build_ui()
        self._connect_signals()
        self._load_stylesheet()

    def _build_ui(self):
        """Build the UI."""
        central = QWidget()
        self.setCentralWidget(central)

        outer = QVBoxLayout(central)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(12)

        title = QLabel("YouTube Downloader")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        self.url_bar = UrlBar()
        outer.addWidget(self.url_bar)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)

        # Left panel
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        self.info_panel = InfoPanel()
        left_layout.addWidget(self.info_panel, stretch=1)

        self.options_panel = OptionsPanel()
        left_layout.addWidget(self.options_panel, stretch=1)

        # Right panel
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        self.progress_panel = ProgressPanel()
        right_layout.addWidget(self.progress_panel, stretch=1)

        self.log_panel = LogPanel()
        right_layout.addWidget(self.log_panel, stretch=1)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([550, 550])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        outer.addWidget(splitter, stretch=1)

        # Action row
        actions = QHBoxLayout()
        actions.setSpacing(8)
        actions.addStretch()

        self.download_button = QPushButton("Start Download")
        self.download_button.setObjectName("primaryButton")
        self.download_button.setMinimumWidth(140)
        actions.addWidget(self.download_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("ghostButton")
        self.clear_button.setMinimumWidth(100)
        actions.addWidget(self.clear_button)

        outer.addLayout(actions)

    def _connect_signals(self):
        """Connect signals to slots."""
        self.url_bar.fetchRequested.connect(self._on_fetch_requested)
        self.clear_button.clicked.connect(self._on_clear)

    def _load_stylesheet(self):
        """Load and apply QSS stylesheet."""
        if STYLES_PATH.exists():
            self.setStyleSheet(STYLES_PATH.read_text(encoding="utf-8"))

    # ─── Slots ─────────────────────────────────────

    def _on_fetch_requested(self, url: str):
        """Handle Fetch Info button click."""
        self.log_panel.log(f"→ Fetching: {url}")
        self.progress_panel.set_status("Fetching info...")
        self.info_panel.clear()
        self.url_bar.set_enabled(False)

        self._worker = FetchInfoWorker(url)
        self._worker.success.connect(self._on_fetch_success)
        self._worker.error.connect(self._on_fetch_error)
        self._worker.start()

    def _on_fetch_success(self, video: VideoInfo):
        """Handle successful info fetch."""
        self.info_panel.set_video_info(video)
        self.progress_panel.set_status("Ready")
        self.url_bar.set_enabled(True)
        self.log_panel.log(f"✓ Fetched: {video.title}")
        self.log_panel.log(
            f"  {len(video.formats)} formats available "
            f"({len(video.video_formats)} video, {len(video.audio_formats)} audio)"
        )

    def _on_fetch_error(self, message: str):
        """Handle fetch error."""
        self.progress_panel.set_status("Error")
        self.url_bar.set_enabled(True)
        self.log_panel.log(f"✗ Error: {message}")

    def _on_clear(self):
        """Handle Clear button click."""
        self.url_bar.url_input.clear()
        self.info_panel.clear()
        self.progress_panel.reset()
        self.log_panel.log_view.clear()
        self.log_panel.log("Cleared.")