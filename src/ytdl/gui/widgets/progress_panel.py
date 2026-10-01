from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QProgressBar,
    QVBoxLayout,
)


class ProgressPanel(QGroupBox):
    """Panel showing download progress and status."""

    def __init__(self, parent=None):
        super().__init__("Progress", parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(10)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("metaLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

    def set_status(self, text: str):
        """Update the status label."""
        self.status_label.setText(text)

    def set_progress(self, value: int):
        """Set progress value (0-100)."""
        self.progress_bar.setValue(value)

    def reset(self):
        """Reset to initial state."""
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready")