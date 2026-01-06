from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QSpinBox, QPushButton, QFormLayout)
from PySide6.QtCore import Signal
from ..core.config import PomodoroConfig


class SettingsDialog(QDialog):
    settings_changed = Signal(PomodoroConfig)

    def __init__(self, config: PomodoroConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("Settings")
        self.setMinimumWidth(300)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.work_duration_spin = QSpinBox()
        self.work_duration_spin.setRange(1, 120)
        self.work_duration_spin.setValue(self.config.work_duration)
        self.work_duration_spin.setSuffix(" min")
        form_layout.addRow("Work Duration:", self.work_duration_spin)

        self.short_break_spin = QSpinBox()
        self.short_break_spin.setRange(1, 30)
        self.short_break_spin.setValue(self.config.short_break)
        self.short_break_spin.setSuffix(" min")
        form_layout.addRow("Short Break:", self.short_break_spin)

        self.long_break_spin = QSpinBox()
        self.long_break_spin.setRange(1, 60)
        self.long_break_spin.setValue(self.config.long_break)
        self.long_break_spin.setSuffix(" min")
        form_layout.addRow("Long Break:", self.long_break_spin)

        self.sessions_spin = QSpinBox()
        self.sessions_spin.setRange(2, 10)
        self.sessions_spin.setValue(self.config.sessions_before_long_break)
        form_layout.addRow("Sessions Before Long Break:", self.sessions_spin)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply")
        self.cancel_btn = QPushButton("Cancel")

        self.apply_btn.clicked.connect(self.on_apply)
        self.cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def on_apply(self):
        new_config = PomodoroConfig(
            work_duration=self.work_duration_spin.value(),
            short_break=self.short_break_spin.value(),
            long_break=self.long_break_spin.value(),
            sessions_before_long_break=self.sessions_spin.value()
        )
        self.settings_changed.emit(new_config)
        self.accept()
