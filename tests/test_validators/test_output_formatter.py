"""Tests for output formatter."""
import pytest
from datetime import datetime
from validators.output_formatter import (
    format_program_output,
    _get_safety_warnings,
    _get_next_steps,
    _get_timestamp
)


class TestFormatProgramOutput:
    """Test program output formatting."""

    def test_format_program_output_basic(self):
        """Test basic program output formatting."""
        program = {"type": "strength", "experience_level": "beginner"}
        analysis = {"experience_level": "beginner", "goal": "strength"}
        result = format_program_output(program, analysis)

        assert "disclaimer" in result
        assert "user_analysis" in result
        assert "safety_warnings" in result
        assert "next_steps" in result
        assert "generated_at" in result
        assert "program" in result

    def test_format_program_output_disclaimer_text(self):
        """Test disclaimer contains required text."""
        program = {"type": "strength"}
        analysis = {"experience_level": "beginner"}
        result = format_program_output(program, analysis)

        expected_text = "This program is general information only. Consult a physician before starting."
        assert expected_text in result["disclaimer"]

    def test_format_program_output_user_analysis_structure(self):
        """Test user analysis contains expected fields."""
        program = {"type": "running"}
        analysis = {
            "experience_level": "intermediate",
            "goal": "5k",
            "constraints": {"days_per_week": 4},
            "flags": ["injury"]
        }
        result = format_program_output(program, analysis)

        user_analysis = result["user_analysis"]
        assert user_analysis["experience_level"] == "intermediate"
        assert user_analysis["goal"] == "5k"
        assert user_analysis["constraints"] == {"days_per_week": 4}
        assert user_analysis["flags"] == ["injury"]

    def test_format_program_output_no_constraints(self):
        """Test formatting with no constraints."""
        program = {"type": "recovery"}
        analysis = {"experience_level": "beginner", "goal": "recovery"}
        result = format_program_output(program, analysis)

        assert result["user_analysis"]["constraints"] == {}

    def test_format_program_output_no_flags(self):
        """Test formatting with no safety flags."""
        program = {"type": "strength"}
        analysis = {"experience_level": "advanced", "goal": "strength"}
        result = format_program_output(program, analysis)

        assert result["user_analysis"]["flags"] == []

    def test_format_program_output_generated_at_format(self):
        """Test generated_at is ISO format timestamp."""
        program = {"type": "strength"}
        analysis = {"experience_level": "beginner"}
        result = format_program_output(program, analysis)

        # Should be parseable as ISO format datetime
        datetime.fromisoformat(result["generated_at"])

    def test_format_program_output_preserves_program(self):
        """Test original program is preserved in output."""
        program = {
            "type": "strength",
            "experience_level": "beginner",
            "weeks": [
                {"intensity_level": 0.65, "sessions": 3},
                {"intensity_level": 0.70, "sessions": 3}
            ]
        }
        analysis = {"experience_level": "beginner", "goal": "strength"}
        result = format_program_output(program, analysis)

        assert result["program"] == program


class TestGetSafetyWarnings:
    """Test safety warnings generation."""

    def test_get_safety_warnings_medical_concern(self):
        """Test medical concern flag generates warning."""
        flags = ["medical_concern"]
        warnings = _get_safety_warnings(flags)

        assert len(warnings) > 0
        assert any("Medical concern" in warning for warning in warnings)
        assert any("physician" in warning.lower() for warning in warnings)

    def test_get_safety_warnings_injury(self):
        """Test injury flag generates warning."""
        flags = ["injury"]
        warnings = _get_safety_warnings(flags)

        assert len(warnings) > 0
        assert any("Injury" in warning for warning in warnings)
        assert any("medical" in warning.lower() for warning in warnings)

    def test_get_safety_warnings_recovery_concern(self):
        """Test recovery concern flag generates warning."""
        flags = ["recovery_concern"]
        warnings = _get_safety_warnings(flags)

        assert len(warnings) > 0
        assert any("Recovery concern" in warning for warning in warnings)
        assert any("deload" in warning.lower() for warning in warnings)

    def test_get_safety_warnings_multiple_flags(self):
        """Test multiple flags generate multiple warnings."""
        flags = ["medical_concern", "injury", "recovery_concern"]
        warnings = _get_safety_warnings(flags)

        assert len(warnings) >= 3

    def test_get_safety_warnings_no_flags(self):
        """Test no flags returns empty warnings list."""
        flags = []
        warnings = _get_safety_warnings(flags)

        assert len(warnings) == 0

    def test_get_safety_warnings_unknown_flag(self):
        """Test unknown flags don't generate warnings."""
        flags = ["unknown_flag", "another_unknown"]
        warnings = _get_safety_warnings(flags)

        assert len(warnings) == 0

    def test_get_safety_warnings_mixed_flags(self):
        """Test mix of known and unknown flags."""
        flags = ["medical_concern", "unknown_flag", "injury"]
        warnings = _get_safety_warnings(flags)

        # Should only generate warnings for known flags
        assert len(warnings) >= 2
        assert len(warnings) <= 2  # Only medical_concern and injury


class TestGetNextSteps:
    """Test next steps generation."""

    def test_get_next_steps_returns_list(self):
        """Test next steps returns a list."""
        program = {"type": "strength"}
        steps = _get_next_steps(program)

        assert isinstance(steps, list)

    def test_get_next_steps_content(self):
        """Test next steps contain expected guidance."""
        program = {"type": "strength"}
        steps = _get_next_steps(program)

        assert len(steps) > 0
        assert any("review" in step.lower() for step in steps)
        assert any("warm-up" in step.lower() for step in steps)

    def test_get_next_steps_independent_of_program_type(self):
        """Test next steps are consistent across program types."""
        program_types = ["strength", "running", "recovery", "general"]

        steps_set = set()
        for program_type in program_types:
            program = {"type": program_type}
            steps = _get_next_steps(program)
            steps_set.add(tuple(steps))

        # All program types should return same steps
        assert len(steps_set) == 1


class TestGetTimestamp:
    """Test timestamp generation."""

    def test_get_timestamp_returns_string(self):
        """Test timestamp returns a string."""
        timestamp = _get_timestamp()

        assert isinstance(timestamp, str)

    def test_get_timestamp_iso_format(self):
        """Test timestamp is in ISO format."""
        timestamp = _get_timestamp()

        # Should be parseable as ISO format datetime
        datetime.fromisoformat(timestamp)

    def test_get_timestamp_current_time(self):
        """Test timestamp represents current time."""
        before = datetime.now()
        timestamp = _get_timestamp()
        after = datetime.now()

        parsed_time = datetime.fromisoformat(timestamp)

        # Should be between before and after (within reasonable margin)
        assert before <= parsed_time
        assert parsed_time <= after

    def test_get_timestamp_unique_values(self):
        """Test timestamps contain time information."""
        timestamp = _get_timestamp()

        # Timestamp should contain date and time components
        assert "T" in timestamp  # ISO format separator
        assert len(timestamp) > 10  # Should have more than just date
