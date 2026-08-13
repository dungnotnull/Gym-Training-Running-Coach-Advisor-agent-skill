"""
Progression Planner Tool

Based on research:
- Rhea et al. (2003) - 2-10% increases optimal
- Kraemer & Ratamess (2004) - Progression variables
- ACSM (2009) - Progression guidelines

References:
- Rhea, M. R., et al. (2003). A meta-analysis to determine the dose response for strength development.
- Kraemer, W. J., & Ratamess, N. A. (2004). Fundamentals of Resistance Training: Progression.
- ACSM (2009). Progression models in resistance training.
"""

from typing import Dict, Any, List
from enum import Enum


class ProgressionType(Enum):
    LINEAR = "linear"
    UNDULATING = "undulating"
    BLOCK = "block"


def create_progression_plan(
    current_program: Dict[str, Any],
    progression_type: str = "linear"
) -> Dict[str, Any]:
    """
    Create detailed progression plan for training program.

    Research: Based on periodization principles from Bompa & Buzzichelli (2018)

    Args:
        current_program: Current training program with weeks
        progression_type: Type of progression model

    Returns:
        Dict with detailed progression plan
    """
    weeks = current_program.get("weeks", [])
    if not weeks:
        return {"error": "No weeks found in current program"}

    # Analyze current structure
    current_structure = _analyze_program_structure(current_program)

    # Create progression plan based on type
    if progression_type == "linear":
        return _create_linear_progression(weeks, current_structure)
    elif progression_type == "undulating":
        return _create_undulating_progression(weeks, current_structure)
    elif progression_type == "block":
        return _create_block_progression(weeks, current_structure)
    else:
        return {"error": f"Unknown progression type: {progression_type}"}


def _create_linear_progression(weeks: List[Dict], structure: Dict) -> Dict[str, Any]:
    """Create linear progression plan."""
    progression = {
        "type": "linear",
        "description": "Linear increase in intensity over time",
        "phases": [],
        "progression_rules": []
    }

    # Analyze current phases
    current_intensity_weeks = [w for w in weeks if "intensity_level" in w]
    if current_intensity_weeks:
        current_intensity = current_intensity_weeks[0]["intensity_level"]

        # Plan next progression
        if current_intensity < 0.70:
            progression["phases"].append({
                "phase": "hypertrophy_to_strength",
                "current_intensity": current_intensity,
                "target_intensity": 0.75,
                "duration_weeks": 4,
                "progression_rate": "Increase 2.5% per week"
            })
            progression["progression_rules"].append("Increase weight when top of rep range achieved")
        elif current_intensity < 0.85:
            progression["phases"].append({
                "phase": "strength_to_peaking",
                "current_intensity": current_intensity,
                "target_intensity": 0.90,
                "duration_weeks": 4,
                "progression_rate": "Increase 2.5% per week"
            })
            progression["progression_rules"].append("Maintain strict form as weight increases")
        else:
            progression["phases"].append({
                "phase": "peaking_to_competition",
                "current_intensity": current_intensity,
                "target_intensity": current_intensity,
                "duration_weeks": 2,
                "progression_rate": "Maintain intensity, reduce volume"
            })
            progression["progression_rules"].append("Taper: reduce volume 40-60%")

    progression["next_steps"] = [
        "Track weight and reps for each exercise",
        "Increase weight when target reps achieved with good form",
        "Deload every 4th week (50% volume reduction)",
        "Re-test 1RM after 12-week cycle"
    ]

    return progression


