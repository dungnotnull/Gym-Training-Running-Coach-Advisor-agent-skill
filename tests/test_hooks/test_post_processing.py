"""
Tests for Post-Processing Hooks

Research-based testing for program validation and formatting.
Based on ACSM program validation requirements and safety compliance.
"""

import pytest
from hooks.post_processing import (
    PostProcessingHooks,
    validate_program_completeness,
    apply_safety_compliance_checks,
    format_output_with_disclaimers,
    check_for_progressive_overload,
    verify_recovery_included
)


class TestPostProcessingHooks:
    """Test post-processing hooks system."""

    def test_hooks_initialization(self):
        """Test that hooks system initializes correctly."""
        hooks = PostProcessingHooks()
        assert "after_program_generation" in hooks.hooks
        assert hooks.enabled is True

    def test_register_hook(self):
        """Test registering a new hook function."""
        hooks = PostProcessingHooks()
        def dummy_hook(context):
            return {"status": "success"}

        result = hooks.register_hook("after_program_generation", dummy_hook)
        assert result is True

    def test_execute_hooks_returns_results(self):
        """Test that hook execution returns results."""
        hooks = PostProcessingHooks()
        def dummy_hook(context):
            return {"status": "success"}

        hooks.register_hook("after_program_generation", dummy_hook)
        result = hooks.execute_hooks("after_program_generation", {})
        assert "results" in result

    def test_all_passed_with_all_successes(self):
        """Test that all_passed is True when all hooks succeed."""
        hooks = PostProcessingHooks()
        def success_hook(context):
            return {"status": "success"}

        hooks.register_hook("after_program_generation", success_hook)
        hooks.register_hook("after_program_generation", success_hook)

        result = hooks.execute_hooks("after_program_generation", {})
        assert result["all_passed"] is True

    def test_all_passed_with_one_failure(self):
        """Test that all_passed is False when one hook fails."""
        hooks = PostProcessingHooks()
        def success_hook(context):
            return {"status": "success"}
        def fail_hook(context):
            return {"status": "failed"}

        hooks.register_hook("after_program_generation", success_hook)
        hooks.register_hook("after_program_generation", fail_hook)

        result = hooks.execute_hooks("after_program_generation", {})
        assert result["all_passed"] is False

    def test_disabled_hooks_skip_execution(self):
        """Test that disabled hooks skip execution."""
        hooks = PostProcessingHooks()
        hooks.enabled = False

        result = hooks.execute_hooks("after_program_generation", {})
        assert result["status"] == "disabled"


class TestValidateProgramCompleteness:
    """Test program completeness validation."""

    def test_complete_program_passes(self):
        """Test that complete program passes validation."""
        program = {
            "type": "strength",
            "experience_level": "intermediate",
            "goal": "strength",
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [
                                {"name": "squat", "sets": 3, "reps": 10}
                            ]
                        }
                    ]
                }
            ]
        }
        context = {"program": program}
        result = validate_program_completeness(context)
        assert result["status"] == "success"

    def test_program_missing_type_fails(self):
        """Test that program without type fails."""
        program = {"weeks": []}
        context = {"program": program}
        result = validate_program_completeness(context)
        assert result["status"] == "failed"

    def test_program_missing_weeks_fails(self):
        """Test that program without weeks fails."""
        program = {
            "type": "strength",
            "experience_level": "intermediate"
        }
        context = {"program": program}
        result = validate_program_completeness(context)
        assert result["status"] == "failed"

    def test_program_with_empty_weeks_fails(self):
        """Test that program with empty weeks list fails."""
        program = {
            "type": "strength",
            "weeks": []
        }
        context = {"program": program}
        result = validate_program_completeness(context)
        assert result["status"] == "failed"

    def test_includes_issues_on_failure(self):
        """Test that validation includes issues on failure."""
        program = {"type": "strength"}
        context = {"program": program}
        result = validate_program_completeness(context)
        assert "issues" in result
        assert len(result["issues"]) > 0


