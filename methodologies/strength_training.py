"""Strength training methodology implementations with periodization models."""

from typing import Dict, Any, List


def generate_strength_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate strength training program based on analysis.

    Routes to appropriate periodization model based on experience level.
    """
    experience = analysis.get("experience_level", "intermediate")

    if experience == "beginner":
        return build_linear_program(analysis)
    elif experience == "intermediate":
        return build_undulating_program(analysis)
    else:
        return build_block_program(analysis)


def build_linear_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build linear periodization program for beginners.

    Linear periodization follows a progressive overload model where:
    - Volume decreases over time
    - Intensity increases over time
    - Deload weeks every 4 weeks

    Phases:
    1. Hypertrophy/Endurance (weeks 1-4): High volume, low intensity
    2. Strength (weeks 5-8): Moderate volume, moderate intensity
    3. Peaking (weeks 9-12): Low volume, high intensity
    """
    weeks = []

    # Phase 1: Hypertrophy/Endurance (weeks 1-4)
    for week in range(1, 5):
        weeks.append(_create_hypertrophy_week(week, analysis))

    # Add deload to week 4
    weeks[3]["is_deload"] = True
    weeks[3]["deload_reduction"] = 0.5

    # Phase 2: Strength (weeks 5-8)
    for week in range(5, 9):
        weeks.append(_create_strength_week(week, analysis))

    # Add deload to week 8
    weeks[7]["is_deload"] = True
    weeks[7]["deload_reduction"] = 0.5

    # Phase 3: Peaking (weeks 9-12)
    for week in range(9, 13):
        weeks.append(_create_peaking_week(week, analysis))

    return {
        "periodization_model": "linear",
        "experience_level": "beginner",
        "goal": analysis.get("goal", "strength"),
        "weeks": weeks,
        "progression_rules": _get_linear_progression_rules(),
        "deload_schedule": [4, 8],
        "total_duration": "12 weeks"
    }


def _create_hypertrophy_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a hypertrophy-focused week.

    Hypertrophy phase characteristics:
    - High volume (3 sets, 10-12 reps)
    - Low intensity (65% 1RM)
    - Short rest periods (90 seconds)
    """
    days = _get_available_days(analysis)
    return {
        "week_number": week_num,
        "phase": "hypertrophy",
        "intensity_level": 0.65,
        "volume": "high",
        "reps_per_set": "10-12",
        "sets_per_exercise": 3,
        "rest_interval": "90 seconds",
        "sessions": _create_sessions(days, "hypertrophy"),
        "focus": "Work capacity and muscle development"
    }


def _create_strength_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a strength-focused week.

    Strength phase characteristics:
    - Moderate volume (4 sets, 5-8 reps)
    - Moderate intensity (80% 1RM)
    - Longer rest periods (3 minutes)
    """
    days = _get_available_days(analysis)
    return {
        "week_number": week_num,
        "phase": "strength",
        "intensity_level": 0.80,
        "volume": "moderate",
        "reps_per_set": "5-8",
        "sets_per_exercise": 4,
        "rest_interval": "3 minutes",
        "sessions": _create_sessions(days, "strength"),
        "focus": "Maximal strength development"
    }


def _create_peaking_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a peaking-focused week.

    Peaking phase characteristics:
    - Low volume (3 sets, 2-5 reps)
    - High intensity (90% 1RM)
    - Long rest periods (5 minutes)
    """
    days = _get_available_days(analysis)
    return {
        "week_number": week_num,
        "phase": "peaking",
        "intensity_level": 0.90,
        "volume": "low",
        "reps_per_set": "2-5",
        "sets_per_exercise": 3,
        "rest_interval": "5 minutes",
        "sessions": _create_sessions(days, "peaking"),
        "focus": "Maximal strength expression"
    }


def _get_available_days(analysis: Dict) -> List[str]:
    """Determine available training days from constraints.

    Defaults to 3 days per week if not specified.
    """
    time_constraint = analysis.get("constraints", {}).get("time_available", "")

    if "3" in time_constraint:
        return ["monday", "wednesday", "friday"]
    elif "4" in time_constraint:
        return ["monday", "tuesday", "thursday", "friday"]
    else:
        return ["monday", "wednesday", "friday"]


def _create_sessions(days: List[str], phase: str) -> List[Dict]:
    """Create training sessions for the week.

    Each session includes warmup, exercises, and cooldown.
    """
    sessions = []
    exercises = _get_exercises_for_phase(phase)

    for day in days:
        sessions.append({
            "day": day,
            "exercises": exercises,
            "warmup": "5-10 min light cardio + dynamic stretching",
            "cooldown": "5-10 min stretching"
        })

    return sessions


def _get_exercises_for_phase(phase: str) -> List[Dict]:
    """Get exercises appropriate for the training phase.

    Returns compound movements with sets, reps, and rest periods
    adjusted for the specific phase goals.
    """
    base_exercises = [
        {"name": "Squat", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Bench Press", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Deadlift", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Overhead Press", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Barbell Row", "sets": 3, "reps": "per_phase", "rest": "per_phase"}
    ]

    if phase == "hypertrophy":
        for ex in base_exercises:
            ex["reps"] = "10-12"
            ex["rest"] = "90 seconds"
    elif phase == "strength":
        for ex in base_exercises:
            ex["reps"] = "5-8"
            ex["rest"] = "3 minutes"
            if ex["name"] == "Squat":
                ex["sets"] = 4
    elif phase == "peaking":
        for ex in base_exercises:
            ex["reps"] = "3-5"
            ex["rest"] = "5 minutes"

    return base_exercises


def _get_linear_progression_rules() -> Dict[str, str]:
    """Get progression rules for linear periodization.

    Defines how athletes should progress load and when to deload.
    """
    return {
        "increases": "Increase weight when able to complete top of rep range",
        "deload": "Reduce volume by 50% every 4th week",
        "progression": "Linear intensity increase: 65% -> 80% -> 90% 1RM"
    }


def build_undulating_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build undulating periodization program for intermediate athletes.

    Daily undulating periodization varies intensity and volume within each week.
    Placeholder for future implementation.
    """
    return {"type": "undulating", "status": "placeholder"}


def build_block_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build block periodization program for advanced athletes.

    Block periodization focuses on specific training qualities in concentrated blocks.
    Placeholder for future implementation.
    """
    return {"type": "block", "status": "placeholder"}
