"""Main application window for ytdl GUI."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Main window of the ytdl application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ytdl — YouTube Downloader")
        self.resize(1100, 700)
        self.setMinimumSize(900, 600)

        # Central widget (wajib untuk QMainWindow)
        central = QWidget()
        self.setCentralWidget(central)

        # Layout utama
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Placeholder label (sementara)
        title = QLabel("ytdl — YouTube Downloader")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title)

        subtitle = QLabel("GUI under construction 🚧")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px;")
        layout.addWidget(subtitle)

        layout.addStretch()