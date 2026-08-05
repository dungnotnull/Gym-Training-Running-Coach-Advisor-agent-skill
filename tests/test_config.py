import pytest
from config import config

def test_config_loads():
    assert config.get("system.version") == "1.0.0"
    assert config.get("performance.token_budget") == 3000

def test_config_get_with_default():
    assert config.get("nonexistent.key", "default") == "default"

def test_config_nested_get():
    assert config.get("logging.level") == "INFO"
