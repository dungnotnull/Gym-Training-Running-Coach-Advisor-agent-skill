import pytest
import shutil
from pathlib import Path


def test_save_and_load_session():
    from hooks.state_management import SessionManager
    test_dir = ".test_sessions"
    mgr = SessionManager(test_dir)
    session_id = "test-session"
    data = {"test": "data"}

    assert mgr.save_session(session_id, data) == True
    loaded = mgr.load_session(session_id)
    assert loaded["test"] == "data"

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)


def test_update_program_history():
    from hooks.state_management import SessionManager
    test_dir = ".test_sessions"
    mgr = SessionManager(test_dir)
    session_id = "test-session-2"
    program = {"type": "strength"}

    mgr.update_program_history(session_id, program)
    session = mgr.load_session(session_id)
    assert session["iteration_count"] == 1
    assert len(session["program_history"]) == 1
    assert session["program_history"][0]["program_summary"]["type"] == "strength"

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)


def test_list_sessions():
    from hooks.state_management import SessionManager
    test_dir = ".test_sessions"
    mgr = SessionManager(test_dir)

    # Create some sessions
    mgr.save_session("session-1", {"data": "1"})
    mgr.save_session("session-2", {"data": "2"})

    sessions = mgr.list_sessions()
    assert "session-1" in sessions
    assert "session-2" in sessions

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)


def test_load_nonexistent_session():
    from hooks.state_management import SessionManager
    test_dir = ".test_sessions"
    mgr = SessionManager(test_dir)

    result = mgr.load_session("nonexistent")
    assert result is None

    # Cleanup
    shutil.rmtree(test_dir, ignore_errors=True)