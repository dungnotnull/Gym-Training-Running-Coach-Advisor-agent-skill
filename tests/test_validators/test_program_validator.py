"""Tests for program validator."""
import pytest
from validators.program_validator import (
    validate_program,
    check_disclaimer_included
)


class TestValidateProgram:
    """Test program validation."""

    def test_validate_complete_strength_program(self):
        """Test complete strength program validates successfully."""
        program = {
            "type": "strength",
            "experience_level": "beginner",
            "weeks": [
                {"intensity_level": 0.65, "sessions": 3},
                {"intensity_level": 0.70, "sessions": 3},
                {"intensity_level": 0.75, "sessions": 3},
                {"intensity_level": 0.80, "sessions": 3}
            ]
        }
        result = validate_program(program)

        assert result["valid"] is True
        assert len(result["issues"]) == 0

    def test_validate_complete_running_program(self):
        """Test complete running program validates successfully."""
        program = {
            "type": "running",
            "experience_level": "intermediate",
            "goal": "5k",
            "weeks": [
                {"intensity_level": 0.60, "distance_km": 15},
                {"intensity_level": 0.65, "distance_km": 18},
                {"intensity_level": 0.70, "distance_km": 20}
            ]
        }
        result = validate_program(program)

        assert result["valid"] is True

    def test_validate_missing_type_field(self):
        """Test program without type field fails validation."""
        program = {
            "experience_level": "beginner",
            "weeks": [{"intensity_level": 0.65}]
        }
        result = validate_program(program)

        assert result["valid"] is False
        assert any("Missing required field: type" in issue for issue in result["issues"])

    def test_validate_missing_experience_level(self):
        """Test program without experience_level fails validation."""
        program = {
            "type": "strength",
            "weeks": [{"intensity_level": 0.65}]
        }
        result = validate_program(program)

        assert result["valid"] is False
        assert any("Missing required field: experience_level" in issue for issue in result["issues"])

    def test_validate_missing_weeks(self):
        """Test program without weeks fails validation."""
        program = {
            "type": "strength",
            "experience_level": "beginner"
        }
        result = validate_program(program)

        assert result["valid"] is False
        assert any("Program has no weeks" in issue for issue in result["issues"])

    def test_validate_empty_weeks_list(self):
        """Test program with empty weeks list fails validation."""
        program = {
            "type": "strength",
            "experience_level": "beginner",
            "weeks": []
        }
        result = validate_program(program)

        assert result["valid"] is False
        assert any("Program has no weeks" in issue for issue in result["issues"])

    def test_validate_no_intensity_progression(self):
        """Test program with no intensity progression is flagged."""
        program = {
            "type": "strength",
            "experience_level": "beginner",
            "weeks": [
                {"intensity_level": 0.70, "sessions": 3},
                {"intensity_level": 0.70, "sessions": 3}
            ]
        }
        result = validate_program(program)

        assert result["valid"] is False
        assert any("No intensity progression detected" in issue for issue in result["issues"])

    def test_validate_single_week_program(self):
        """Test single-week program doesn't require progression check."""
        program = {
            "type": "strength",
            "experience_level": "beginner",
            "weeks": [{"intensity_level": 0.70}]
        }
        result = validate_program(program)

        # Single week should be valid even without progression
        assert result["valid"] is True
        assert len(result["issues"]) == 0

    def test_validate_multiple_issues(self):
        """Test program with multiple validation issues."""
        program = {
            "type": "strength"
            # Missing experience_level and weeks
        }
        result = validate_program(program)

        assert result["valid"] is False
        assert len(result["issues"]) >= 2

    def test_validate_with_warnings(self):
        """Test validation returns warnings list (even if empty)."""
        program = {
            "type": "strength",
            "experience_level": "beginner",
            "weeks": [
                {"intensity_level": 0.65},
                {"intensity_level": 0.80}
            ]
        }
        result = validate_program(program)

        assert "warnings" in result
        assert isinstance(result["warnings"], list)

    def test_validate_progressive_increase(self):
        """Test program with proper progressive increase validates."""
        program = {
            "type": "running",
            "experience_level": "intermediate",
            "weeks": [
                {"intensity_level": 0.60},
                {"intensity_level": 0.65},
                {"intensity_level": 0.70},
                {"intensity_level": 0.75},
                {"intensity_level": 0.80}
            ]
        }
        result = validate_program(program)

        assert result["valid"] is True
        assert len(result["issues"]) == 0


class TestCheckDisclaimerIncluded:
    """Test disclaimer inclusion checking."""

    def test_check_disclaimer_included_true(self):
        """Test program with disclaimer_included=True returns True."""
        program = {
            "type": "strength",
            "disclaimer_included": True
        }
        result = check_disclaimer_included(program)

        assert result is True

    def test_check_disclaimer_included_false(self):
        """Test program with disclaimer_included=False returns False."""
        program = {
            "type": "strength",
            "disclaimer_included": False
        }
        result = check_disclaimer_included(program)

        assert result is False

    def test_check_disclaimer_included_missing(self):
        """Test program without disclaimer_included returns False."""
        program = {
            "type": "strength"
        }
        result = check_disclaimer_included(program)

        assert result is False

    def test_check_disclaimer_included_with_various_types(self):
        """Test disclaimer check with different program types."""
        program_types = ["strength", "running", "recovery", "general"]

        for program_type in program_types:
            program = {
                "type": program_type,
                "disclaimer_included": True
            }
            result = check_disclaimer_included(program)
            assert result is True, f"Failed for program type: {program_type}"
