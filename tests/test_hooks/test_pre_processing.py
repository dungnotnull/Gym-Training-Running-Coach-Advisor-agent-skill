"""
Tests for Pre-Processing Hooks

Research-based testing for input validation and safety checks.
Based on ACSM guidelines for exercise prescription.
"""

import pytest
from hooks.pre_processing import (
    PreProcessingHooks,
    validate_input_completeness,
    check_medical_clearance_flags,
    detect_contradictions
)


class TestPreProcessingHooks:
    """Test pre-processing hooks system."""

    def test_hooks_initialization(self):
        """Test that hooks system initializes correctly."""
        hooks = PreProcessingHooks()
        assert "before_program_generation" in hooks.hooks
        assert hooks.enabled is True

    def test_register_hook(self):
        """Test registering a new hook function."""
        hooks = PreProcessingHooks()
        def dummy_hook(context):
            return {"status": "success"}

        result = hooks.register_hook("before_program_generation", dummy_hook)
        assert result is True

    def test_register_hook_invalid_name(self):
        """Test registering hook with invalid name returns False."""
        hooks = PreProcessingHooks()
        def dummy_hook(context):
            return {"status": "success"}

        result = hooks.register_hook("invalid_hook_name", dummy_hook)
        assert result is False

    def test_execute_hooks_returns_results(self):
        """Test that hook execution returns results."""
        hooks = PreProcessingHooks()
        def dummy_hook(context):
            return {"status": "success"}

        hooks.register_hook("before_program_generation", dummy_hook)
        result = hooks.execute_hooks("before_program_generation", {})
        assert "results" in result
        assert len(result["results"]) > 0

    def test_execute_hooks_all_passed_flag(self):
        """Test that all_passed flag works correctly."""
        hooks = PreProcessingHooks()
        def success_hook(context):
            return {"status": "success"}

        def fail_hook(context):
            return {"status": "failed"}

        hooks.register_hook("before_program_generation", success_hook)
        hooks.register_hook("before_program_generation", fail_hook)

        result = hooks.execute_hooks("before_program_generation", {})
        assert result["all_passed"] is False

    def test_disabled_hooks_skip_execution(self):
        """Test that disabled hooks skip execution."""
        hooks = PreProcessingHooks()
        hooks.enabled = False

        result = hooks.execute_hooks("before_program_generation", {})
        assert result["status"] == "disabled"

    def test_hooks_handle_exceptions_gracefully(self):
        """Test that hooks handle exceptions gracefully."""
        hooks = PreProcessingHooks()
        def error_hook(context):
            raise ValueError("Test error")

        hooks.register_hook("before_program_generation", error_hook)
        result = hooks.execute_hooks("before_program_generation", {})
        # Should return error in results instead of raising
        assert "error" in result["results"][0]


class TestValidateInputCompleteness:
    """Test input completeness validation."""

    def test_complete_input_passes(self):
        """Test that complete input passes validation."""
        user_input = "I'm an intermediate lifter looking to build strength"
        result = validate_input_completeness(user_input, {})
        assert result["status"] == "success"
        assert result["experience_detected"] is True
        assert result["goal_detected"] is True

    def test_missing_experience_level_fails(self):
        """Test that missing experience level fails."""
        user_input = "I want to get stronger"
        result = validate_input_completeness(user_input, {})
        assert result["status"] == "failed"
        assert "experience" in result["message"].lower()

    def test_missing_goal_fails(self):
        """Test that missing goal fails."""
        user_input = "I'm an intermediate lifter"
        result = validate_input_completeness(user_input, {})
        assert result["status"] == "failed"
        assert "goal" in result["message"].lower()

    def test_detects_beginner_experience(self):
        """Test detection of beginner experience."""
        user_input = "I'm a beginner just starting"
        result = validate_input_completeness(user_input, {})
        assert result["experience_detected"] is True

    def test_detects_intermediate_experience(self):
        """Test detection of intermediate experience."""
        user_input = "I have some experience with training"
        result = validate_input_completeness(user_input, {})
        assert result["experience_detected"] is True

    def test_detects_advanced_experience(self):
        """Test detection of advanced experience."""
        user_input = "I've been training for years"
        result = validate_input_completeness(user_input, {})
        assert result["experience_detected"] is True

    def test_detects_strength_goal(self):
        """Test detection of strength goal."""
        user_input = "I want to get stronger and improve my squat"
        result = validate_input_completeness(user_input, {})
        assert result["goal_detected"] is True

    def test_detects_muscle_goal(self):
        """Test detection of muscle/hypertrophy goal."""
        user_input = "I want to build muscle and mass"
        result = validate_input_completeness(user_input, {})
        assert result["goal_detected"] is True

    def test_detects_running_goal(self):
        """Test detection of running goal."""
        user_input = "I want to run a 5k race"
        result = validate_input_completeness(user_input, {})
        assert result["goal_detected"] is True

    def test_detects_marathon_goal(self):
        """Test detection of marathon goal."""
        user_input = "I'm training for a marathon"
        result = validate_input_completeness(user_input, {})
        assert result["goal_detected"] is True

    def test_detects_general_fitness_goal(self):
        """Test detection of general fitness goal."""
        user_input = "I want to improve my general fitness"
        result = validate_input_completeness(user_input, {})
        assert result["goal_detected"] is True


