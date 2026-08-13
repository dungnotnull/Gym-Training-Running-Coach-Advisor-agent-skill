"""
Tests for Error Handlers

Research-based testing for error handling and fallback mechanisms.
Based on safety principles in exercise prescription.
"""

import pytest
from hooks.error_handlers import (
    ErrorHandlers,
    log_error,
    handle_input_validation_error,
    handle_safety_concern,
    handle_methodology_error,
    handle_critical_failure,
    _create_fallback_weeks,
    _get_professional_resources
)


class TestErrorHandlers:
    """Test error handlers system."""

    def test_error_handlers_initialization(self):
        """Test that error handlers initialize correctly."""
        handlers = ErrorHandlers()
        assert "on_error" in handlers.hooks
        assert handlers.enabled is True

    def test_register_hook(self):
        """Test registering a new error handler."""
        handlers = ErrorHandlers()
        def dummy_handler(context):
            return {"resolution": True}

        result = handlers.register_hook("on_error", dummy_handler)
        assert result is True

    def test_register_hook_invalid_name(self):
        """Test registering with invalid name returns False."""
        handlers = ErrorHandlers()
        def dummy_handler(context):
            return {"resolution": True}

        result = handlers.register_hook("invalid_hook", dummy_handler)
        assert result is False

    def test_execute_hooks(self):
        """Test hook execution."""
        handlers = ErrorHandlers()
        def dummy_handler(context):
            return {"resolution": False}

        handlers.register_hook("on_error", dummy_handler)
        result = handlers.execute_hooks("on_error", {})
        assert "resolution_available" in result

    def test_resolution_available_when_any_handler_resolves(self):
        """Test that resolution_available is True when any handler resolves."""
        handlers = ErrorHandlers()
        def fail_handler(context):
            return {"resolution": False}
        def resolve_handler(context):
            return {"resolution": True}

        handlers.register_hook("on_error", fail_handler)
        handlers.register_hook("on_error", resolve_handler)

        result = handlers.execute_hooks("on_error", {})
        assert result["resolution_available"] is True

    def test_disabled_handlers_skip_execution(self):
        """Test that disabled handlers skip execution."""
        handlers = ErrorHandlers()
        handlers.enabled = False

        result = handlers.execute_hooks("on_error", {})
        assert result["status"] == "disabled"

    def test_handlers_handle_exceptions_gracefully(self):
        """Test that handlers handle exceptions gracefully."""
        handlers = ErrorHandlers()
        def error_handler(context):
            raise ValueError("Test error")

        handlers.register_hook("on_error", error_handler)
        result = handlers.execute_hooks("on_error", {})
        # Should return error in results instead of raising
        assert "error" in result["results"][0]


class TestLogError:
    """Test error logging."""

    def test_log_error_creates_entry(self):
        """Test that logging creates error entry."""
        result = log_error("ValueError", {"session_id": "test-123"})
        assert result["status"] == "logged"
        assert "entry" in result

    def test_log_entry_includes_timestamp(self):
        """Test that log entry includes timestamp."""
        result = log_error("TypeError", {"session_id": "test-456"})
        assert "timestamp" in result["entry"]

    def test_log_entry_includes_error_type(self):
        """Test that log entry includes error type."""
        result = log_error("AttributeError", {"session_id": "test-789"})
        assert result["entry"]["error_type"] == "AttributeError"

    def test_log_entry_includes_session_id(self):
        """Test that log entry includes session ID."""
        result = log_error("RuntimeError", {"session_id": "test-session"})
        assert result["entry"]["session_id"] == "test-session"

    def test_log_entry_truncates_user_input(self):
        """Test that log entry truncates long user input."""
        long_input = "a" * 200
        result = log_error("Error", {"user_input": long_input, "session_id": "test"})
        # Should be truncated to 100 chars
        assert len(result["entry"]["context"]["user_input"]) <= 100


