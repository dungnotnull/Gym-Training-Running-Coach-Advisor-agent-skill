"""Program validator for training program completeness and structure."""
from typing import Dict, Any, List, Optional


class ValidationRule:
    """Represents a single validation rule."""
    name: str
    description: str

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


def validate_program(program: Dict[str, Any]) -> Dict[str, Any]:
    """Validate training program completeness and structure.

    Checks for:
    - Required fields (type, experience_level, weeks)
    - Presence of weeks in program
    - Intensity progression across weeks (for programs with intensity_level)

    Args:
        program: Training program dict with type, experience_level, and weeks

    Returns:
        Dict with 'valid' boolean, 'issues' list, and 'warnings' list
    """
    issues: List[str] = []
    warnings: List[str] = []

    # Check required fields
    required_fields = ["type", "experience_level", "weeks"]
    for field in required_fields:
        if field not in program:
            issues.append(f"Missing required field: {field}")

    # Check weeks exist and is not empty
    weeks = program.get("weeks", [])
    if not weeks or len(weeks) == 0:
        issues.append("Program has no weeks")
    else:
        # Check for progression if more than one week and has intensity_level
        if len(weeks) > 1:
            # Only check intensity progression if weeks have intensity_level
            weeks_with_intensity = [w for w in weeks if "intensity_level" in w]

            if len(weeks_with_intensity) >= 2:
                first_intensity = weeks_with_intensity[0]["intensity_level"]
                last_intensity = weeks_with_intensity[-1]["intensity_level"]

                if first_intensity is not None and last_intensity is not None:
                    if first_intensity == last_intensity:
                        issues.append("No intensity progression detected")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings
    }


def check_disclaimer_included(program: Dict[str, Any]) -> bool:
    """Check if program includes required disclaimer.

    Args:
        program: Training program dict

    Returns:
        True if disclaimer_included is True, False otherwise
    """
    return program.get("disclaimer_included", False)
