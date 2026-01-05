import json
from pathlib import Path
from typing import List, Optional
from ..core.task import Task


class TaskStorage:
    def __init__(self, storage_path: Path = None):
        if storage_path is None:
            storage_path = Path(__file__).parent.parent / 'data' / 'tasks.json'
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.storage_path.exists():
            self._init_storage()

    def _init_storage(self):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump({"tasks": []}, f, indent=2)

    def save_task(self, task: Task):
        data = self._load_data()
        existing_index = None
        for i, t in enumerate(data['tasks']):
            if t['task_id'] == task.task_id:
                existing_index = i
                break

        if existing_index is not None:
            data['tasks'][existing_index] = task.to_dict()
        else:
            data['tasks'].append(task.to_dict())

        self._save_data(data)

    def load_tasks(self, include_completed: bool = False) -> List[Task]:
        data = self._load_data()
        tasks = [Task.from_dict(t) for t in data['tasks']]
        if not include_completed:
            tasks = [t for t in tasks if not t.is_completed]
        return tasks

    def get_task(self, task_id: str) -> Optional[Task]:
        tasks = self.load_tasks(include_completed=True)
        for task in tasks:
            if task.task_id == task_id:
                return task
        return None

    def delete_task(self, task_id: str):
        data = self._load_data()
        data['tasks'] = [t for t in data['tasks'] if t['task_id'] != task_id]
        self._save_data(data)

    def _load_data(self) -> dict:
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"tasks": []}

    def _save_data(self, data: dict):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
