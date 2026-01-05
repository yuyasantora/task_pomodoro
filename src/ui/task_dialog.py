from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                               QLineEdit, QSpinBox, QPushButton, QListWidget,
                               QListWidgetItem, QTabWidget, QWidget, QMessageBox)
from PySide6.QtCore import Signal
from ..core.task import Task
from ..data.task_storage import TaskStorage


class TaskDialog(QDialog):
    task_selected = Signal(Task)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select or Create Task")
        self.setMinimumSize(500, 400)
        self.task_storage = TaskStorage()
        self.selected_task = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        tabs = QTabWidget()

        select_tab = self._create_select_tab()
        create_tab = self._create_create_tab()

        tabs.addTab(select_tab, "Select Existing Task")
        tabs.addTab(create_tab, "Create New Task")

        layout.addWidget(tabs)

        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Session")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _create_select_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        self.task_list = QListWidget()
        self.task_list.itemClicked.connect(self.on_task_selected)
        self.task_list.itemDoubleClicked.connect(self.on_task_double_clicked)

        self._load_tasks()

        delete_btn = QPushButton("Delete Selected Task")
        delete_btn.clicked.connect(self.on_delete_task)

        layout.addWidget(QLabel("Select a task:"))
        layout.addWidget(self.task_list)
        layout.addWidget(delete_btn)

        widget.setLayout(layout)
        return widget

    def _create_create_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()

        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name...")

        self.target_pomodoros_input = QSpinBox()
        self.target_pomodoros_input.setRange(1, 100)
        self.target_pomodoros_input.setValue(4)
        self.target_pomodoros_input.setSuffix(" pomodoros")

        create_btn = QPushButton("Create Task")
        create_btn.clicked.connect(self.on_create_task)

        layout.addWidget(QLabel("Task Name:"))
        layout.addWidget(self.task_name_input)
        layout.addWidget(QLabel("Target Pomodoros:"))
        layout.addWidget(self.target_pomodoros_input)
        layout.addWidget(create_btn)
        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def _load_tasks(self):
        self.task_list.clear()
        tasks = self.task_storage.load_tasks()

        for task in tasks:
            progress = task.get_progress() * 100
            item_text = f"{task.name} ({task.completed_pomodoros}/{task.target_pomodoros}) - {progress:.0f}%"
            item = QListWidgetItem(item_text)
            item.setData(256, task.task_id)
            self.task_list.addItem(item)

    def on_task_selected(self, item):
        task_id = item.data(256)
        self.selected_task = self.task_storage.get_task(task_id)
        self.start_btn.setEnabled(True)

    def on_task_double_clicked(self, item):
        self.on_task_selected(item)
        self.accept()

    def on_create_task(self):
        task_name = self.task_name_input.text().strip()
        if not task_name:
            QMessageBox.warning(self, "Error", "Please enter a task name.")
            return

        target_pomodoros = self.target_pomodoros_input.value()
        task = Task.create(task_name, target_pomodoros)
        self.task_storage.save_task(task)

        self.selected_task = task
        QMessageBox.information(self, "Success", f"Task '{task_name}' created!")
        self._load_tasks()
        self.start_btn.setEnabled(True)

    def on_delete_task(self):
        current_item = self.task_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a task to delete.")
            return

        reply = QMessageBox.question(
            self,
            "Delete Task",
            "Are you sure you want to delete this task?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            task_id = current_item.data(256)
            self.task_storage.delete_task(task_id)
            self._load_tasks()
            self.start_btn.setEnabled(False)

    def get_selected_task(self) -> Task:
        return self.selected_task
