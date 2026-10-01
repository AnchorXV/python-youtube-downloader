"""Log panel — read-only text viewer."""

from PySide6.QtWidgets import (
    QGroupBox,
    QPlainTextEdit,
    QVBoxLayout,
)


class LogPanel(QGroupBox):
    """Panel showing log messages."""

    def __init__(self, parent=None):
        super().__init__("Log", parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 16)

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setPlaceholderText("Log messages will appear here...")
        layout.addWidget(self.log_view)

    def log(self, message: str):
        """Append a message to the log."""
        self.log_view.appendPlainText(message)