class TestCheckMedicalClearanceFlags:
    """Test medical clearance flag checking."""

    def test_no_flags_returns_success(self):
        """Test that no flags returns success."""
        analysis = {"flags": [], "raw_input": "I want to get stronger"}
        context = {"analysis": analysis}
        result = check_medical_clearance_flags(context)
        assert result["status"] == "success"
        assert result["clearance"] == "not_required"

    def test_medical_concern_flag_triggers_warning(self):
        """Test that medical_concern flag triggers warning."""
        analysis = {"flags": ["medical_concern"], "raw_input": "I have a concern"}
        context = {"analysis": analysis}
        result = check_medical_clearance_flags(context)
        assert result["status"] == "warning"
        assert result["requires_clearance"] is True

    def test_heart_condition_in_input_triggers_warning(self):
        """Test that heart condition in input triggers warning."""
        analysis = {"flags": [], "raw_input": "I have a heart condition"}
        context = {"analysis": analysis}
        result = check_medical_clearance_flags(context)
        assert result["status"] == "warning"
        assert result["requires_clearance"] is True

    def test_diabetes_in_input_triggers_warning(self):
        """Test that diabetes in input triggers warning."""
        analysis = {"flags": [], "raw_input": "I have diabetes"}
        context = {"analysis": analysis}
        result = check_medical_clearance_flags(context)
        assert result["requires_clearance"] is True

    def test_asthma_in_input_triggers_warning(self):
        """Test that asthma in input triggers warning."""
        analysis = {"flags": [], "raw_input": "I have asthma"}
        context = {"analysis": analysis}
        result = check_medical_clearance_flags(context)
        assert result["requires_clearance"] is True

    def test_includes_physician_consultation_recommendation(self):
        """Test that warning includes physician consultation."""
        analysis = {"flags": ["medical_concern"], "raw_input": "medical issue"}
        context = {"analysis": analysis}
        result = check_medical_clearance_flags(context)
        assert "consult" in result["recommendation"].lower()
        assert "physician" in result["recommendation"].lower()


class TestDetectContradictions:
    """Test contradiction detection in user input."""

    def test_no_contradiction_returns_success(self):
        """Test that consistent input returns success."""
        analysis = {
            "experience_level": "beginner",
            "raw_input": "I'm new to training"
        }
        context = {"analysis": analysis}
        result = detect_contradictions(context)
        assert result["status"] == "success"
        assert result["contradictions"] is None

    def test_beginner_with_training_for_contradiction(self):
        """Test detection of beginner + 'training for' contradiction."""
        analysis = {
            "experience_level": "beginner",
            "raw_input": "I'm a beginner but I've been training for 3 years"
        }
        context = {"analysis": analysis}
        result = detect_contradictions(context)
        assert result["status"] == "warning"
        assert "contradiction" in result["message"].lower()

    def test_beginner_with_consistent_contradiction(self):
        """Test detection of beginner + consistent contradiction."""
        analysis = {
            "experience_level": "beginner",
            "raw_input": "I'm a beginner who has been consistent for months"
        }
        context = {"analysis": analysis}
        result = detect_contradictions(context)
        assert result["status"] == "warning"

    def test_beginner_with_advanced_contradiction(self):
        """Test detection of beginner + advanced contradiction."""
        analysis = {
            "experience_level": "beginner",
            "raw_input": "I'm a beginner with advanced experience"
        }
        context = {"analysis": analysis}
        result = detect_contradictions(context)
        assert result["status"] == "warning"

    def test_intermediate_no_contradiction(self):
        """Test that intermediate with reasonable input is fine."""
        analysis = {
            "experience_level": "intermediate",
            "raw_input": "I've been training for a while"
        }
        context = {"analysis": analysis}
        result = detect_contradictions(context)
        assert result["status"] == "success"

    def test_includes_action_for_contradiction(self):
        """Test that contradiction includes action to resolve."""
        analysis = {
            "experience_level": "beginner",
            "raw_input": "I'm a beginner training for years"
        }
        context = {"analysis": analysis}
        result = detect_contradictions(context)
        assert "action" in result
        assert "clarify" in result["action"].lower()
