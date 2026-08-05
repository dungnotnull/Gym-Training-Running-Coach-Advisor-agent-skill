import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

SESSION_DIR = Path(".sessions")


class SessionManager:
    """Manage session persistence across requests."""

    def __init__(self, session_dir: str = ".sessions"):
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)

    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data to disk."""
        try:
            session_path = self.session_dir / f"{session_id}.json"
            with open(session_path, 'w') as f:
                json.dump(session_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data from disk."""
        try:
            session_path = self.session_dir / f"{session_id}.json"
            if session_path.exists():
                with open(session_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def update_program_history(self, session_id: str, program: Dict[str, Any]) -> bool:
        """Add program to session history."""
        session = self.load_session(session_id) or {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "program_history": [],
            "iteration_count": 0
        }

        session["iteration_count"] += 1
        session["program_history"].append({
            "iteration": session["iteration_count"],
            "timestamp": datetime.now().isoformat(),
            "program_summary": {"type": program.get("type")}
        })

        return self.save_session(session_id, session)

    def list_sessions(self) -> list:
        """List all available session IDs."""
        if not self.session_dir.exists():
            return []
        return [f.stem for f in self.session_dir.glob("*.json")]


session_manager = SessionManager()