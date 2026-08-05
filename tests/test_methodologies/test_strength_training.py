"""Tests for strength training methodology implementations."""

import pytest
from methodologies.strength_training import (
    build_linear_program,
    build_undulating_program
)


def test_linear_program_for_beginner():
    """Test that linear periodization generates correct structure for beginners."""
    analysis = {
        "experience_level": "beginner",
        "goal": "strength",
        "constraints": {"time_available": "3 days per week"}
    }
    program = build_linear_program(analysis)

    assert program["periodization_model"] == "linear"
    assert len(program["weeks"]) >= 8
    assert program["weeks"][0]["phase"] == "hypertrophy"
    assert program["weeks"][-1]["phase"] == "peaking"


def test_linear_program_has_deload():
    """Test that linear periodization includes deload weeks."""
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)

    deload_weeks = [w for w in program["weeks"] if w.get("is_deload")]
    assert len(deload_weeks) >= 2


def test_linear_program_progression():
    """Test that linear periodization shows intensity progression."""
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)

    week1_intensity = program["weeks"][0]["intensity_level"]
    week8_intensity = program["weeks"][7]["intensity_level"]
    assert week8_intensity > week1_intensity


def test_linear_program_complete_12_weeks():
    """Test that linear periodization creates complete 12-week program."""
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)

    assert len(program["weeks"]) == 12
    assert program["total_duration"] == "12 weeks"


def test_linear_program_phases():
    """Test that linear periodization has correct phases in order."""
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)

    # Weeks 1-4 should be hypertrophy
    for week in program["weeks"][:4]:
        assert week["phase"] == "hypertrophy"

    # Weeks 5-8 should be strength
    for week in program["weeks"][4:8]:
        assert week["phase"] == "strength"

    # Weeks 9-12 should be peaking
    for week in program["weeks"][8:12]:
        assert week["phase"] == "peaking"


def test_linear_program_deload_schedule():
    """Test that deload weeks are scheduled correctly."""
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)

    # Deload should be at weeks 4 and 8
    deload_weeks = [w for w in program["weeks"] if w.get("is_deload")]
    deload_week_numbers = [w["week_number"] for w in deload_weeks]

    assert 4 in deload_week_numbers
    assert 8 in deload_week_numbers


def test_linear_program_exercises():
    """Test that each week has appropriate exercises."""
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)

    # Check that sessions have exercises
    for week in program["weeks"]:
        for session in week["sessions"]:
            assert len(session["exercises"]) > 0
            assert "warmup" in session
            assert "cooldown" in session


# ============ UNDULATING PERIODIZATION TESTS ============

def test_undulating_program_for_intermediate():
    """Test that undulating periodization generates correct structure for intermediates."""
    analysis = {
        "experience_level": "intermediate",
        "goal": "strength",
        "constraints": {"time_available": "4 days per week"}
    }
    program = build_undulating_program(analysis)

    assert program["periodization_model"] == "undulating"
    assert "weekly_pattern" in program
    assert program["weekly_pattern"]["monday"] == "heavy"
    assert program["weekly_pattern"]["friday"] == "light"


def test_undulating_program_intensity_variation():
    """Test that undulating program varies intensity within the week."""
    analysis = {"experience_level": "intermediate", "goal": "strength"}
    program = build_undulating_program(analysis)

    week = program["weeks"][0]
    monday_session = next(s for s in week["sessions"] if s["day"] == "monday")
    friday_session = next(s for s in week["sessions"] if s["day"] == "friday")

    assert monday_session["intensity"] == "heavy"
    assert friday_session["intensity"] == "light"


def test_undulating_program_deload_weeks():
    """Test that undulating program includes deload weeks."""
    analysis = {"experience_level": "intermediate", "goal": "strength"}
    program = build_undulating_program(analysis)

    deload_weeks = [w for w in program["weeks"] if w.get("is_deload")]
    assert len(deload_weeks) >= 2

    # Check deload weeks are at weeks 4 and 8
    deload_week_numbers = [w["week_number"] for w in deload_weeks]
    assert 4 in deload_week_numbers
    assert 8 in deload_week_numbers


def test_undulating_program_complete_12_weeks():
    """Test that undulating program creates complete 12-week program."""
    analysis = {"experience_level": "intermediate", "goal": "strength"}
    program = build_undulating_program(analysis)

    assert len(program["weeks"]) == 12
    assert program["total_duration"] == "12 weeks"


def test_undulating_program_heavy_medium_light_pattern():
    """Test that undulating program follows heavy/medium/light pattern."""
    analysis = {"experience_level": "intermediate", "goal": "strength"}
    program = build_undulating_program(analysis)

    # Check weekly pattern is correct
    assert program["weekly_pattern"]["monday"] == "heavy"
    assert program["weekly_pattern"]["wednesday"] == "medium"
    assert program["weekly_pattern"]["friday"] == "light"


def test_undulating_program_intensity_parameters():
    """Test that intensity parameters are correct for each level."""
    analysis = {"experience_level": "intermediate", "goal": "strength"}
    program = build_undulating_program(analysis)

    week = program["weeks"][0]  # First week (non-deload)

    # Get heavy session
    heavy_session = next(s for s in week["sessions"] if s["intensity"] == "heavy")
    heavy_exercise = heavy_session["exercises"][0]

    # Get light session
    light_session = next(s for s in week["sessions"] if s["intensity"] == "light")
    light_exercise = light_session["exercises"][0]

    # Heavy should be higher intensity than light
    assert heavy_exercise["percent_1rm"] > light_exercise["percent_1rm"]