class TestHandleInputValidationError:
    """Test input validation error handling."""

    def test_input_validation_error_returns_resolution(self):
        """Test that validation error returns resolution."""
        result = handle_input_validation_error({
            "missing_information": ["experience_level", "goal"]
        })
        assert result["status"] == "resolution_available"
        assert result["resolution_type"] == "request_clarification"

    def test_includes_missing_info_list(self):
        """Test that error includes missing information list."""
        result = handle_input_validation_error({
            "missing_information": ["experience_level", "goal", "days_per_week"]
        })
        assert "required_information" in result
        assert len(result["required_information"]) == 3

    def test_includes_user_friendly_message(self):
        """Test that error includes user-friendly message."""
        result = handle_input_validation_error({
            "missing_information": ["experience_level"]
        })
        assert "message" in result
        assert "need a bit more information" in result["message"].lower()

    def test_includes_examples_for_clarification(self):
        """Test that error includes clarification examples."""
        result = handle_input_validation_error({
            "missing_information": ["experience_level"]
        })
        assert "examples" in result
        assert len(result["examples"]) > 0


class TestHandleSafetyConcern:
    """Test safety concern handling."""

    def test_medical_concern_returns_medical_type(self):
        """Test that medical concern returns medical concern type."""
        result = handle_safety_concern({
            "analysis": {"flags": ["medical_concern"]}
        })
        assert result["concern_type"] == "medical"

    def test_injury_concern_returns_injury_type(self):
        """Test that injury concern returns injury concern type."""
        result = handle_safety_concern({
            "analysis": {"flags": ["injury"]}
        })
        assert result["concern_type"] == "injury"

    def test_eating_disorder_concern_returns_eating_disorder_type(self):
        """Test that eating disorder concern returns correct type."""
        result = handle_safety_concern({
            "analysis": {"flags": ["eating_disorder_concern"]}
        })
        assert result["concern_type"] == "eating_disorder"

    def test_includes_medical_disclaimer(self):
        """Test that medical concern includes disclaimer."""
        result = handle_safety_concern({
            "analysis": {"flags": ["medical_concern"]}
        })
        assert "disclaimer" in result
        assert "not a substitute" in result["disclaimer"].lower()

    def test_includes_injury_disclaimer(self):
        """Test that injury concern includes disclaimer."""
        result = handle_safety_concern({
            "analysis": {"flags": ["injury"]}
        })
        assert "disclaimer" in result
        assert "physical therapist" in result["disclaimer"].lower()

    def test_includes_eating_disorder_resources(self):
        """Test that eating disorder includes resources."""
        result = handle_safety_concern({
            "analysis": {"flags": ["eating_disorder_concern"]}
        })
        assert "resources" in result
        assert any("neda" in r.lower() for r in result["resources"])

    def test_includes_professional_resources(self):
        """Test that concern includes professional resources."""
        result = handle_safety_concern({
            "analysis": {"flags": ["medical_concern"]}
        })
        assert "resources" in result
        assert len(result["resources"]) > 0

    def test_no_concern_flag_returns_none_type(self):
        """Test that no concern flag returns None type."""
        result = handle_safety_concern({
            "analysis": {"flags": []}
        })
        assert result["concern_type"] is None


class TestHandleMethodologyError:
    """Test methodology error handling."""

    def test_methodology_error_creates_fallback_program(self):
        """Test that methodology error creates fallback program."""
        result = handle_methodology_error({
            "error": "Test error",
            "analysis": {"experience_level": "intermediate", "goal": "general"}
        })
        assert result["status"] == "resolution_available"
        assert result["resolution_type"] == "use_fallback"
        assert "fallback_program" in result

    def test_fallback_program_has_basic_structure(self):
        """Test that fallback program has basic structure."""
        result = handle_methodology_error({
            "error": "Test error",
            "analysis": {"experience_level": "beginner", "goal": "strength"}
        })
        program = result["fallback_program"]
        assert "type" in program
        assert "weeks" in program
        assert len(program["weeks"]) > 0

    def test_fallback_program_includes_note(self):
        """Test that fallback program includes explanatory note."""
        result = handle_methodology_error({
            "error": "Test error",
            "analysis": {"experience_level": "intermediate", "goal": "general"}
        })
        assert "note" in result["fallback_program"]
        assert "simplified" in result["fallback_program"]["note"].lower()

    def test_includes_user_friendly_message(self):
        """Test that error includes user-friendly message."""
        result = handle_methodology_error({
            "error": "Test error",
            "analysis": {"experience_level": "intermediate", "goal": "general"}
        })
        assert "message" in result


