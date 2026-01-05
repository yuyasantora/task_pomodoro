from PySide6.QtCore import QObject, Signal, QTimer
from datetime import datetime
from .session import SessionData
from .config import PomodoroConfig


class PomodoroTimer(QObject):
    time_updated = Signal(int)
    phase_changed = Signal(str)
    session_completed = Signal(SessionData)

    def __init__(self, config: PomodoroConfig):
        super().__init__()
        self.config = config
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)

        self.current_phase = "work"
        self.remaining_seconds = config.work_duration * 60
        self.total_seconds = self.remaining_seconds
        self.completed_work_sessions = 0
        self.is_running = False

        self.current_session = None
        self.pause_count = 0

    def start(self):
        if not self.is_running:
            if self.current_session is None:
                self.current_session = SessionData(
                    session_type=self.current_phase,
                    start_time=datetime.now(),
                    planned_duration=self.total_seconds
                )
            self.is_running = True
            self.timer.start(1000)

    def pause(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            self.pause_count += 1

    def reset(self):
        self.timer.stop()
        self.is_running = False
        self._set_phase(self.current_phase)
        if self.current_session:
            self.current_session = None
        self.pause_count = 0

    def skip(self):
        if self.current_session:
            self.current_session.was_skipped = True
            self.current_session.end_time = datetime.now()
            self.current_session.actual_duration = self.total_seconds - self.remaining_seconds
            self.current_session.pause_count = self.pause_count
            self.session_completed.emit(self.current_session)

        self._advance_phase()
        self.current_session = None
        self.pause_count = 0

    def get_current_phase(self) -> str:
        return self.current_phase

    def get_remaining_time(self) -> int:
        return self.remaining_seconds

    def _tick(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.time_updated.emit(self.remaining_seconds)
        else:
            self._complete_session()

    def _complete_session(self):
        self.timer.stop()
        self.is_running = False

        if self.current_session:
            self.current_session.was_completed = True
            self.current_session.end_time = datetime.now()
            self.current_session.actual_duration = self.total_seconds
            self.current_session.pause_count = self.pause_count
            self.session_completed.emit(self.current_session)

        self._advance_phase()
        self.current_session = None
        self.pause_count = 0

    def _advance_phase(self):
        if self.current_phase == "work":
            self.completed_work_sessions += 1
            if self.completed_work_sessions % self.config.sessions_before_long_break == 0:
                self._set_phase("long_break")
            else:
                self._set_phase("short_break")
        else:
            self._set_phase("work")

    def _set_phase(self, phase: str):
        self.current_phase = phase

        if phase == "work":
            self.total_seconds = self.config.work_duration * 60
        elif phase == "short_break":
            self.total_seconds = self.config.short_break * 60
        elif phase == "long_break":
            self.total_seconds = self.config.long_break * 60

        self.remaining_seconds = self.total_seconds
        self.phase_changed.emit(phase)
        self.time_updated.emit(self.remaining_seconds)