class TestApplySafetyComplianceChecks:
    """Test safety compliance checks."""

    def test_safe_program_passes(self):
        """Test that safe program passes compliance."""
        program = {
            "type": "strength",
            "weeks": [
                {
                    "week_number": 1,
                    "intensity_level": 0.70,
                    "sessions": [{"exercises": [{"sets": 3, "reps": 10}]}]
                }
            ]
        }
        analysis = {"flags": []}
        context = {"program": program, "analysis": analysis}
        result = apply_safety_compliance_checks(context)
        assert result["status"] == "success"
        assert result["safety_check"] == "passed"

    def test_program_with_safety_issues_returns_warning(self):
        """Test that program with safety issues returns warning."""
        program = {
            "type": "strength",
            "weeks": [
                {
                    "week_number": 1,
                    "intensity_level": 0.95,  # Too high for most
                    "sessions": []
                }
            ]
        }
        analysis = {"flags": []}
        context = {"program": program, "analysis": analysis}
        result = apply_safety_compliance_checks(context)
        assert result["status"] in ["warning", "critical"]

    def test_medical_flag_requires_clearance(self):
        """Test that medical flag requires clearance."""
        program = {"type": "strength", "weeks": [{"week_number": 1}]}
        analysis = {"flags": ["medical_concern"]}
        context = {"program": program, "analysis": analysis}
        result = apply_safety_compliance_checks(context)
        assert result["status"] == "critical"
        assert result["program_blocked"] is True

    def test_includes_recommendation_for_warning(self):
        """Test that warning includes recommendation."""
        program = {"type": "strength", "weeks": [{"week_number": 1, "intensity_level": 0.95}]}
        analysis = {"flags": []}
        context = {"program": program, "analysis": analysis}
        result = apply_safety_compliance_checks(context)
        if result.get("status") == "warning":
            assert "recommendation" in result


class TestFormatOutputWithDisclaimers:
    """Test output formatting with disclaimers."""

    def test_formats_program_output(self):
        """Test that program output is formatted."""
        program = {
            "type": "strength",
            "experience_level": "intermediate",
            "weeks": [{"week_number": 1}]
        }
        analysis = {"goal": "strength"}
        context = {"program": program, "analysis": analysis}
        result = format_output_with_disclaimers(context)
        assert result["status"] == "success"
        assert "formatted_output" in result

    def test_includes_compliance_checks(self):
        """Test that formatted output includes compliance."""
        program = {"type": "strength", "weeks": []}
        analysis = {"goal": "strength"}
        context = {"program": program, "analysis": analysis}
        result = format_output_with_disclaimers(context)
        formatted = result["formatted_output"]
        assert "compliance" in formatted
        assert formatted["compliance"]["validated"] is True
        assert formatted["compliance"]["safety_checked"] is True
        assert formatted["compliance"]["disclaimer_acknowledged"] is True

    def test_includes_disclaimer_in_output(self):
        """Test that disclaimer is included in output."""
        program = {"type": "strength", "weeks": []}
        analysis = {"goal": "strength"}
        context = {"program": program, "analysis": analysis}
        result = format_output_with_disclaimers(context)
        formatted = result["formatted_output"]
        # Should have some form of disclaimer
        assert "disclaimer" in str(formatted).lower() or "warning" in str(formatted).lower()


