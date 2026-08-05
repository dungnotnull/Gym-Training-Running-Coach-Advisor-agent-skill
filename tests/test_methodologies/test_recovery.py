"""Tests for recovery methodology."""
import pytest
from methodologies.recovery import (
    generate_recovery_plan,
    _create_recovery_sessions,
    assess_overtraining_risk
)


class TestGenerateRecoveryPlan:
    """Test recovery plan generation."""

    def test_generate_recovery_plan_structure(self):
        """Test recovery plan has correct structure."""
        analysis = {
            "experience_level": "intermediate",
            "goal": "general",
            "constraints": {}
        }
        plan = generate_recovery_plan(analysis)

        assert plan["type"] == "recovery"
        assert plan["duration"] == "4 weeks"
        assert plan["focus"] == "Restore and rebuild"
        assert len(plan["weeks"]) == 4

    def test_generate_recovery_plan_week_structure(self):
        """Test each week has proper structure."""
        analysis = {
            "experience_level": "intermediate",
            "goal": "general"
        }
        plan = generate_recovery_plan(analysis)

        for week in plan["weeks"]:
            assert "week_number" in week
            assert "focus" in week
            assert "intensity" in week
            assert "sessions" in week
            assert week["focus"] == "recovery"
            assert week["intensity"] == "low"

    def test_generate_recovery_plan_week_numbering(self):
        """Test weeks are numbered sequentially."""
        analysis = {}
        plan = generate_recovery_plan(analysis)

        week_numbers = [week["week_number"] for week in plan["weeks"]]
        assert week_numbers == [1, 2, 3, 4]


class TestCreateRecoverySessions:
    """Test recovery session creation."""

    def test_create_recovery_sessions_returns_list(self):
        """Test sessions is a list."""
        analysis = {"experience_level": "intermediate"}
        sessions = _create_recovery_sessions(analysis)

        assert isinstance(sessions, list)

    def test_create_recovery_sessions_content(self):
        """Test recovery sessions have proper structure."""
        analysis = {}
        sessions = _create_recovery_sessions(analysis)

        # Should have sessions for the week
        assert len(sessions) > 0

        # Check first session structure
        session = sessions[0]
        assert "day" in session
        assert "zone" in session
        assert "duration" in session


class TestAssessOvertrainingRisk:
    """Test overtraining risk assessment."""

    def test_assess_overtraining_risk_no_flags(self):
        """Test risk is low without recovery concern flag."""
        session = {"flags": [], "type": "easy_run"}
        result = assess_overtraining_risk(session)

        assert result["risk_level"] == "low"

    def test_assess_overtraining_risk_with_recovery_concern(self):
        """Test risk is high with recovery concern flag."""
        session = {
            "flags": ["recovery_concern"],
            "type": "intervals"
        }
        result = assess_overtraining_risk(session)

        assert result["risk_level"] == "high"

    def test_assess_overtraining_risk_no_flags_key(self):
        """Test risk when flags key is missing."""
        session = {"type": "easy_run"}
        result = assess_overtraining_risk(session)

        assert result["risk_level"] == "low"

    def test_assess_overtraining_risk_other_flags(self):
        """Test risk with other flags but not recovery concern."""
        session = {
            "flags": ["injury", "medical_concern"],
            "type": "tempo"
        }
        result = assess_overtraining_risk(session)

        assert result["risk_level"] == "low"
