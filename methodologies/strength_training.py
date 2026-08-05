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
        "type": "strength",
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

    # Handle None case
    if time_constraint is None:
        time_constraint = ""

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
    """Build undulating (DUP) program for intermediate lifters.

    Daily Undulating Periodization varies intensity within each week:
    - Heavy day: 85% 1RM, 3-5 reps
    - Medium day: 75% 1RM, 6-8 reps
    - Light day: 60% 1RM, 10-12 reps

    This allows intermediate athletes to train multiple qualities simultaneously.
    """
    weeks = []

    for week_num in range(1, 13):
        if week_num % 4 == 0:
            weeks.append(_create_dup_deload_week(week_num, analysis))
        else:
            weeks.append(_create_dup_week(week_num, analysis))

    return {
        "type": "strength",
        "periodization_model": "undulating",
        "experience_level": "intermediate",
        "goal": analysis.get("goal", "strength"),
        "weekly_pattern": {
            "monday": "heavy",
            "wednesday": "medium",
            "friday": "light"
        },
        "weeks": weeks,
        "progression_rules": _get_dup_progression_rules(),
        "deload_schedule": [4, 8],
        "total_duration": "12 weeks"
    }


def _create_dup_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a DUP week with heavy/medium/light pattern."""
    days = _get_available_days(analysis)
    sessions = []

    intensity_pattern = {
        "monday": "heavy",
        "wednesday": "medium",
        "friday": "light"
    }

    for day in days:
        if day in intensity_pattern:
            intensity = intensity_pattern[day]
            sessions.append(_create_dup_session(day, intensity, analysis))

    return {
        "week_number": week_num,
        "sessions": sessions,
        "pattern": "heavy/medium/light",
        "focus": "Variation in intensity for adaptation"
    }


def _create_dup_session(day: str, intensity: str, analysis: Dict) -> Dict[str, Any]:
    """Create a single DUP session."""
    intensity_params = {
        "heavy": {"percent": 0.85, "reps": "3-5", "rest": "3-5 min"},
        "medium": {"percent": 0.75, "reps": "6-8", "rest": "2-3 min"},
        "light": {"percent": 0.60, "reps": "10-12", "rest": "1-2 min"}
    }

    params = intensity_params[intensity]
    exercises = _get_exercises_for_dup(params)

    return {
        "day": day,
        "intensity": intensity,
        "exercises": exercises,
        "warmup": "5-10 min light cardio + dynamic stretching",
        "cooldown": "5-10 min stretching"
    }


def _get_exercises_for_dup(params: Dict) -> List[Dict]:
    """Get exercises for DUP session."""
    return [
        {"name": "Squat", "sets": 4, "reps": params["reps"], "percent_1rm": params["percent"], "rest": params["rest"]},
        {"name": "Bench Press", "sets": 4, "reps": params["reps"], "percent_1rm": params["percent"], "rest": params["rest"]},
        {"name": "Deadlift", "sets": 3, "reps": params["reps"], "percent_1rm": params["percent"], "rest": params["rest"]}
    ]


def _create_dup_deload_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a deload week for DUP."""
    days = _get_available_days(analysis)
    sessions = []

    for day in days:
        if day in ["monday", "wednesday", "friday"]:
            sessions.append({
                "day": day,
                "intensity": "light",
                "is_deload": True,
                "exercises": _get_exercises_for_dup({"percent": 0.60, "reps": "8-10", "rest": "2 min"}),
                "note": "Reduce volume, focus on technique"
            })

    return {
        "week_number": week_num,
        "is_deload": True,
        "sessions": sessions,
        "deload_reduction": 0.40
    }


def _get_dup_progression_rules() -> Dict[str, str]:
    """Get progression rules for DUP."""
    return {
        "weekly_progression": "Increase heavy day load by 2.5-5 lbs when target reps achieved",
        "medium_day_adjustment": "Maintain at ~80% of heavy day load",
        "light_day_adjustment": "Maintain at ~60% of heavy day load",
        "deload_frequency": "Every 4 weeks",
        "deload_protocol": "Reduce all session loads by 40%, maintain volume"
    }


