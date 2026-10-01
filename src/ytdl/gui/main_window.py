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

from ytdl.gui.widgets.info_panel import InfoPanel
from ytdl.gui.widgets.log_panel import LogPanel
from ytdl.gui.widgets.options_panel import OptionsPanel
from ytdl.gui.widgets.progress_panel import ProgressPanel
from ytdl.gui.widgets.url_bar import UrlBar


STYLES_PATH = Path(__file__).parent / "styles" / "main.qss"


class MainWindow(QMainWindow):
    """Main window of the ytdl application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)

        self._build_ui()
        self._load_stylesheet()

    def _build_ui(self):
        """Build the UI."""
        central = QWidget()
        self.setCentralWidget(central)

        # Outer layout
        outer = QVBoxLayout(central)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(12)

        # Header
        title = QLabel("YouTube Downloader")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(title)

        # URL bar
        self.url_bar = UrlBar()
        outer.addWidget(self.url_bar)

        # Splitter (kiri info+options, kanan progress+log)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(8)

        # ─── Left panel ─────────────────────────────
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(12)

        self.info_panel = InfoPanel()
        left_layout.addWidget(self.info_panel, stretch=1)    # ← 50%

        self.options_panel = OptionsPanel()
        left_layout.addWidget(self.options_panel, stretch=1)  # ← 50%

        # ─── Right panel ────────────────────────────
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(12)

        self.progress_panel = ProgressPanel()
        right_layout.addWidget(self.progress_panel, stretch=1)  # ← 50%

        self.log_panel = LogPanel()
        right_layout.addWidget(self.log_panel, stretch=1)       # ← 50%

        # Add to splitter
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([550, 550])
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        outer.addWidget(splitter, stretch=1)

        # ─── Action row (di bawah splitter) ──────────
        actions = QHBoxLayout()
        actions.setSpacing(8)
        actions.addStretch()  # dorong ke kanan

        self.download_button = QPushButton("Start Download")
        self.download_button.setObjectName("primaryButton")
        self.download_button.setMinimumWidth(140)
        actions.addWidget(self.download_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("ghostButton")
        self.clear_button.setMinimumWidth(100)
        actions.addWidget(self.clear_button)

        outer.addLayout(actions)

    def _load_stylesheet(self):
        """Load and apply QSS stylesheet."""
        if STYLES_PATH.exists():
            self.setStyleSheet(STYLES_PATH.read_text(encoding="utf-8"))