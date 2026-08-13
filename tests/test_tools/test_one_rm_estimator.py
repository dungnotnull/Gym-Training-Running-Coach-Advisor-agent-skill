"""
Tests for 1RM Estimator Tool

Research-based testing for Epley and Brzycki formulas.
"""

import pytest
from tools.one_rm_estimator import estimate_1rm, test_1rm_protocol, calculate_training_percentages


class TestEstimate1RM:
    """Test 1RM estimation formulas."""

    def test_epley_formula_basic_calculation(self):
        """Test Epley formula: weight × (1 + reps/30)."""
        result = estimate_1rm(100, 5, formula="epley")
        # 100 × (1 + 5/30) = 100 × 1.1667 = 116.67
        assert abs(result["estimated_1rm"] - 116.67) < 0.1

    def test_brzycki_formula_basic_calculation(self):
        """Test Brzycki formula: weight × (36/(37-reps))."""
        result = estimate_1rm(100, 5, formula="brzycki")
        # 100 × (36/(37-5)) = 100 × 1.125 = 112.5
        assert abs(result["estimated_1rm"] - 112.5) < 0.1

    def test_epley_heavy_weight_low_reps(self):
        """Test Epley with heavy weight, low reps (near 1RM)."""
        result = estimate_1rm(200, 3, formula="epley")
        # 200 × (1 + 3/30) = 200 × 1.1 = 220
        assert abs(result["estimated_1rm"] - 220.0) < 0.1

    def test_brzycki_heavy_weight_low_reps(self):
        """Test Brzycki with heavy weight, low reps."""
        result = estimate_1rm(200, 3, formula="brzycki")
        # 200 × (36/(37-3)) = 200 × 1.0588 = 211.76
        assert abs(result["estimated_1rm"] - 211.76) < 0.1

    def test_epley_with_high_reps(self):
        """Test Epley with higher reps (less accurate)."""
        result = estimate_1rm(60, 8, formula="epley")
        # 60 × (1 + 8/30) = 60 × 1.267 = 76
        assert abs(result["estimated_1rm"] - 76.0) < 0.1

    def test_brzycki_with_high_reps(self):
        """Test Brzycki with higher reps."""
        result = estimate_1rm(60, 8, formula="brzycki")
        # 60 × (36/(37-8)) = 60 × 1.241 = 74.48
        assert abs(result["estimated_1rm"] - 74.48) < 0.1

    def test_both_formulas_return_similar_results(self):
        """Test that both formulas return similar estimates (within 10%)."""
        epley_result = estimate_1rm(100, 5, formula="epley")
        brzycki_result = estimate_1rm(100, 5, formula="brzycki")

        difference = abs(epley_result["estimated_1rm"] - brzycki_result["estimated_1rm"])
        avg = (epley_result["estimated_1rm"] + brzycki_result["estimated_1rm"]) / 2

        # Difference should be less than 10% of average
        assert (difference / avg) < 0.10

    def test_invalid_formula_raises_error(self):
        """Test that invalid formula name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown formula"):
            estimate_1rm(100, 5, formula="invalid")

    def test_zero_reps_raises_error(self):
        """Test that zero reps raises ValueError."""
        with pytest.raises(ValueError, match="Reps must be greater than 0"):
            estimate_1rm(100, 0)

    def test_negative_reps_raises_error(self):
        """Test that negative reps raises ValueError."""
        with pytest.raises(ValueError, match="Reps must be greater than 0"):
            estimate_1rm(100, -5)

    def test_ten_or_more_reps_raises_warning(self):
        """Test that 10+ reps raises ValueError (less accurate)."""
        with pytest.raises(ValueError, match="less accurate"):
            estimate_1rm(100, 10)

    def test_returns_formula_used(self):
        """Test that result includes which formula was used."""
        result = estimate_1rm(100, 5, formula="epley")
        assert result["formula_used"] == "epley"

    def test_returns_based_on_values(self):
        """Test that result includes based_on with weight and reps."""
        result = estimate_1rm(135, 4, formula="brzycki")
        assert result["based_on"]["weight"] == 135
        assert result["based_on"]["reps"] == 4

    def test_default_formula_is_epley(self):
        """Test that default formula is Epley when not specified."""
        result = estimate_1rm(100, 5)
        assert result["formula_used"] == "epley"

    def test_includes_confidence_level(self):
        """Test that result includes confidence level."""
        result = estimate_1rm(100, 3, formula="epley")
        assert "confidence_level" in result
        # Low reps should have high confidence
        assert result["confidence_level"] == "high"

    def test_high_reps_have_moderate_confidence(self):
        """Test that higher reps have moderate confidence."""
        result = estimate_1rm(100, 7, formula="epley")
        assert result["confidence_level"] == "moderate"


class TestCalculateTrainingPercentages:
    """Test training percentage calculations."""

    def test_returns_standard_percentages(self):
        """Test that standard training percentages are returned."""
        result = calculate_training_percentages(200)
        assert "50_percent" in result
        assert "70_percent" in result
        assert "85_percent" in result

    def test_calculations_are_accurate(self):
        """Test that percentage calculations are accurate."""
        result = calculate_training_percentages(100)
        assert result["70_percent"] == 70
        assert result["85_percent"] == 85
        assert result["50_percent"] == 50


class Test1RMTestingProtocol:
    """Test 1RM testing protocol generation."""

    def test_squat_protocol(self):
        """Test squat 1RM testing protocol."""
        protocol = test_1rm_protocol("squat")
        assert "warmup_sets" in protocol
        assert protocol["warmup_sets"] == 3

    def test_bench_press_protocol(self):
        """Test bench press 1RM testing protocol."""
        protocol = test_1rm_protocol("bench_press")
        assert "warmup_sets" in protocol
        assert "safety_warning" in protocol

    def test_deadlift_protocol(self):
        """Test deadlift 1RM testing protocol."""
        protocol = test_1rm_protocol("deadlift")
        assert "warmup_sets" in protocol
        assert "rest_between_attempts" in protocol

    def test_protocol_has_warmup_reps(self):
        """Test that protocol includes warmup reps progression."""
        protocol = test_1rm_protocol("squat")
        assert "warmup_reps" in protocol
        assert len(protocol["warmup_reps"]) == 3

    def test_includes_rest_periods(self):
        """Test that protocol includes rest periods."""
        protocol = test_1rm_protocol("squat")
        assert "rest_between_attempts" in protocol

    def test_squat_includes_increment(self):
        """Test that protocol includes weight increment."""
        protocol = test_1rm_protocol("squat")
        assert "increment" in protocol

    def test_includes_safety_warning(self):
        """Test that protocol includes safety warning."""
        protocol = test_1rm_protocol("squat")
        assert "safety_warning" in protocol

    def test_unknown_exercise_returns_default(self):
        """Test that unknown exercise returns default (squat) protocol."""
        protocol = test_1rm_protocol("unknown_exercise")
        # Should return squat protocol as default
        assert protocol["warmup_sets"] == 3

    def test_overhead_press_protocol(self):
        """Test overhead press protocol."""
        protocol = test_1rm_protocol("overhead_press")
        assert "warmup_sets" in protocol
        assert "safety_warning" in protocol
