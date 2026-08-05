import json
from pathlib import Path
from typing import Dict, Any

class Config:
    _instance = None
    _config: Dict[str, Any] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self) -> Dict[str, Any]:
        if self._config is None:
            config_path = Path(__file__).parent / "settings.json"
            with open(config_path) as f:
                self._config = json.load(f)
        return self._config

    def get(self, key: str, default=None) -> Any:
        config = self.load()
        keys = key.split(".")
        value = config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

config = Config()