def build_block_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build block periodization program for advanced lifters.

    Block periodization concentrates training effects in sequential blocks:
    1. Accumulation block: High volume, low intensity for work capacity
    2. Transmutation block: Convert to specific strength qualities
    3. Realization block: Maximize specific performance with peak intensity

    This allows advanced athletes to achieve high-level specificity in training.
    """
    blocks = []

    blocks.append(_create_accumulation_block(1, analysis))
    blocks.append(_create_transmutation_block(2, analysis))
    blocks.append(_create_realization_block(3, analysis))

    return {
        "type": "strength",
        "periodization_model": "block",
        "experience_level": "advanced",
        "goal": analysis.get("goal", "strength"),
        "blocks": blocks,
        "total_duration": "12 weeks",
        "progression_rules": _get_block_progression_rules(),
        "block_structure": "accumulation -> transmutation -> realization"
    }


def _create_accumulation_block(block_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create accumulation block."""
    weeks = []
    for week in range(1, 5):
        weeks.append({
            "week_number": week,
            "focus": "volume",
            "intensity": "moderate",
            "exercises": _get_accumulation_exercises(),
            "sessions_per_week": len(_get_available_days(analysis))
        })

    return {
        "block_number": block_num,
        "type": "accumulation",
        "duration": "4 weeks",
        "weeks": weeks,
        "focus": "Build work capacity",
        "volume": "high",
        "intensity": "low to moderate"
    }


def _create_transmutation_block(block_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create transmutation block."""
    weeks = []
    for week in range(1, 5):
        weeks.append({
            "week_number": week + 4,
            "focus": "strength conversion",
            "intensity": "high",
            "exercises": _get_transmutation_exercises(),
            "sessions_per_week": len(_get_available_days(analysis))
        })

    return {
        "block_number": block_num,
        "type": "transmutation",
        "duration": "4 weeks",
        "weeks": weeks,
        "focus": "Convert to specific strength",
        "volume": "moderate",
        "intensity": "moderate to high"
    }


def _create_realization_block(block_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create realization block."""
    weeks = []
    for week in range(1, 5):
        weeks.append({
            "week_number": week + 8,
            "focus": "maximal strength",
            "intensity": "very high",
            "exercises": _get_realization_exercises(),
            "sessions_per_week": len(_get_available_days(analysis))
        })

    return {
        "block_number": block_num,
        "type": "realization",
        "duration": "4 weeks",
        "weeks": weeks,
        "focus": "Maximize specific performance",
        "volume": "low",
        "intensity": "high"
    }


def _get_accumulation_exercises() -> List[Dict]:
    """Get exercises for accumulation block (high volume, low intensity)."""
    return [
        {"name": "Squat", "sets": 4, "reps": "8-10", "percent_1rm": 0.70},
        {"name": "Bench Press", "sets": 4, "reps": "10", "percent_1rm": 0.65},
        {"name": "Deadlift", "sets": 4, "reps": "6-8", "percent_1rm": 0.70},
        {"name": "Rows", "sets": 4, "reps": "12", "percent_1rm": 0.60}
    ]


def _get_transmutation_exercises() -> List[Dict]:
    """Get exercises for transmutation block (moderate volume, moderate intensity)."""
    return [
        {"name": "Squat", "sets": 5, "reps": "5", "percent_1rm": 0.80},
        {"name": "Bench Press", "sets": 5, "reps": "5", "percent_1rm": 0.80},
        {"name": "Deadlift", "sets": 4, "reps": "4", "percent_1rm": 0.80}
    ]


def _get_realization_exercises() -> List[Dict]:
    """Get exercises for realization block (low volume, high intensity)."""
    return [
        {"name": "Squat", "sets": 3, "reps": "3", "percent_1rm": 0.90},
        {"name": "Bench Press", "sets": 3, "reps": "3", "percent_1rm": 0.90},
        {"name": "Deadlift", "sets": 2, "reps": "2-3", "percent_1rm": 0.90}
    ]


def _get_block_progression_rules() -> Dict[str, str]:
    """Get progression rules for block periodization."""
    return {
        "accumulation_progression": "Increase volume first, then intensity",
        "transmutation_progression": "Focus on intensity increases",
        "realization_progression": "Peak at specific weights",
        "deload_between_blocks": "1 week reduced volume between blocks"
    }
