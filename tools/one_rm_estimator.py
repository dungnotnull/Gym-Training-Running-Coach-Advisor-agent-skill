"""
1RM Estimator Tool

Based on research:
- Epley formula for estimating 1RM from submaximal reps
- Brzycki formula alternative
- ACSM guidelines for testing protocols

References:
- Epley, B. (1985). Weight training for strength and fitness.
- Brzycki, M. (1993). Strength testing: Predicting a person's one-rep max.
- LeSuer, D. A., et al. (1997). Accuracy of prediction equations.
"""

from typing import Dict, Any, Optional
import math


def estimate_1rm(weight: float, reps: int, formula: str = "epley") -> Dict[str, Any]:
    """
    Estimate 1RM from submaximal set using Epley or Brzycki formula.

    Args:
        weight: Weight lifted (lbs or kg)
        reps: Repetitions completed (must be <10 for accuracy)
        formula: "epley" or "brzycki"

    Returns:
        Dict with estimated_1rm, confidence_level, and recommendations
    """
    if reps <= 0:
        raise ValueError("Reps must be greater than 0")
    if reps >= 10:
        raise ValueError("Estimates less accurate for 10+ reps. Use lighter weight.")

    if formula == "epley":
        # Epley formula: 1RM = weight × (1 + reps/30)
        estimated_1rm = weight * (1 + reps / 30.0)
        confidence = "high" if reps <= 5 else "moderate"
    elif formula == "brzycki":
        # Brzycki formula: 1RM = weight × 36 / (37 - reps)
        estimated_1rm = weight * (36.0 / (37 - reps))
        confidence = "high" if reps <= 5 else "moderate"
    else:
        raise ValueError(f"Unknown formula: {formula}")

    return {
        "estimated_1rm": round(estimated_1rm, 2),
        "formula_used": formula,
        "confidence_level": confidence,
        "based_on": {"weight": weight, "reps": reps},
        "validity_range": "Best for reps 2-8",
        "recommendation": "Test with heavier weight if reps >8 for more accuracy"
    }


def calculate_training_percentages(estimated_1rm: float) -> Dict[str, float]:
    """
    Calculate training percentages based on ACSM guidelines.

    Research: ACSM (2009) position stand on progression models.

    Args:
        estimated_1rm: Estimated or tested 1RM

    Returns:
        Dict of training zones with percentages
    """
    return {
        "warmup": round(estimated_1rm * 0.50, 2),
        "hypertrophy_low": round(estimated_1rm * 0.65, 2),
        "hypertrophy_high": round(estimated_1rm * 0.75, 2),
        "strength_low": round(estimated_1rm * 0.80, 2),
        "strength_high": round(estimated_1rm * 0.90, 2),
        "peaking": round(estimated_1rm * 0.95, 2)
    }


def generate_progression_plan(
    current_weight: float,
    current_reps: int,
    target_reps: int,
    weeks: int = 8
) -> Dict[str, Any]:
    """
    Generate progressive overload plan based on Rhea et al. (2003).

    Research: Rhea et al. found 2-10% increases per session optimal.

    Args:
        current_weight: Current working weight
        current_reps: Current reps achieved
        target_reps: Target reps to achieve
        weeks: Duration of progression block

    Returns:
        Dict with weekly progression plan
    """
    estimated_1rm = estimate_1rm(current_weight, current_reps)

    # Calculate starting percentage
    start_percentage = (current_weight / estimated_1rm["estimated_1rm"]) * 100

    # Weekly progression: 2.5% increase (conservative per Rhea)
    weekly_increase = 0.025

    progression_plan = {
        "estimated_1rm": estimated_1rm["estimated_1rm"],
        "start_weight": current_weight,
        "start_percentage": round(start_percentage, 1),
        "target_reps": target_reps,
        "duration_weeks": weeks,
        "weekly_progression": []
    }

    current_weight_progression = current_weight

    for week in range(1, weeks + 1):
        week_weight = current_weight_progression
        week_percentage = (week_weight / estimated_1rm["estimated_1rm"]) * 100

        progression_plan["weekly_progression"].append({
            "week": week,
            "weight": round(week_weight, 2),
            "percentage_of_1rm": round(week_percentage, 1),
            "target_reps": target_reps,
            "notes": _get_week_notes(week, week_percentage)
        })

        # Increase by 2.5% for next week
        current_weight_progression = estimated_1rm["estimated_1rm"] * ((week_percentage / 100) + weekly_increase)

    return progression_plan


def _get_week_notes(week: int, percentage: float) -> str:
    """Get training notes based on week and intensity."""
    if percentage < 60:
        return "Focus on technique and form"
    elif percentage < 70:
        return "Work capacity phase - build foundation"
    elif percentage < 80:
        return "Strength building phase"
    elif percentage < 90:
        return "Peak strength phase - maintain strict form"
    else:
        return "Peaking phase - reduce volume, maintain intensity"


def test_1rm_protocol(exercise_type: str = "squat") -> Dict[str, Any]:
    """
    Provide recommended 1RM testing protocol.

    Research: Based on ACSM testing guidelines.

    Args:
        exercise_type: Type of exercise being tested

    Returns:
        Dict with testing protocol steps
    """
    protocols = {
        "squat": {
            "warmup_sets": 3,
            "warmup_reps": [10, 5, 3],
            "rest_between_attempts": "3-5 minutes",
            "increment": "10-20 lbs",
            "safety_warning": "Have spotter ready for heavy sets"
        },
        "bench_press": {
            "warmup_sets": 3,
            "warmup_reps": [10, 5, 3],
            "rest_between_attempts": "3-5 minutes",
            "increment": "5-10 lbs",
            "safety_warning": "Keep shoulders retracted, feet flat on floor"
        },
        "deadlift": {
            "warmup_sets": 3,
            "warmup_reps": [5, 3, 1],
            "rest_between_attempts": "5-7 minutes",
            "increment": "10-20 lbs",
            "safety_warning": "Maintain neutral spine, don't round upper back"
        },
        "overhead_press": {
            "warmup_sets": 3,
            "warmup_reps": [8, 4, 2],
            "rest_between_attempts": "3-5 minutes",
            "increment": "5 lbs",
            "safety_warning": "Don't arch lower back, keep core tight"
        }
    }

    return protocols.get(exercise_type, protocols["squat"])