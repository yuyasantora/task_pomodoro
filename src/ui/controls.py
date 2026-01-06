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

        self._apply_styles()

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

    def _apply_styles(self):
        base_style = """
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
            QPushButton:disabled {{
                background-color: #BDBDBD;
                color: #757575;
            }}
        """

        self.start_btn.setStyleSheet(base_style.format(
            bg_color="#4CAF50", hover_color="#43A047", pressed_color="#388E3C"
        ))
        self.pause_btn.setStyleSheet(base_style.format(
            bg_color="#FF9800", hover_color="#FB8C00", pressed_color="#F57C00"
        ))
        self.reset_btn.setStyleSheet(base_style.format(
            bg_color="#2196F3", hover_color="#1E88E5", pressed_color="#1976D2"
        ))
        self.skip_btn.setStyleSheet(base_style.format(
            bg_color="#9C27B0", hover_color="#8E24AA", pressed_color="#7B1FA2"
        ))
