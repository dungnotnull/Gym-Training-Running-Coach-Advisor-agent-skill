"""Tests for safety checker validator."""
import pytest
from validators.safety_checker import (
    check_program_safety,
    validate_medical_clearance
)


class TestCheckProgramSafety:
    """Test program safety checking."""

    def test_check_program_safe_program(self):
        """Test safe program returns safe=True."""
        program = {
            "experience_level": "beginner",
            "weeks": [
                {"intensity_level": 0.60},
                {"intensity_level": 0.65}
            ]
        }
        result = check_program_safety(program)

        assert result["safe"] is True
        assert len(result["issues"]) == 0

    def test_check_program_high_intensity_beginner(self):
        """Test beginner with high intensity is flagged."""
        program = {
            "experience_level": "beginner",
            "weeks": [
                {"intensity_level": 0.90}
            ]
        }
        result = check_program_safety(program)

        assert result["safe"] is False
        assert len(result["issues"]) > 0
        assert any("High intensity" in issue for issue in result["issues"])

    def test_check_program_advanced_high_intensity(self):
        """Test advanced athlete can handle high intensity."""
        program = {
            "experience_level": "advanced",
            "weeks": [
                {"intensity_level": 0.90},
                {"intensity_level": 0.95}
            ]
        }
        result = check_program_safety(program)

        # Advanced athletes can handle high intensity
        assert result["safe"] is True

    def test_check_program_intermediate_threshold(self):
        """Test intermediate athlete intensity threshold."""
        program = {
            "experience_level": "intermediate",
            "weeks": [
                {"intensity_level": 0.87}
            ]
        }
        result = check_program_safety(program)

        # Intermediate should be safe up to ~85-90%
        assert result["safe"] is True

    def test_check_program_no_experience_level(self):
        """Test program without experience level defaults to safe."""
        program = {
            "weeks": [{"intensity_level": 0.90}]
        }
        result = check_program_safety(program)

        # Should default to safe if no experience level specified
        assert result["safe"] is True

    def test_check_program_no_weeks(self):
        """Test program without weeks is safe."""
        program = {"experience_level": "beginner"}
        result = check_program_safety(program)

        assert result["safe"] is True

    def test_check_program_multiple_issues(self):
        """Test multiple safety issues are captured."""
        program = {
            "experience_level": "beginner",
            "weeks": [
                {"intensity_level": 0.90},
                {"intensity_level": 0.92},
                {"intensity_level": 0.95}
            ]
        }
        result = check_program_safety(program)

        assert result["safe"] is False
        # Should flag each high intensity week
        assert len(result["issues"]) >= 1


class TestValidateMedicalClearance:
    """Test medical clearance validation."""

    def test_validate_medical_clearance_no_concerns(self):
        """Test clearance with no medical concerns."""
        flags = []
        result = validate_medical_clearance(flags)

        assert result["cleared"] is True
        assert "requires" not in result

    def test_validate_medical_clearance_with_medical_concern(self):
        """Test medical concern flag requires physician consultation."""
        flags = ["medical_concern"]
        result = validate_medical_clearance(flags)

        assert result["cleared"] is False
        assert result["requires"] == "physician consultation"

    def test_validate_medical_clearance_with_injury_only(self):
        """Test injury flag alone doesn't require physician."""
        flags = ["injury"]
        result = validate_medical_clearance(flags)

        assert result["cleared"] is True

    def test_validate_medical_clearance_medical_and_injury(self):
        """Test medical concern with injury still requires physician."""
        flags = ["medical_concern", "injury"]
        result = validate_medical_clearance(flags)

        assert result["cleared"] is False
        assert result["requires"] == "physician consultation"

    def test_validate_medical_clearance_other_flags(self):
        """Test other safety flags don't require physician."""
        flags = ["recovery_concern", "injury"]
        result = validate_medical_clearance(flags)

        assert result["cleared"] is True
