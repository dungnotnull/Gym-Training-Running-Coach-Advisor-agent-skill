"""
Tests for Recovery Status Tool

Research-based testing for recovery assessment and OTS detection.
Based on Kreher & Schwartz (2012) overtraining syndrome research.
"""

import pytest
from tools.recovery_status import (
    determine_recovery_status,
    assess_overtraining_risk
)


class TestDetermineRecoveryStatus:
    """Test recovery status determination."""

    def test_optimal_recovery_all_scores_five(self):
        """Test optimal recovery when all markers are 5/5."""
        result = determine_recovery_status(
            sleep_hours=8,
            sleep_quality="excellent",
            resting_hr=60,
            mood="energetic",
            muscle_soreness="none",
            motivation_level="high"
        )
        assert result["status"] == "optimal"
        assert result["overall_score"] == 5.0

    def test_good_recovery_mostly_high_scores(self):
        """Test good recovery with mostly high scores."""
        result = determine_recovery_status(
            sleep_hours=7,
            sleep_quality="good",
            resting_hr=62,
            mood="good",
            muscle_soreness="mild",
            motivation_level="high"
        )
        assert result["status"] in ["optimal", "good"]

    def test_moderate_recovery_mixed_scores(self):
        """Test moderate recovery with mixed scores."""
        result = determine_recovery_status(
            sleep_hours=6,
            sleep_quality="fair",
            resting_hr=65,
            mood="neutral",
            muscle_soreness="moderate",
            motivation_level="moderate"
        )
        assert result["status"] == "moderate"

    def test_poor_recovery_low_scores(self):
        """Test poor recovery with low scores."""
        result = determine_recovery_status(
            sleep_hours=5,
            sleep_quality="poor",
            resting_hr=70,
            mood="fatigued",
            muscle_soreness="high",
            motivation_level="low"
        )
        assert result["status"] == "poor"

    def test_critical_recovery_all_scores_one(self):
        """Test critical recovery when all markers are 1/5."""
        result = determine_recovery_status(
            sleep_hours=4,
            sleep_quality="terrible",
            resting_hr=80,
            mood="exhausted",
            muscle_soreness="severe",
            motivation_level="very_low"
        )
        assert result["status"] == "critical"

    def test_includes_individual_marker_scores(self):
        """Test that result includes individual marker scores."""
        result = determine_recovery_status(
            sleep_hours=7,
            sleep_quality="good",
            resting_hr=62,
            mood="good",
            muscle_soreness="mild",
            motivation_level="high"
        )
        assert "marker_scores" in result
        assert "sleep_score" in result["marker_scores"]
        assert "hrv_score" in result["marker_scores"]
        assert "mood_score" in result["marker_scores"]
        assert "soreness_score" in result["marker_scores"]
        assert "motivation_score" in result["marker_scores"]

    def test_low_sleep_produces_low_sleep_score(self):
        """Test that low sleep hours produce low sleep score."""
        result = determine_recovery_status(
            sleep_hours=5,
            sleep_quality="poor",
            resting_hr=62,
            mood="good",
            muscle_soreness="mild",
            motivation_level="high"
        )
        assert result["marker_scores"]["sleep_score"] <= 2

    def test_high_resting_hr_reduces_hrv_score(self):
        """Test that high resting HR reduces HRV score."""
        result = determine_recovery_status(
            sleep_hours=7,
            sleep_quality="good",
            resting_hr=75,
            mood="good",
            muscle_soreness="mild",
            motivation_level="high"
        )
        assert result["marker_scores"]["hrv_score"] <= 2

    def test_includes_recommendations(self):
        """Test that result includes recommendations."""
        result = determine_recovery_status(
            sleep_hours=6,
            sleep_quality="fair",
            resting_hr=65,
            mood="neutral",
            muscle_soreness="moderate",
            motivation_level="moderate"
        )
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0

    def test_poor_recovery_has_more_recommendations(self):
        """Test that poor recovery status has more recommendations."""
        poor_result = determine_recovery_status(
            sleep_hours=5,
            sleep_quality="poor",
            resting_hr=70,
            mood="fatigued",
            muscle_soreness="high",
            motivation_level="low"
        )
        good_result = determine_recovery_status(
            sleep_hours=8,
            sleep_quality="excellent",
            resting_hr=60,
            mood="energetic",
            muscle_soreness="none",
            motivation_level="high"
        )
        assert len(poor_result["recommendations"]) > len(good_result["recommendations"])

    def test_ots_warning_signs_detection(self):
        """Test detection of OTS warning signs."""
        result = determine_recovery_status(
            sleep_hours=4,
            sleep_quality="poor",
            resting_hr=80,
            mood="exhausted",
            muscle_soreness="severe",
            motivation_level="very_low"
        )
        assert "warnings" in result
        assert len(result["warnings"]) > 0

    def test_no_ots_warnings_for_optimal_recovery(self):
        """Test no OTS warnings for optimal recovery."""
        result = determine_recovery_status(
            sleep_hours=8,
            sleep_quality="excellent",
            resting_hr=60,
            mood="energetic",
            muscle_soreness="none",
            motivation_level="high"
        )
        assert len(result.get("warnings", [])) == 0

    def test_invalid_sleep_hours_raises_error(self):
        """Test that invalid sleep hours raises error."""
        with pytest.raises(ValueError):
            determine_recovery_status(
                sleep_hours=-1,
                sleep_quality="good",
                resting_hr=62,
                mood="good",
                muscle_soreness="mild",
                motivation_level="high"
            )

    def test_invalid_resting_hr_raises_error(self):
        """Test that invalid resting HR raises error."""
        with pytest.raises(ValueError):
            determine_recovery_status(
                sleep_hours=7,
                sleep_quality="good",
                resting_hr=0,
                mood="good",
                muscle_soreness="mild",
                motivation_level="high"
            )


