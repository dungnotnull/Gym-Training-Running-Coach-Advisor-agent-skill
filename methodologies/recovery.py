"""Recovery-focused training methodology."""
from typing import Dict, Any, List


def generate_recovery_plan(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate recovery-focused program.

    Args:
        analysis: User analysis dict containing experience_level, goal, constraints

    Returns:
        Recovery program with 4 weeks of low-intensity training
    """
    weeks = []

    for week_num in range(1, 5):
        weeks.append({
            "week_number": week_num,
            "focus": "recovery",
            "intensity": "low",
            "sessions": _create_recovery_sessions(analysis)
        })

    return {
        "type": "recovery",
        "duration": "4 weeks",
        "weeks": weeks,
        "focus": "Restore and rebuild"
    }


def _create_recovery_sessions(analysis: Dict) -> List[Dict]:
    """Create recovery-focused training sessions.

    Args:
        analysis: User analysis dict

    Returns:
        List of recovery sessions
    """
    sessions = [
        {
            "day": "Monday",
            "zone": "zone1_easy",
            "duration": "20-30 min",
            "type": "easy_run",
            "description": "Very easy conversational pace"
        },
        {
            "day": "Tuesday",
            "zone": "rest",
            "duration": "rest",
            "type": "rest",
            "description": "Full rest day"
        },
        {
            "day": "Wednesday",
            "zone": "zone1_easy",
            "duration": "25-35 min",
            "type": "easy_run",
            "description": "Easy aerobic work"
        },
        {
            "day": "Thursday",
            "zone": "rest",
            "duration": "rest",
            "type": "rest",
            "description": "Full rest day"
        },
        {
            "day": "Friday",
            "zone": "zone1_easy",
            "duration": "20-30 min",
            "type": "easy_run",
            "description": "Light easy run"
        },
        {
            "day": "Saturday",
            "zone": "rest",
            "duration": "rest",
            "type": "rest",
            "description": "Full rest day"
        },
        {
            "day": "Sunday",
            "zone": "zone1_easy",
            "duration": "30-40 min",
            "type": "easy_run",
            "description": "Slightly longer easy effort"
        }
    ]

    return sessions


def assess_overtraining_risk(session: Dict) -> Dict:
    """Assess overtraining risk based on session flags.

    Args:
        session: Training session dict with optional flags key

    Returns:
        Dict with risk_level: "high" or "low"
    """
    flags = session.get("flags", [])

    if "recovery_concern" in flags:
        return {"risk_level": "high"}

    return {"risk_level": "low"}
