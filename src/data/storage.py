import json
from pathlib import Path
from typing import List
from ..core.session import SessionData

class SessionStorage:
    def __init__(self, storage_path: Path = None):
        if storage_path is None:
            storage_path = Path(__file__).parent.parent / 'data' / 'sessions.json'
        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.storage_path.exists():
            self._init_storage()
    
    def _init_storage(self):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump({'sessions': []}, f, indent=2)
            
    def save_session(self, session: SessionData):
        data = self._load_data()
        data['sessions'].append(session.to_dict())
        self._save_data(data)
    
    def load_sessions(self) -> List[SessionData]:
        data = self._load_data()
        return [SessionData.from_dict(s) for s in data['sessions']]
    
    def clear_all_sessions(self):
        self._save_data({'sessions': []})
        
    def _load_data(self) -> dict:
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {'sessions': []}
        
    def _save_data(self, data: dict):
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
            
            