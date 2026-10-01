from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)


class UrlBar(QWidget):
    """Widget for URL input and fetch button."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste YouTube URL here...")
        layout.addWidget(self.url_input, stretch=1)

        self.fetch_button = QPushButton("Fetch Info")
        self.fetch_button.setObjectName("primaryButton")
        self.fetch_button.setMinimumWidth(110)
        layout.addWidget(self.fetch_button)