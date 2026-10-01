from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
)


class OptionsPanel(QGroupBox):
    """Panel with mode, format, and quality selectors."""

    def __init__(self, parent=None):
        super().__init__("Options", parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(12)

        # Mode selector (Video / Audio)
        mode_layout = QHBoxLayout()
        self.video_radio = QRadioButton("Video")
        self.video_radio.setChecked(True)
        self.audio_radio = QRadioButton("Audio Only")
        mode_layout.addWidget(self.video_radio)
        mode_layout.addWidget(self.audio_radio)
        mode_layout.addStretch()

        # Group radio biar cuma bisa pilih satu
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.video_radio)
        self.mode_group.addButton(self.audio_radio)

        layout.addLayout(mode_layout)

        # Format & Quality (pakai form layout)
        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(
            __import__("PySide6.QtCore", fromlist=["Qt"]).Qt.AlignmentFlag.AlignRight
        )

        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp4", "mkv", "webm", "mov", "avi", "wmv"])
        form.addRow("Format:", self.format_combo)

        self.quality_combo = QComboBox()
        self.quality_combo.addItems(
            ["best", "1080p", "720p", "480p", "360p", "240p", "144p"]
        )
        form.addRow("Quality:", self.quality_combo)

        layout.addLayout(form)
        layout.addStretch()