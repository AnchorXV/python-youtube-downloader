from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from ytdl.core.models import VideoInfo


class InfoPanel(QGroupBox):
    """Panel showing video metadata."""

    def __init__(self, parent=None):
        super().__init__("Video Info", parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 20, 16, 16)
        layout.setSpacing(16)

        # Thumbnail placeholder
        self.thumbnail = QLabel()
        self.thumbnail.setFixedSize(160, 90)
        self.thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail.setObjectName("thumbnailPlaceholder")
        self.thumbnail.setText("No thumbnail")
        layout.addWidget(self.thumbnail)

        # Info column
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)

        self.title_label = QLabel("No video loaded")
        self.title_label.setObjectName("videoTitle")
        self.title_label.setWordWrap(True)
        info_layout.addWidget(self.title_label)

        self.uploader_label = QLabel("Uploader: —")
        self.uploader_label.setObjectName("metaLabel")
        info_layout.addWidget(self.uploader_label)

        self.duration_label = QLabel("Duration: —")
        self.duration_label.setObjectName("metaLabel")
        info_layout.addWidget(self.duration_label)

        info_layout.addStretch()
        layout.addLayout(info_layout, stretch=1)

    def set_video_info(self, video: VideoInfo):
        """Populate panel with video data."""
        self.title_label.setText(video.title)
        self.uploader_label.setText(f"Uploader: {video.uploader}")
        self.duration_label.setText(f"Duration: {video.duration_str}")

    def clear(self):
        """Reset panel to empty state."""
        self.title_label.setText("No video loaded")
        self.uploader_label.setText("Uploader: —")
        self.duration_label.setText("Duration: —")
        self.thumbnail.setText("No thumbnail")