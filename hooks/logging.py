import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

LOG_DIR = Path(".logs")
LOG_DIR.mkdir(exist_ok=True)


def log_event(event_type: str, session_id: str, details: Dict[str, Any]) -> bool:
    """Log structured event with correlation ID."""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "correlation_id": str(uuid.uuid4()),
            "event_type": event_type,
            "session_id": session_id,
            "details": details
        }

        # Append to daily log file
        log_file = LOG_DIR / f"training_advisor_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        return True
    except Exception as e:
        print(f"Error logging event: {e}")
        return False


def get_recent_logs(session_id: Optional[str] = None, limit: int = 10) -> list:
    """Get recent log entries."""
    logs = []
    log_files = sorted(LOG_DIR.glob("training_advisor_*.jsonl"), reverse=True)

    for log_file in log_files[:3]:  # Last 3 days
        with open(log_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if session_id is None or entry.get("session_id") == session_id:
                    logs.append(entry)
                    if len(logs) >= limit:
                        return logs

    return logs[:limit]