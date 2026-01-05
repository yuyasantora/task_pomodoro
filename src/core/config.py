import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

@dataclass
class PomodoroConfig:
    work_duration: int = 25
    short_break: int = 5
    long_break: int = 15
    sessions_before_long_break: int = 4

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'PomodoroConfig':
        return cls(**data)
    
class ConfigManager:
    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'data' / 'config.json'
        self.config_path = config_path
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> PomodoroConfig:
        if not self.config_path.exists():
            return PomodoroConfig()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return PomodoroConfig.from_dict(data)
        except (json.JSONDecodeError, KeyError, TypeError):
            return PomodoroConfig()

    def save(self, config: PomodoroConfig):
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
            
                