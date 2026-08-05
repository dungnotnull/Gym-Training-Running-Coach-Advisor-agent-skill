"""Safety checker for training programs."""
from typing import Dict, Any, List


def check_program_safety(program: Dict) -> Dict[str, Any]:
    """Check program for safety concerns.

    Args:
        program: Training program dict with experience_level and weeks

    Returns:
        Dict with 'safe' boolean and list of 'issues'
    """
    issues = []

    experience_level = program.get("experience_level")
    weeks = program.get("weeks", [])

    # Check if beginner has high intensity sessions
    if experience_level == "beginner":
        for week in weeks:
            intensity = week.get("intensity_level", 0)
            if intensity > 0.85:
                issues.append(
                    f"High intensity for beginner: {intensity:.2f} exceeds 0.85 threshold"
                )

    return {
        "safe": len(issues) == 0,
        "issues": issues
    }


def validate_medical_clearance(flags: List[str]) -> Dict:
    """Validate if user has medical clearance for training.

    Args:
        flags: List of safety flags from user input

    Returns:
        Dict with 'cleared' boolean and optional 'requires' field
    """
    if "medical_concern" in flags:
        return {
            "cleared": False,
            "requires": "physician consultation"
        }

    return {"cleared": True}
