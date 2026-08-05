from typing import Dict, Any

def generate_running_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate running program based on analysis."""
    goal = analysis.get("goal", "general")

    if goal in ["5k", "10k"]:
        return build_race_preparation_program(analysis)
    elif goal in ["half_marathon", "marathon"]:
        return build_base_building_program(analysis)
    else:
        return {"type": "running", "status": "placeholder"}

def build_base_building_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build base building program for half marathon and marathon."""
    weeks = []

    for week_num in range(1, 13):
        weeks.append(_create_running_week(week_num, "base", analysis))

    return {
        "type": "running",
        "program_type": "base_building",
        "goal": analysis.get("goal", "marathon"),
        "weeks": weeks,
        "polarized_distribution": "80/20",
        "duration": "12 weeks"
    }

def build_race_preparation_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build race preparation program for 5K/10K."""
    weeks = []

    for week_num in range(1, 12):
        weeks.append(_create_running_week(week_num, "race_prep", analysis))

    return {
        "type": "running",
        "program_type": "race_preparation",
        "goal": analysis.get("goal", "5k"),
        "weeks": weeks,
        "polarized_distribution": "80/20",
        "duration": "11 weeks"
    }

def _create_running_week(week_num: int, phase: str, analysis: Dict) -> Dict[str, Any]:
    """Create a training week."""
    days = ["monday", "wednesday", "friday", "saturday"]
    sessions = []

    for day in days:
        sessions.append({
            "day": day,
            "type": "easy" if day in ["monday", "wednesday", "saturday"] else "interval",
            "zone": "zone1_easy" if day == "monday" else "zone2_marathon" if day == "saturday" else "zone4_interval"
        })

    return {"week_number": week_num, "sessions": sessions, "focus": phase}