class TestHandleCriticalFailure:
    """Test critical failure handling."""

    def test_critical_failure_returns_failed_status(self):
        """Test that critical failure returns failed status."""
        result = handle_critical_failure({})
        assert result["status"] == "failed"

    def test_includes_technical_difficulties_message(self):
        """Test that critical failure includes technical difficulties message."""
        result = handle_critical_failure({})
        assert "message" in result
        assert "technical difficulties" in result["message"].lower()

    def test_includes_recommendation_to_consult_professional(self):
        """Test that critical failure includes professional consultation."""
        result = handle_critical_failure({})
        assert "recommendation" in result
        assert "personal trainer" in result["recommendation"].lower()

    def test_includes_error_code(self):
        """Test that critical failure includes error code."""
        result = handle_critical_failure({})
        assert "error_code" in result
        assert result["error_code"] == "CRITICAL_FAILURE"


class TestCreateFallbackWeeks:
    """Test fallback week creation."""

    def test_creates_four_weeks(self):
        """Test that fallback creates 4 weeks."""
        weeks = _create_fallback_weeks({"experience_level": "intermediate"})
        assert len(weeks) == 4

    def test_creates_three_day_schedule(self):
        """Test that fallback creates 3-day schedule."""
        weeks = _create_fallback_weeks({})
        for week in weeks:
            assert len(week["sessions"]) == 3

    def test_sessions_on_monday_wednesday_friday(self):
        """Test that sessions are on Mon/Wed/Fri."""
        weeks = _create_fallback_weeks({})
        week = weeks[0]
        days = [s["day"] for s in week["sessions"]]
        assert "monday" in days
        assert "wednesday" in days
        assert "friday" in days

    def test_includes_week_numbers(self):
        """Test that weeks include week numbers."""
        weeks = _create_fallback_weeks({})
        for i, week in enumerate(weeks, 1):
            assert week["week_number"] == i

    def test_includes_simplified_note(self):
        """Test that weeks include simplified note."""
        weeks = _create_fallback_weeks({})
        for week in weeks:
            assert "note" in week
            assert "simplified" in week["note"].lower()


class TestGetProfessionalResources:
    """Test professional resources retrieval."""

    def test_medical_resources_include_physician(self):
        """Test that medical resources include physician."""
        resources = _get_professional_resources("medical")
        assert any("physician" in r.lower() or "md" in r.lower() for r in resources)

    def test_medical_resources_include_sports_medicine(self):
        """Test that medical resources include sports medicine."""
        resources = _get_professional_resources("medical")
        assert any("sports medicine" in r.lower() for r in resources)

    def test_injury_resources_include_physical_therapist(self):
        """Test that injury resources include physical therapist."""
        resources = _get_professional_resources("injury")
        assert any("physical therapist" in r.lower() or "pt" in r.lower() for r in resources)

    def test_injury_resources_include_athletic_trainer(self):
        """Test that injury resources include athletic trainer."""
        resources = _get_professional_resources("injury")
        assert any("athletic trainer" in r.lower() or "atc" in r.lower() for r in resources)

    def test_eating_disorder_resources_include_neda(self):
        """Test that eating disorder resources include NEDA."""
        resources = _get_professional_resources("eating_disorder")
        assert any("neda" in r.lower() for r in resources)

    def test_eating_disorder_resources_include_hotline(self):
        """Test that eating disorder resources include hotline."""
        resources = _get_professional_resources("eating_disorder")
        assert any("helpline" in r.lower() or "hotline" in r.lower() for r in resources)

    def test_unknown_concern_returns_generic_resource(self):
        """Test that unknown concern returns generic resource."""
        resources = _get_professional_resources("unknown")
        assert "Healthcare Provider" in resources

    def test_all_resources_return_lists(self):
        """Test that all resources return lists."""
        for concern_type in ["medical", "injury", "eating_disorder"]:
            resources = _get_professional_resources(concern_type)
            assert isinstance(resources, list)
            assert len(resources) > 0
