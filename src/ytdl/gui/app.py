"""GUI entry point for ytdl."""

import sys
from PySide6.QtWidgets import QApplication
from ytdl.gui.main_window import MainWindow

def run() -> int:
    """Run the GUI application.
    
    Returns:
        Exit code (0 = success).
    """
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(run())