from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


STYLES_PATH = Path(__file__).parent / "styles" / "main.qss"


class MainWindow(QMainWindow):
    """Main window of the ytdl application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ytdl — YouTube Downloader")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)

        self._build_ui()
        self._load_stylesheet()

    def _build_ui(self):
        """Build the UI."""
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)

        # Title
        title = QLabel("ytdl — YouTube Downloader")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("GUI under construction 🚧")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # URL bar (test)
        url_row = QHBoxLayout()
        url_input = QLineEdit()
        url_input.setPlaceholderText("Paste YouTube URL here...")
        url_row.addWidget(url_input)
        fetch_btn = QPushButton("Fetch Info")
        fetch_btn.setObjectName("primaryButton")
        url_row.addWidget(fetch_btn)
        layout.addLayout(url_row)

        # Progress bar (test)
        progress = QProgressBar()
        progress.setValue(45)
        layout.addWidget(progress)

        # Tombol download (test)
        download_btn = QPushButton("Start Download")
        download_btn.setObjectName("primaryButton")
        layout.addWidget(download_btn)

        layout.addStretch()

    def _load_stylesheet(self):
        """Load and apply QSS stylesheet."""
        if STYLES_PATH.exists():
            self.setStyleSheet(STYLES_PATH.read_text(encoding="utf-8"))