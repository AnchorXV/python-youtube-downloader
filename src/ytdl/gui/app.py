import sys
from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from ytdl.gui.main_window import MainWindow


FONTS_DIR = Path(__file__).parent.parent.parent.parent / "assets" / "fonts"

# Hanya load varian yang dibutuhkan
FONT_FILES = [
    "PlusJakartaSans-Regular.ttf",
    "PlusJakartaSans-Medium.ttf",
    "PlusJakartaSans-SemiBold.ttf",
    "PlusJakartaSans-Bold.ttf",
    "JetBrainsMono-Regular.ttf",
    "JetBrainsMono-Medium.ttf",
]


def load_fonts() -> None:
    """Load custom fonts from assets/fonts/."""
    if not FONTS_DIR.exists():
        print(f"Warning: Fonts folder not found at {FONTS_DIR}")
        return

    loaded_families: set[str] = set()
    for fname in FONT_FILES:
        path = FONTS_DIR / fname
        if not path.exists():
            print(f"Warning: Missing {fname}")
            continue

        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id == -1:
            print(f"Warning: Failed to load {fname}")
            continue

        # Ambil family name dari font ini
        families = QFontDatabase.applicationFontFamilies(font_id)
        loaded_families.update(families)

    print(f"Loaded font families: {sorted(loaded_families)}")


def run() -> int:
    """Run the GUI application."""
    app = QApplication(sys.argv)

    load_fonts()
    app.setFont(QFont("Plus Jakarta Sans", 10))

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(run())