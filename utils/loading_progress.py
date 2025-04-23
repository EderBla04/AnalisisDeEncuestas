from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import QSize

class LoadingProgress(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(30, 30))
        
        self.setTextVisible(False)
        self.setRange(0, 0)  # Modo indeterminado
        self.setStyleSheet("""
            QProgressBar {
                border: 2px solid #cccccc;
                border-radius: 15px;
                background-color: transparent;
            }
            QProgressBar::chunk {
                background-color: transparent;
            }
        """)