def _create_undulating_progression(weeks: List[Dict], structure: Dict) -> Dict[str, Any]:
    """Create undulating (DUP) progression plan."""
    progression = {
        "type": "undulating",
        "description": "Weekly variation in intensity with progression over weeks",
        "weekly_pattern": {
            "monday": "heavy",
            "wednesday": "medium",
            "friday": "light"
        },
        "progression_rules": []
    }

    # Analyze current intensities
    heavy_days = []
    for week in weeks:
        for session in week.get("sessions", []):
            if session.get("intensity") == "heavy":
                heavy_days.append(session)

    if heavy_days:
        # Analyze heavy day progression
        progression["progression_rules"].append("Progression occurs week-to-week, not within week")
        progression["progression_rules"].append("Heavy day: increase 2.5-5 lbs when target reps achieved")
        progression["progression_rules"].append("Medium day: maintain ~80% of heavy day")
        progression["progression_rules"].append("Light day: maintain ~60% of heavy day")
        progression["progression_rules"].append("Deload every 4th week: reduce all loads 40%")

    progression["next_steps"] = [
        "Maintain heavy/medium/light weekly pattern",
        "Track heavy day performance for progression",
        "Adjust medium and light days as heavy day increases",
        "Deload week 4, 8, 12"
    ]

    return progression


def _create_block_progression(weeks: List[Dict], structure: Dict) -> Dict[str, Any]:
    """Create block progression plan."""
    progression = {
        "type": "block",
        "description": "Sequential focus blocks with concentrated training",
        "block_sequence": ["accumulation", "transmutation", "realization"],
        "progression_rules": []
    }

    blocks = structure.get("blocks", [])
    if blocks:
        current_block_type = blocks[-1].get("type", "realization")

        if current_block_type == "accumulation":
            progression["next_block"] = {
                "type": "transmutation",
                "focus": "Convert general qualities to specific strength",
                "duration": "4 weeks",
                "volume": "moderate",
                "intensity": "moderate to high"
            }
            progression["progression_rules"].append("Build work capacity first, then convert")
        elif current_block_type == "transmutation":
            progression["next_block"] = {
                "type": "realization",
                "focus": "Maximize specific performance",
                "duration": "4 weeks",
                "volume": "low",
                "intensity": "high"
            }
            progression["progression_rules"].append("Peaking requires specificity - reduce exercise variety")
        else:
            # Currently in realization - next is recovery or new cycle
            progression["next_block"] = {
                "type": "transition",
                "focus": "Active recovery before next cycle",
                "duration": "1-2 weeks",
                "volume": "low",
                "intensity": "low"
            }
            progression["progression_rules"].append("Take deload after realization block")

    progression["next_steps"] = [
        "Complete current block as programmed",
        "Take 1-week deload between blocks",
        "Review and adjust goals for next block",
        "Test 1RM at end of each cycle"
    ]

    return progression


def _analyze_program_structure(program: Dict) -> Dict[str, Any]:
    """Analyze current program structure."""
    weeks = program.get("weeks", [])

    return {
        "total_weeks": len(weeks),
        "phases": _identify_phases(weeks),
        "current_intensity": _get_current_intensity(weeks),
        "deload_weeks": _identify_deloads(weeks)
    }


def _identify_phases(weeks: List[Dict]) -> List[str]:
    """Identify training phases in program."""
    phases = []
    for week in weeks:
        phase = week.get("phase", "unknown")
        if phase not in phases:
            phases.append(phase)
    return phases


def _get_current_intensity(weeks: List[Dict]) -> float:
    """Get current average intensity level."""
    intensities = []
    for week in weeks:
        if "intensity_level" in week:
            intensities.append(week["intensity_level"])
        if "intensity" in week:
            # Extract numeric value
            if isinstance(week["intensity"], str):
                if "high" in week["intensity"].lower():
                    intensities.append(0.85)
                elif "medium" in week["intensity"].lower():
                    intensities.append(0.75)
                elif "light" in week["intensity"].lower():
                    intensities.append(0.60)

    return sum(intensities) / len(intensities) if intensities else 0.65


def _identify_deloads(weeks: List[Dict]) -> List[int]:
    """Identify deload weeks."""
    deloads = []
    for i, week in enumerate(weeks, 1):
        if week.get("is_deload", False):
            deloads.append(i)
    return deloads


