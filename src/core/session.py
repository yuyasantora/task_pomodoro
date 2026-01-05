from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class SessionData:
    session_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    planned_duration: int = 0
    actual_duration: int = 0
    pause_count: int = 0
    was_skipped: bool = False
    was_completed: bool = False
    task_id: Optional[str] = None
    task_name: Optional[str] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data['start_time'] = self.start_time.isoformat()
        if self.end_time:
            data['end_time'] = self.end_time.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'SessionData':
        data = data.copy()
        data['start_time'] = datetime.fromisoformat(data['start_time'])
        if data.get('end_time'):
            data['end_time'] = datetime.fromisoformat(data['end_time'])
        return cls(**data)
    
    