"""
Recovery Status Assessment Tool

Based on research:
- Kreher & Schwartz (2012) - Overtraining Syndrome warning signs
- Sluka et al. (2017) - Sleep requirements for athletes
- Nederhof et al. (2018) - Subjective and objective recovery markers
- Meeusen & Duclos (2004) - Acute:Chronic workload ratio

References:
- Kreher, J. B., & Schwartz, J. B. (2012). Overtraining Syndrome: A Practical Guide.
- Sluka, K. A., et al. (2017). Sleep, Recovery, and Performance in Athletes.
- Nederhof, E., et al. (2018). Monitoring Athletes' Readiness.
"""

from typing import Dict, Any, List
from enum import Enum


class RecoveryStatus(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


def determine_recovery_status(
    sleep_hours: float,
    sleep_quality: str,
    resting_hr: int,
    mood: str,
    muscle_soreness: str,
    motivation_level: str
) -> Dict[str, Any]:
    """
    Comprehensive recovery assessment based on multiple markers.

    Research: Kreher & Schwartz (2012), Sluka et al. (2017)

    Args:
        sleep_hours: Hours of sleep (target: 8-10 for athletes)
        sleep_quality: "excellent", "good", "fair", or "poor"
        resting_hr: Morning resting heart rate (check against baseline)
        mood: "energized", "good", "neutral", "fatigued", "exhausted", "irritable"
        muscle_soreness: "none", "mild", "moderate", "severe"
        motivation_level: "very_high", "high", "moderate", "low", "very_low"

    Returns:
        Dict with recovery status, recommendations, and warnings
    """
    # Assess each marker
    sleep_score = _assess_sleep(sleep_hours, sleep_quality)
    hr_score = _assess_resting_hr(resting_hr)
    mood_score = _assess_mood(mood)
    soreness_score = _assess_soreness(muscle_soreness)
    motivation_score = _assess_motivation(motivation_level)

    # Calculate overall recovery score
    scores = [sleep_score, hr_score, mood_score, soreness_score, motivation_score]
    avg_score = sum(scores) / len(scores)

    # Determine recovery status
    if avg_score >= 4.5:
        status = RecoveryStatus.EXCELLENT.value
    elif avg_score >= 3.5:
        status = RecoveryStatus.GOOD.value
    elif avg_score >= 2.5:
        status = RecoveryStatus.FAIR.value
    elif avg_score >= 1.5:
        status = RecoveryStatus.POOR.value
    else:
        status = RecoveryStatus.CRITICAL.value

    # Generate recommendations
    recommendations = _generate_recommendations(
        sleep_score, mood_score, soreness_score, motivation_score
    )

    # Check for warning signs
    warnings = _check_warning_signs(
        sleep_hours, resting_hr, mood, muscle_soreness, motivation_level
    )

    return {
        "status": status,
        "overall_score": round(avg_score, 2),
        "marker_scores": {
            "sleep": sleep_score,
            "resting_hr": hr_score,
            "mood": mood_score,
            "muscle_soreness": soreness_score,
            "motivation": motivation_score
        },
        "recommendations": recommendations,
        "warnings": warnings,
        "action_needed": status in [RecoveryStatus.POOR.value, RecoveryStatus.CRITICAL.value]
    }


def _assess_sleep(hours: float, quality: str) -> float:
    """Assess sleep quality (1-5 scale)."""
    score = 0

    # Hours assessment
    if hours >= 9:
        score += 2
    elif hours >= 7:
        score += 1
    elif hours >= 6:
        score += 0.5
    else:
        score += 0

    # Quality assessment
    quality_scores = {
        "excellent": 3,
        "good": 2,
        "fair": 1,
        "poor": 0
    }
    score += quality_scores.get(quality, 0)

    return min(score, 5)


def _assess_resting_hr(hr: int) -> float:
    """Assess resting heart rate (assumes baseline ~60)."""
    if hr <= 60:
        return 5  # Normal
    elif hr <= 65:
        return 4  # Slightly elevated
    elif hr <= 70:
        return 3  # Elevated
    elif hr <= 75:
        return 2  # Significantly elevated
    else:
        return 1  # Very elevated - poor recovery


def _assess_mood(mood: str) -> float:
    """Assess mood state (1-5 scale)."""
    mood_scores = {
        "energized": 5,
        "good": 4,
        "neutral": 3,
        "fatigued": 2,
        "exhausted": 1,
        "irritable": 1
    }
    return mood_scores.get(mood.lower(), 3)


def _assess_soreness(soreness: str) -> float:
    """Assess muscle soreness (1-5 scale)."""
    soreness_scores = {
        "none": 5,
        "mild": 4,
        "moderate": 3,
        "severe": 1
    }
    return soreness_scores.get(soreness.lower(), 3)


def _assess_motivation(motivation: str) -> float:
    """Assess motivation level (1-5 scale)."""
    motivation_scores = {
        "very_high": 5,
        "high": 4,
        "moderate": 3,
        "low": 2,
        "very_low": 1
    }
    return motivation_scores.get(motivation.lower(), 3)


def _generate_recommendations(
    sleep_score: float,
    mood_score: float,
    soreness_score: float,
    motivation_score: float
) -> List[str]:
    """Generate recovery recommendations."""
    recommendations = []

    if sleep_score < 3:
        recommendations.append("Prioritize sleep - aim for 8-10 hours")
        recommendations.append("Maintain consistent sleep schedule")

    if mood_score < 3:
        recommendations.append("Consider rest day or light activity")
        recommendations.append("Evaluate training load and life stress")

    if soreness_score <= 2:
        recommendations.append("Active recovery: light Zone 1 activity")
        recommendations.append("Foam rolling or mobility work recommended")

    if motivation_score < 3:
        recommendations.append("Reduce training volume by 20-30%")
        recommendations.append("Take 2-3 complete rest days")

    if len(recommendations) == 0:
        recommendations.append("Recovery on track - continue normal training")

    return recommendations


def _check_warning_signs(
    sleep_hours: float,
    resting_hr: int,
    mood: str,
    muscle_soreness: str,
    motivation_level: str
) -> List[str]:
    """Check for OTS warning signs."""
    warnings = []

    if sleep_hours < 6:
        warnings.append("⚠️ Sleep deprivation detected")

    if resting_hr > 70:
        warnings.append("⚠️ Elevated resting heart rate - poor recovery")

    if mood in ["exhausted", "irritable"]:
        warnings.append("⚠️ Mood change detected - monitor closely")

    if muscle_soreness == "severe":
        warnings.append("⚠️ Severe soreness - reduce intensity")

    if motivation_level in ["low", "very_low"]:
        warnings.append("⚠️ Low motivation - possible overtraining")

    # Count warnings
    if len(warnings) >= 3:
        warnings.append("🚨 MULTIPLE WARNING SIGNS - Consider deload week immediately")

    return warnings


def assess_overtraining_risk(session_data: Dict) -> Dict[str, Any]:
    """
    Assess overall overtraining risk based on session history.

    Research: Kreher & Schwartz (2012) warning signs checklist

    Args:
        session_data: Session with program history

    Returns:
        Dict with risk assessment
    """
    warning_signs = []
    program_history = session_data.get("program_history", [])

    # Check for performance decline
    if len(program_history) >= 2:
        recent = program_history[-1]
        previous = program_history[-2]
        # Would compare performance if tracked
        # For now, check iteration frequency
        if session_data.get("iteration_count", 0) > 8:
            warning_signs.append("High training frequency without deload")

    # Check for insufficient recovery
    last_analysis = session_data.get("user_profile", {})
    flags = last_analysis.get("flags", [])

    if "recovery_concern" in flags:
        warning_signs.append("Recovery concern flagged")

    if "medical_concern" in flags:
        warning_signs.append("Medical concern present")

    # Determine risk level
    risk_level = "low"
    if len(warning_signs) >= 2:
        risk_level = "moderate"
    if len(warning_signs) >= 3:
        risk_level = "high"
    if len(warning_signs) >= 4:
        risk_level = "critical"

    return {
        "risk_level": risk_level,
        "warning_signs": warning_signs,
        "recommendation": _get_risk_recommendation(risk_level)
    }


def _get_risk_recommendation(risk_level: str) -> str:
    """Get recommendation based on risk level."""
    recommendations = {
        "low": "Continue normal training with monitoring",
        "moderate": "Consider reducing training volume 10-20% and monitor",
        "high": "Implement deload week - reduce volume 50% for 1 week",
        "critical": "STOP - Take 1-2 weeks complete rest or consult physician"
    }
    return recommendations.get(risk_level, "Monitor training closely")