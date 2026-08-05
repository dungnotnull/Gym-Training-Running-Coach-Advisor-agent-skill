import pytest
import shutil
from pathlib import Path


def test_log_event():
    from hooks.logging import log_event
    test_dir = ".test_logs"
    import hooks.logging as logging_module
    original_log_dir = logging_module.LOG_DIR
    logging_module.LOG_DIR = Path(test_dir)
    logging_module.LOG_DIR.mkdir(exist_ok=True)

    result = log_event("test_event", "session-123", {"test": "data"})
    assert result == True

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)
    logging_module.LOG_DIR = original_log_dir


def test_get_recent_logs():
    from hooks.logging import log_event, get_recent_logs
    test_dir = ".test_logs"
    import hooks.logging as logging_module
    original_log_dir = logging_module.LOG_DIR
    logging_module.LOG_DIR = Path(test_dir)
    logging_module.LOG_DIR.mkdir(exist_ok=True)

    log_event("test_event", "session-456", {"test": "data"})
    logs = get_recent_logs("session-456", 5)
    assert len(logs) > 0
    assert logs[0]["session_id"] == "session-456"

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)
    logging_module.LOG_DIR = original_log_dir


def test_get_recent_logs_limit():
    from hooks.logging import log_event, get_recent_logs
    test_dir = ".test_logs"
    import hooks.logging as logging_module
    original_log_dir = logging_module.LOG_DIR
    logging_module.LOG_DIR = Path(test_dir)
    logging_module.LOG_DIR.mkdir(exist_ok=True)

    # Create multiple logs
    for i in range(5):
        log_event("test_event", "session-limit", {"iteration": i})

    logs = get_recent_logs("session-limit", 3)
    assert len(logs) == 3

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)
    logging_module.LOG_DIR = original_log_dir