class TestCheckForProgressiveOverload:
    """Test progressive overload verification."""

    def test_program_with_progression_passes(self):
        """Test that program with progression passes."""
        program = {
            "weeks": [
                {"week_number": 1, "intensity_level": 0.65},
                {"week_number": 2, "intensity_level": 0.70},
                {"week_number": 3, "intensity_level": 0.75}
            ]
        }
        context = {"program": program}
        result = check_for_progressive_overload(context)
        assert result["status"] == "success"
        assert result["progression_verified"] is True

    def test_program_without_progression_returns_warning(self):
        """Test that program without progression returns warning."""
        program = {
            "weeks": [
                {"week_number": 1, "intensity_level": 0.70},
                {"week_number": 2, "intensity_level": 0.70},
                {"week_number": 3, "intensity_level": 0.70}
            ]
        }
        context = {"program": program}
        result = check_for_progressive_overload(context)
        assert result["status"] == "warning"
        assert "recommendation" in result

    def test_single_week_program_returns_warning(self):
        """Test that single week program returns warning."""
        program = {
            "weeks": [
                {"week_number": 1, "intensity_level": 0.70}
            ]
        }
        context = {"program": program}
        result = check_for_progressive_overload(context)
        assert result["status"] == "warning"

    def test_includes_recommendation_to_add_progression(self):
        """Test that recommendation includes adding progression."""
        program = {
            "weeks": [
                {"week_number": 1, "intensity_level": 0.70},
                {"week_number": 2, "intensity_level": 0.70}
            ]
        }
        context = {"program": program}
        result = check_for_progressive_overload(context)
        assert "progressive overload" in str(result["recommendation"]).lower()


class TestVerifyRecoveryIncluded:
    """Test recovery verification."""

    def test_program_with_deloads_passes(self):
        """Test that program with deloads passes."""
        program = {
            "weeks": [
                {"week_number": 1, "is_deload": False},
                {"week_number": 2, "is_deload": False},
                {"week_number": 3, "is_deload": False},
                {"week_number": 4, "is_deload": True}
            ]
        }
        context = {"program": program}
        result = verify_recovery_included(context)
        assert result["status"] == "success"
        assert result["recovery_verified"] is True

    def test_short_program_without_deloads_passes(self):
        """Test that short programs (4 weeks or less) pass without deloads."""
        program = {
            "weeks": [
                {"week_number": 1, "is_deload": False},
                {"week_number": 2, "is_deload": False},
                {"week_number": 3, "is_deload": False},
                {"week_number": 4, "is_deload": False}
            ]
        }
        context = {"program": program}
        result = verify_recovery_included(context)
        assert result["status"] == "success"

    def test_long_program_without_deloads_fails(self):
        """Test that long programs without deloads fail."""
        program = {
            "weeks": [
                {"week_number": i, "is_deload": False}
                for i in range(1, 9)  # 8 weeks
            ]
        }
        context = {"program": program}
        result = verify_recovery_included(context)
        assert result["status"] == "warning"

    def test_includes_deload_count(self):
        """Test that result includes deload count."""
        program = {
            "weeks": [
                {"week_number": 1, "is_deload": False},
                {"week_number": 2, "is_deload": False},
                {"week_number": 3, "is_deload": False},
                {"week_number": 4, "is_deload": True}
            ]
        }
        context = {"program": program}
        result = verify_recovery_included(context)
        assert "deload_count" in result
        assert result["deload_count"] == 1

    def test_includes_recommendation_to_add_deloads(self):
        """Test that recommendation includes adding deloads."""
        program = {
            "weeks": [
                {"week_number": i, "is_deload": False}
                for i in range(1, 9)
            ]
        }
        context = {"program": program}
        result = verify_recovery_included(context)
        if result.get("status") == "warning":
            assert "deload" in str(result["recommendation"]).lower()

    def test_multiple_deloads_pass(self):
        """Test that multiple deloads pass."""
        program = {
            "weeks": [
                {"week_number": 1, "is_deload": False},
                {"week_number": 2, "is_deload": False},
                {"week_number": 3, "is_deload": False},
                {"week_number": 4, "is_deload": True},
                {"week_number": 5, "is_deload": False},
                {"week_number": 6, "is_deload": False},
                {"week_number": 7, "is_deload": False},
                {"week_number": 8, "is_deload": True}
            ]
        }
        context = {"program": program}
        result = verify_recovery_included(context)
        assert result["status"] == "success"
        assert result["deload_count"] == 2
