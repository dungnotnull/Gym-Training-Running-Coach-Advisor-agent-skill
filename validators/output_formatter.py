"""Output formatter for training programs with consistent structure and disclaimers."""
from typing import Dict, Any, List
from datetime import datetime

REQUIRED_DISCLAIMER = "This program is general information only. Consult a physician before starting."


def format_program_output(program: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Format program with consistent structure and required disclaimers.

    Args:
        program: Training program dict
        analysis: User analysis dict with experience_level, goal, constraints, flags

    Returns:
        Dict with formatted structure including:
        - program: Original program
        - disclaimer: Required disclaimer text
        - user_analysis: User information
        - safety_warnings: Safety-related warnings based on flags
        - next_steps: Recommended next steps
        - generated_at: ISO timestamp
    """
    formatted = {
        "program": program,
        "disclaimer": REQUIRED_DISCLAIMER,
        "user_analysis": {
            "experience_level": analysis.get("experience_level"),
            "goal": analysis.get("goal"),
            "constraints": analysis.get("constraints", {}),
            "flags": analysis.get("flags", [])
        },
        "safety_warnings": _get_safety_warnings(analysis.get("flags", [])),
        "next_steps": _get_next_steps(program),
        "generated_at": _get_timestamp()
    }

    return formatted


def _get_safety_warnings(flags: List[str]) -> List[str]:
    """Generate safety warnings based on safety flags.

    Args:
        flags: List of safety flag strings

    Returns:
        List of safety warning messages
    """
    warnings = []

    if "medical_concern" in flags:
        warnings.append("Medical concern detected - Consult physician before starting")

    if "injury" in flags:
        warnings.append("Injury detected - Follow medical guidance")

    if "recovery_concern" in flags:
        warnings.append("Recovery concern detected - Consider deload week")

    return warnings


def _get_next_steps(program: Dict[str, Any]) -> List[str]:
    """Generate recommended next steps for starting the program.

    Args:
        program: Training program dict

    Returns:
        List of next step recommendations
    """
    return [
        "1. Review program completely before starting",
        "2. Ensure proper warm-up for each session",
        "3. Follow recommended rest intervals",
        "4. Track progress and adjust as needed"
    ]


def _get_timestamp() -> str:
    """Get current ISO format timestamp.

    Returns:
        ISO format datetime string
    """
    return datetime.now().isoformat()
