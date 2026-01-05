from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal


class TimerControls(QWidget):
    start_clicked = Signal()
    pause_clicked = Signal()
    reset_clicked = Signal()
    skip_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout()

        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.reset_btn = QPushButton("Reset")
        self.skip_btn = QPushButton("Skip")

        self.start_btn.clicked.connect(self.start_clicked.emit)
        self.pause_btn.clicked.connect(self.pause_clicked.emit)
        self.reset_btn.clicked.connect(self.reset_clicked.emit)
        self.skip_btn.clicked.connect(self.skip_clicked.emit)

        self.pause_btn.setEnabled(False)

        layout.addWidget(self.start_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.skip_btn)

        self.setLayout(layout)

    def set_running_state(self, is_running: bool):
        self.start_btn.setEnabled(not is_running)
        self.pause_btn.setEnabled(is_running)
