import pytest
from methodologies.shared_utils import classify_experience, classify_goal, extract_constraints

def test_classify_beginner():
    assert classify_experience("I'm new to lifting") == "beginner"
    assert classify_experience("just starting out") == "beginner"
    assert classify_experience("never worked out before") == "beginner"

def test_classify_intermediate():
    assert classify_experience("I've been training for 2 years") == "intermediate"
    assert classify_experience("consistent for 18 months") == "intermediate"

def test_classify_advanced():
    assert classify_experience("I've been training 5 years") == "advanced"
    assert classify_experience("competitive lifter") == "advanced"

def test_classify_unknown_defaults_to_intermediate():
    assert classify_experience("not sure about my experience") == "intermediate"

def test_classify_strength_goal():
    assert classify_goal("I want to get stronger") == "strength"
    assert classify_goal("build strength") == "strength"
    assert classify_goal("increase my squat") == "strength"

def test_classify_hypertrophy_goal():
    assert classify_goal("build muscle mass") == "hypertrophy"
    assert classify_goal("get bigger") == "hypertrophy"
    assert classify_goal("hypertrophy") == "hypertrophy"

def test_classify_running_goals():
    assert classify_goal("train for a 5K") == "5k"
    assert classify_goal("run a marathon") == "marathon"
    assert classify_goal("half marathon training") == "half_marathon"

def test_classify_general_fitness():
    assert classify_goal("just get fit") == "general"
    assert classify_goal("overall health") == "general"

def test_extract_time_constraint():
    result = extract_constraints("I can train 3 days per week")
    assert result["time_available"] == "3 days per week"

def test_extract_equipment_constraint():
    result = extract_constraints("I have dumbbells and a bench")
    assert "dumbbell" in result["equipment"]
    assert "bench" in result["equipment"]

def test_extract_health_constraints():
    result = extract_constraints("I have a bad shoulder")
    assert "shoulder" in result.get("health_conditions", [])

def test_no_constraints_returns_empty():
    result = extract_constraints("I want to get stronger")
    assert result["time_available"] is None
    assert result["equipment"] == []
    assert result["health_conditions"] == []

