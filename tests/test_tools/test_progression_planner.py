"""
Tests for Progression Planner Tool

Research-based testing for progression planning and deload protocols.
Based on Rhea et al. (2003), Bompa & Buzzichelli (2018), Kreher & Schwartz (2012).
"""

import pytest
from tools.progression_planner import (
    create_progression_plan,
    create_deload_protocol,
    calculate_overload_progression,
    ProgressionType
)


class TestCreateProgressionPlan:
    """Test progression plan creation."""

    def test_linear_progression_for_beginner(self):
        """Test linear progression for beginner program."""
        program = {
            "weeks": [
                {"week_number": 1, "intensity_level": 0.60},
                {"week_number": 2, "intensity_level": 0.65},
            ]
        }
        result = create_progression_plan(program, "linear")
        assert result["type"] == "linear"
        assert "phases" in result

    def test_undulating_progression_for_intermediate(self):
        """Test undulating (DUP) progression for intermediate."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {"day": "monday", "intensity": "heavy"},
                        {"day": "wednesday", "intensity": "medium"},
                        {"day": "friday", "intensity": "light"}
                    ]
                }
            ]
        }
        result = create_progression_plan(program, "undulating")
        assert result["type"] == "undulating"
        assert "weekly_pattern" in result

    def test_block_progression_for_advanced(self):
        """Test block progression for advanced program."""
        program = {
            "weeks": [
                {"week_number": 1, "phase": "accumulation"},
                {"week_number": 2, "phase": "accumulation"},
            ],
            "blocks": [
                {"type": "accumulation", "focus": "work capacity"}
            ]
        }
        result = create_progression_plan(program, "block")
        assert result["type"] == "block"
        assert "block_sequence" in result

    def test_unknown_progression_type_returns_error(self):
        """Test that unknown progression type returns error dict."""
        program = {"weeks": []}
        result = create_progression_plan(program, "unknown_type")
        assert "error" in result

    def test_empty_weeks_returns_error(self):
        """Test that empty weeks list returns error."""
        program = {"weeks": []}
        result = create_progression_plan(program, "linear")
        assert "error" in result

    def test_linear_includes_progression_rules(self):
        """Test that linear progression includes rules."""
        program = {
            "weeks": [
                {"week_number": 1, "intensity_level": 0.60}
            ]
        }
        result = create_progression_plan(program, "linear")
        assert "progression_rules" in result
        assert len(result["progression_rules"]) > 0

    def test_undulating_weekly_pattern(self):
        """Test that undulating has heavy/medium/light pattern."""
        program = {
            "weeks": [{"week_number": 1, "sessions": []}]
        }
        result = create_progression_plan(program, "undulating")
        assert result["weekly_pattern"]["monday"] == "heavy"
        assert result["weekly_pattern"]["wednesday"] == "medium"
        assert result["weekly_pattern"]["friday"] == "light"

    def test_block_sequence_includes_accumulation(self):
        """Test that block sequence includes accumulation."""
        program = {
            "weeks": [],
            "blocks": []
        }
        result = create_progression_plan(program, "block")
        assert "accumulation" in result["block_sequence"]

    def test_includes_next_steps(self):
        """Test that progression plan includes next steps."""
        program = {
            "weeks": [{"week_number": 1, "intensity_level": 0.60}]
        }
        result = create_progression_plan(program, "linear")
        assert "next_steps" in result
        assert len(result["next_steps"]) > 0


class TestCreateDeloadProtocol:
    """Test deload protocol creation."""

    def test_standard_deload_protocol(self):
        """Test standard deload (50% volume reduction)."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [
                                {"name": "squat", "sets": 3, "reps": 10, "percent_1rm": 0.70}
                            ]
                        }
                    ]
                }
            ]
        }
        result = create_deload_protocol(program, "standard")
        assert result["severity"] == "standard"
        assert result["volume_reduction"] == "50%"

    def test_light_deload_protocol(self):
        """Test light deload (30% volume reduction)."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [{"name": "squat", "sets": 3, "reps": 10}]
                        }
                    ]
                }
            ]
        }
        result = create_deload_protocol(program, "light")
        assert result["volume_reduction"] == "30%"

    def test_aggressive_deload_protocol(self):
        """Test aggressive deload (60% volume, 10% intensity reduction)."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [{"name": "squat", "sets": 3, "reps": 10}]
                        }
                    ]
                }
            ]
        }
        result = create_deload_protocol(program, "aggressive")
        assert result["volume_reduction"] == "60%"
        assert result["intensity_reduction"] == "10%"

    def test_deload_reduces_sets_properly(self):
        """Test that deload properly reduces sets."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [
                                {"name": "squat", "sets": 5, "reps": 10, "percent_1rm": 0.70}
                            ]
                        }
                    ]
                }
            ]
        }
        result = create_deload_protocol(program, "standard")
        # 5 sets with 50% reduction = 2.5 → rounds to 2 or 3
        deload_sets = result["sessions"][0]["exercises"][0]["sets"]
        assert deload_sets in [2, 3]

    def test_deload_maintains_intensity_for_standard(self):
        """Test that standard deload maintains intensity."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [
                                {"name": "squat", "sets": 3, "reps": 10, "percent_1rm": 0.75}
                            ]
                        }
                    ]
                }
            ]
        }
        result = create_deload_protocol(program, "standard")
        # Standard should not reduce intensity
        deload_intensity = result["sessions"][0]["exercises"][0]["percent_1rm"]
        assert deload_intensity == 0.75

    def test_aggressive_deload_reduces_intensity(self):
        """Test that aggressive deload reduces intensity."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [
                                {"name": "squat", "sets": 3, "reps": 10, "percent_1rm": 0.80}
                            ]
                        }
                    ]
                }
            ]
        }
        result = create_deload_protocol(program, "aggressive")
        # Aggressive should reduce intensity by 10%
        deload_intensity = result["sessions"][0]["exercises"][0]["percent_1rm"]
        assert deload_intensity < 0.80

    def test_deload_duration_is_one_week(self):
        """Test that deload protocol is for 1 week."""
        program = {
            "weeks": [{"week_number": 1, "sessions": []}]
        }
        result = create_deload_protocol(program, "standard")
        assert result["duration"] == "1 week"

    def test_deload_includes_focus_on_recovery(self):
        """Test that deload includes recovery focus."""
        program = {
            "weeks": [{"week_number": 1, "sessions": []}]
        }
        result = create_deload_protocol(program, "standard")
        assert "focus" in result
        assert "recovery" in result["focus"].lower()

    def test_deload_minimum_one_set(self):
        """Test that deload never goes below 1 set."""
        program = {
            "weeks": [
                {
                    "week_number": 1,
                    "sessions": [
                        {
                            "day": "monday",
                            "exercises": [
                                {"name": "squat", "sets": 1, "reps": 10, "percent_1rm": 0.70}
                            ]
                        }
                    ]
                }
            ]
        }
        result = create_deload_protocol(program, "aggressive")
        # Even aggressive (60% reduction) should keep at least 1 set
        deload_sets = result["sessions"][0]["exercises"][0]["sets"]
        assert deload_sets >= 1


class TestCalculateOverloadProgression:
    """Test overload progression calculations."""

    def test_calculate_improvement_percentage(self):
        """Test calculation of improvement percentage."""
        result = calculate_overload_progression(
            starting_1rm=100,
            current_1rm=110,
            weeks_trained=4
        )
        assert result["improvement_percentage"] == 10.0

    def test_weekly_improvement_calculation(self):
        """Test weekly improvement rate calculation (already × 100 in result)."""
        result = calculate_overload_progression(
            starting_1rm=100,
            current_1rm=110,
            weeks_trained=4
        )
        # 10% / 4 weeks = 2.5% per week, but returned as 2.5 (not 0.025)
        assert result["weekly_improvement"] == 2.5

    def test_predictions_for_target_increases(self):
        """Test predictions for various target increases."""
        result = calculate_overload_progression(
            starting_1rm=100,
            current_1rm=105,
            weeks_trained=2
        )
        assert "predictions" in result
        assert "+5%" in result["predictions"]
        assert "+10%" in result["predictions"]
        assert "+15%" in result["predictions"]

    def test_zero_weeks_returns_error(self):
        """Test that zero weeks trained returns error dict."""
        result = calculate_overload_progression(100, 100, 0)
        assert "error" in result
        assert result["error"] == "No training data"

    def test_includes_projection_summary(self):
        """Test that result includes projection summary."""
        result = calculate_overload_progression(
            starting_1rm=100,
            current_1rm=110,
            weeks_trained=4
        )
        assert "projection" in result

    def test_diminishing_returns_in_prediction(self):
        """Test that predictions account for diminishing returns."""
        result = calculate_overload_progression(
            starting_1rm=100,
            current_1rm=110,
            weeks_trained=4
        )
        # Predicted weekly rate should be less than actual weekly rate
        assert result["predicted_weekly_rate"] < result["weekly_improvement"]

    def test_beginner_faster_improvement_assumed(self):
        """Test that beginners are assumed to improve faster."""
        beginner_result = calculate_overload_progression(
            starting_1rm=100,
            current_1rm=115,
            weeks_trained=4
        )
        # 15% in 4 weeks = 3.75% weekly (beginner rate)
        assert beginner_result["weekly_improvement"] > 2.0


class TestProgressionTypeEnum:
    """Test ProgressionType enum values."""

    def test_progression_types_exist(self):
        """Test that all progression types are defined."""
        assert ProgressionType.LINEAR.value == "linear"
        assert ProgressionType.UNDULATING.value == "undulating"
        assert ProgressionType.BLOCK.value == "block"
