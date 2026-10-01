from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)


class UrlBar(QWidget):
    """Widget for URL input and fetch button."""

    fetchRequested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube URL here...")
        self.url_input.returnPressed.connect(self._emit_fetch)
        layout.addWidget(self.url_input, stretch=1)

        self.fetch_button = QPushButton("Fetch Info")
        self.fetch_button.setObjectName("primaryButton")
        self.fetch_button.setMinimumWidth(110)
        self.fetch_button.clicked.connect(self._emit_fetch)
        layout.addWidget(self.fetch_button)

    def _emit_fetch(self):
        """Emit fetchRequested with the current URL."""
        url = self.url_input.text().strip()
        if url:
            self.fetchRequested.emit(url)

    def set_enabled(self, enabled: bool):
        """Enable/disable input & button."""
        self.url_input.setEnabled(enabled)
        self.fetch_button.setEnabled(enabled)