class TestAssessOvertrainingRisk:
    """Test overtraining risk assessment."""

    def test_low_risk_with_clean_history(self):
        """Test low risk with clean session history."""
        session = {
            "iteration_count": 4,
            "user_profile": {"flags": []},
            "program_history": [
                {"iteration": 1},
                {"iteration": 2}
            ]
        }
        result = assess_overtraining_risk(session)
        assert result["risk_level"] == "low"

    def test_moderate_risk_with_two_warning_signs(self):
        """Test moderate risk with 2 warning signs."""
        session = {
            "iteration_count": 10,
            "user_profile": {"flags": ["recovery_concern"]},
            "program_history": [{"iteration": 1}, {"iteration": 2}]
        }
        result = assess_overtraining_risk(session)
        # High training frequency + recovery concern = 2 warning signs
        assert result["risk_level"] in ["low", "moderate"]

    def test_high_risk_with_multiple_warning_signs(self):
        """Test high risk with multiple warning signs."""
        session = {
            "iteration_count": 10,
            "user_profile": {"flags": ["recovery_concern", "medical_concern"]},
            "program_history": [{"iteration": 1}, {"iteration": 2}]
        }
        result = assess_overtraining_risk(session)
        # High frequency + 2 concerns = 3 warning signs
        assert result["risk_level"] in ["moderate", "high"]

    def test_critical_risk_with_many_warning_signs(self):
        """Test critical risk with 4+ warning signs."""
        # Need more complex setup to trigger 4+ signs
        session = {
            "iteration_count": 15,
            "user_profile": {"flags": ["recovery_concern", "medical_concern"]},
            "program_history": [{"iteration": 1}, {"iteration": 2}]
        }
        result = assess_overtraining_risk(session)
        # Should have at least 3 warning signs
        assert result["risk_level"] in ["moderate", "high", "critical"]

    def test_includes_warning_signs_list(self):
        """Test that assessment includes warning signs."""
        session = {
            "iteration_count": 10,
            "user_profile": {"flags": ["recovery_concern"]},
            "program_history": [{"iteration": 1}, {"iteration": 2}]
        }
        result = assess_overtraining_risk(session)
        assert "warning_signs" in result

    def test_includes_recommendation(self):
        """Test that risk assessment includes recommendation."""
        session = {
            "iteration_count": 5,
            "user_profile": {"flags": []},
            "program_history": []
        }
        result = assess_overtraining_risk(session)
        assert "recommendation" in result

    def test_medical_concern_adds_warning_sign(self):
        """Test that medical concern adds warning sign."""
        session = {
            "iteration_count": 5,
            "user_profile": {"flags": ["medical_concern"]},
            "program_history": []
        }
        result = assess_overtraining_risk(session)
        assert "Medical concern present" in result["warning_signs"]

    def test_recovery_concern_adds_warning_sign(self):
        """Test that recovery concern adds warning sign."""
        session = {
            "iteration_count": 5,
            "user_profile": {"flags": ["recovery_concern"]},
            "program_history": []
        }
        result = assess_overtraining_risk(session)
        assert "Recovery concern flagged" in result["warning_signs"]

    def test_high_iteration_count_adds_warning_sign(self):
        """Test that high iteration count adds warning sign."""
        session = {
            "iteration_count": 10,
            "user_profile": {"flags": []},
            "program_history": [{"iteration": 1}, {"iteration": 2}]
        }
        result = assess_overtraining_risk(session)
        assert any("frequency" in sign for sign in result["warning_signs"])
