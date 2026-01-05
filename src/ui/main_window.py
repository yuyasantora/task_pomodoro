from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QMenuBar, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from ..core.timer import PomodoroTimer
from ..core.config import PomodoroConfig, ConfigManager
from ..core.task import Task
from .controls import TimerControls
from .analog_clock import AnalogClockWidget
from .settings_dialog import SettingsDialog
from .task_dialog import TaskDialog
from ..data.storage import SessionStorage
from ..data.task_storage import TaskStorage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setMinimumSize(500, 600)

        self.config_manager = ConfigManager()
        self.config = self.config_manager.load()
        self.storage = SessionStorage()
        self.task_storage = TaskStorage()
        self.current_task = None

        self.timer = PomodoroTimer(self.config)
        self.timer.time_updated.connect(self.update_time_display)
        self.timer.phase_changed.connect(self.update_phase_display)
        self.timer.session_completed.connect(self.on_session_completed)

        self._setup_menu()
        self._setup_ui()

    def _setup_menu(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        settings_menu = menubar.addMenu("Settings")

        config_action = QAction("Configure Timer", self)
        config_action.triggered.connect(self.show_settings)
        settings_menu.addAction(config_action)
        
        data_menu = menubar.addMenu("Data")
        
        view_history_action = QAction("View History", self)
        view_history_action.triggered.connect(self.show_history)
        data_menu.addAction(view_history_action)
        
        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        data_menu.addAction(clear_history_action)

        task_menu = menubar.addMenu("Tasks")

        manage_tasks_action = QAction("Manage Tasks", self)
        manage_tasks_action.triggered.connect(self.show_task_manager)
        task_menu.addAction(manage_tasks_action)

        analysis_menu = menubar.addMenu("Analysis")

        show_analysis_action = QAction("Show Insights", self)
        show_analysis_action.triggered.connect(self.show_analysis)
        analysis_menu.addAction(show_analysis_action)

    def _setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.phase_label = QLabel("WORK")
        self.phase_label.setAlignment(Qt.AlignCenter)
        self.phase_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.task_label = QLabel("No task selected")
        self.task_label.setAlignment(Qt.AlignCenter)
        self.task_label.setStyleSheet("font-size: 14px; color: #666;")

        self.clock_widget = AnalogClockWidget()
        self.clock_widget.set_total_duration(self.timer.total_seconds)
        self.clock_widget.set_time(self.timer.get_remaining_time())
        self.clock_widget.set_phase(self.timer.get_current_phase())

        self.controls = TimerControls()
        self.controls.start_clicked.connect(self.on_start)
        self.controls.pause_clicked.connect(self.on_pause)
        self.controls.reset_clicked.connect(self.on_reset)
        self.controls.skip_clicked.connect(self.on_skip)

        layout.addWidget(self.phase_label)
        layout.addWidget(self.task_label)
        layout.addWidget(self.clock_widget)
        layout.addWidget(self.controls)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def update_time_display(self, seconds: int):
        self.clock_widget.set_time(seconds)

    def update_phase_display(self, phase: str):
        phase_display = {
            "work": "WORK",
            "short_break": "SHORT BREAK",
            "long_break": "LONG BREAK"
        }
        self.phase_label.setText(phase_display.get(phase, phase.upper()))

        colors = {
            "work": "#FF6B6B",
            "short_break": "#4ECDC4",
            "long_break": "#45B7D1"
        }
        color = colors.get(phase, "#000000")
        self.phase_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")

        self.clock_widget.set_phase(phase)
        self.clock_widget.set_total_duration(self.timer.total_seconds)

    def on_start(self):
        if self.timer.get_current_phase() == "work" and self.current_task is None:
            dialog = TaskDialog(self)
            if dialog.exec():
                self.current_task = dialog.get_selected_task()
                if self.current_task:
                    self.task_label.setText(f"Task: {self.current_task.name}")
                    self.timer.start()
                    self.controls.set_running_state(True)
            else:
                return
        else:
            self.timer.start()
            self.controls.set_running_state(True)

    def on_pause(self):
        self.timer.pause()
        self.controls.set_running_state(False)

    def on_reset(self):
        self.timer.reset()
        self.controls.set_running_state(False)
        self.update_time_display(self.timer.get_remaining_time())
        self.current_task = None
        self.task_label.setText("No task selected")

    def on_skip(self):
        self.timer.skip()
        self.controls.set_running_state(False)
        self.update_time_display(self.timer.get_remaining_time())

    def on_session_completed(self, session):
        if self.current_task and session.session_type == "work":
            session.task_id = self.current_task.task_id
            session.task_name = self.current_task.name

            self.current_task.add_session(session.actual_duration)
            self.task_storage.save_task(self.current_task)

            if self.current_task.get_progress() >= 1.0:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Task Completed!",
                    f"Congratulations! You've completed the task: {self.current_task.name}"
                )

            self.current_task = None
            self.task_label.setText("No task selected")

        self.storage.save_session(session)

    def show_settings(self):
        dialog = SettingsDialog(self.config, self)
        dialog.settings_changed.connect(self.on_settings_changed)
        dialog.exec()

    def on_settings_changed(self, new_config: PomodoroConfig):
        self.config = new_config
        self.config_manager.save(new_config)
        self.timer.config = new_config
        self.timer.reset()
        self.update_time_display(self.timer.get_remaining_time())
    
    def show_history(self):
        sessions = self.storage.load_sessions()
        from PySide6.QtWidgets import QMessageBox
        msg = QMessageBox(self)
        msg.setWindowTitle("Session History")
        msg.setText(f"Total sessions: {len(sessions)}")
        
        details = []
        for i, session in enumerate(sessions[-10:], 1):
            status = "Completed" if session.was_completed else "Skipped"
            task_info = f" - {session.task_name}" if session.task_name else ""
            details.append(f"{i}. {session.session_type} - {status}{task_info} - {session.start_time.strftime('%Y-%m-%d %H:%M')}")

        msg.setDetailedText("\n".join(details))
        msg.exec()

    def clear_history(self):
        from PySide6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all session history?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.storage.clear_all_sessions()
            QMessageBox.information(self, "Success", "Session history cleared.")

    def show_task_manager(self):
        dialog = TaskDialog(self)
        dialog.exec()

    def show_analysis(self):
        from .analysis_dialog import AnalysisDialog
        sessions = self.storage.load_sessions()
        dialog = AnalysisDialog(sessions, self)
        dialog.exec()
