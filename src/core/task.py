from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Task:
    task_id: str
    name: str
    target_pomodoros: int
    completed_pomodoros: int = 0
    total_seconds: int = 0
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    is_completed: bool = False
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
            
    @classmethod
    def create(cls, name: str, target_pomodoros: int) -> 'Task':
        return cls(
            task_id=str(uuid.uuid4()),
            name=name,
            target_pomodoros=target_pomodoros,
            created_at=datetime.now()
        )
    
    def add_session(self, duration_seconds: int):
        self.completed_pomodoros += 1
        self.total_seconds += duration_seconds
        
    def mark_completed(self):
        self.is_completed = True
        self.completed_at = datetime.now()
        
    def get_progress(self) -> float:
        if self.target_pomodoros == 0:
            return 0.0
        return min(1.0, self.completed_pomodoros / self.target_pomodoros)
    
    def to_dict(self) -> dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        if self.completed_at:
            data['completed_at'] = self.completed_at.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        data = data.copy()
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data.get('completed_at'):
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        return cls(**data)