def calculate_overload_progression(
    starting_1rm: float,
    current_1rm: float,
    weeks_trained: int
) -> Dict[str, Any]:
    """
    Calculate progression and predict future gains.

    Research: Rhea et al. (2003) - 2-10% increases optimal

    Args:
        starting_1rm: Initial estimated or tested 1RM
        current_1rm: Current 1RM
        weeks_trained: Number of weeks trained

    Returns:
        Dict with progression analysis and predictions
    """
    if weeks_trained == 0:
        return {"error": "No training data"}

    improvement = ((current_1rm - starting_1rm) / starting_1rm) * 100
    weekly_improvement = improvement / weeks_trained

    # Predict future gains (diminishing returns)
    # Research: beginners gain 2-3% per week, intermediates 1%, advanced 0.5%
    predicted_weekly = max(0.5, weekly_improvement * 0.8)  # Diminishing returns

    weeks_to_target = {}
    target_increases = [5, 10, 15, 20]  # Target percentage increases

    for target in target_increases:
        target_weight = starting_1rm * (1 + target / 100)
        remaining = target - improvement
        weeks = remaining / (predicted_weekly * 100)
        weeks_to_target[f"+{target}%"] = max(1, round(weeks))

    return {
        "starting_1rm": starting_1rm,
        "current_1rm": current_1rm,
        "improvement_percentage": round(improvement, 2),
        "weekly_improvement": round(weekly_improvement * 100, 2),
        "predicted_weekly_rate": round(predicted_weekly * 100, 2),
        "predictions": weeks_to_target,
        "projection": f"At current rate, +10% gain in ~{weeks_to_target.get('+10%', 'N/A')} weeks"
    }


def create_deload_protocol(
    current_program: Dict,
    severity: str = "standard"
) -> Dict[str, Any]:
    """
    Create deload protocol based on current training load.

    Research: Based on recovery monitoring research (Kreher & Schwartz, 2012)

    Args:
        current_program: Current training program
        severity: "light", "standard", or "aggressive"

    Returns:
        Dict with deload week protocol
    """
    severity_settings = {
        "light": {"volume_reduction": 0.30, "intensity_reduction": 0.0},
        "standard": {"volume_reduction": 0.50, "intensity_reduction": 0.0},
        "aggressive": {"volume_reduction": 0.60, "intensity_reduction": 0.10}
    }

    settings = severity_settings.get(severity, severity_settings["standard"])

    # Analyze current training load
    weeks = current_program.get("weeks", [])
    if not weeks:
        return {"error": "No weeks to analyze"}

    # Get typical week structure
    reference_week = weeks[0]
    sessions = reference_week.get("sessions", [])

    deload_sessions = []
    for session in sessions:
        original_sets = []
        for exercise in session.get("exercises", []):
            original_sets.append({
                "name": exercise.get("name"),
                "original_sets": exercise.get("sets", 3),
                "original_reps": exercise.get("reps", "10")
            })

        # Calculate reduced sets
        reduced_sets = exercise.get("sets", 3) * (1 - settings["volume_reduction"])
        adjusted_sets = max(1, round(reduced_sets))

        deload_sessions.append({
            "day": session.get("day"),
            "type": "deload",
            "exercises": [
                {
                    "name": ex.get("name"),
                    "sets": adjusted_sets,
                    "reps": ex.get("reps"),
                    "rest": ex.get("rest"),
                    "percent_1rm": ex.get("percent_1rm", 0.70) * (1 - settings["intensity_reduction"])
                }
                for ex in session.get("exercises", [])
            ]
        })

    return {
        "severity": severity,
        "volume_reduction": f"{int(settings['volume_reduction'] * 100)}%",
        "intensity_reduction": f"{int(settings['intensity_reduction'] * 100)}%",
        "duration": "1 week",
        "sessions": deload_sessions,
        "focus": "Recovery and technique",
        "next_step": "Return to normal training with maintenance week"
    }
