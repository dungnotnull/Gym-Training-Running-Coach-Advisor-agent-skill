"""Tests for strength training methodology implementations."""

import pytest
from methodologies.strength_training import (
    build_linear_program,
    build_undulating_program,
    build_block_program
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


# ============ BLOCK PERIODIZATION TESTS ============

def test_block_program_for_advanced():
    """Test that block periodization generates correct structure for advanced."""
    analysis = {
        "experience_level": "advanced",
        "goal": "strength",
        "constraints": {"time_available": "5 days per week"}
    }
    program = build_block_program(analysis)

    assert program["periodization_model"] == "block"
    assert len(program["blocks"]) == 3
    assert program["blocks"][0]["type"] == "accumulation"
    assert program["blocks"][2]["type"] == "realization"


def test_block_program_sequential_focus():
    """Test that block program has sequential training focus."""
    analysis = {"experience_level": "advanced", "goal": "strength"}
    program = build_block_program(analysis)

    # Each block should have different focus
    assert program["blocks"][0]["focus"] != program["blocks"][1]["focus"]
    assert program["blocks"][1]["focus"] != program["blocks"][2]["focus"]


def test_block_program_accumulation_block():
    """Test that accumulation block has high volume, low intensity."""
    analysis = {"experience_level": "advanced", "goal": "strength"}
    program = build_block_program(analysis)

    accumulation = program["blocks"][0]

    assert accumulation["type"] == "accumulation"
    assert accumulation["volume"] == "high"
    assert accumulation["intensity"] == "low to moderate"


def test_block_program_realization_block():
    """Test that realization block has low volume, high intensity."""
    analysis = {"experience_level": "advanced", "goal": "strength"}
    program = build_block_program(analysis)

    realization = program["blocks"][2]

    assert realization["type"] == "realization"
    assert realization["volume"] == "low"
    assert realization["intensity"] == "high"


def test_block_program_duration():
    """Test that each block is 4 weeks."""
    analysis = {"experience_level": "advanced", "goal": "strength"}
    program = build_block_program(analysis)

    for block in program["blocks"]:
        assert block["duration"] == "4 weeks"
        assert len(block["weeks"]) == 4


def test_block_program_exercises_progression():
    """Test that exercises progress from accumulation to realization."""
    analysis = {"experience_level": "advanced", "goal": "strength"}
    program = build_block_program(analysis)

    accumulation_exercise = program["blocks"][0]["weeks"][0]["exercises"][0]
    realization_exercise = program["blocks"][2]["weeks"][0]["exercises"][0]

    # Realization should have higher intensity (lower reps) than accumulation
    realization_reps = int(realization_exercise["reps"])
    accumulation_reps = int(accumulation_exercise["reps"].split("-")[0])

    assert realization_reps < accumulation_reps
