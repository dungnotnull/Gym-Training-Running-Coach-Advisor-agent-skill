import pytest
from router import TrainingAdvisorRouter

def test_router_initialization():
    router = TrainingAdvisorRouter()
    assert router.session_id is not None
    assert "session_id" in router.session
    assert "created_at" in router.session
    assert "user_profile" in router.session
    assert "program_history" in router.session
    assert "iteration_count" in router.session

def test_router_generates_unique_session_ids():
    router1 = TrainingAdvisorRouter()
    router2 = TrainingAdvisorRouter()
    assert router1.session_id != router2.session_id

def test_analyze_input_returns_analysis():
    router = TrainingAdvisorRouter()
    analysis = router.analyze_input("I'm a beginner wanting to get stronger")

    assert analysis["experience_level"] == "beginner"
    assert analysis["goal"] == "strength"
    assert "constraints" in analysis
    assert "flags" in analysis

def test_analyze_input_extracts_constraints():
    router = TrainingAdvisorRouter()
    analysis = router.analyze_input("I can train 3 days per week with dumbbells")

    assert analysis["constraints"]["time_available"] == "3 days per week"
    assert "dumbbell" in analysis["constraints"]["equipment"]

def test_analyze_input_detects_flags():
    router = TrainingAdvisorRouter()
    analysis = router.analyze_input("I have diabetes and want to get stronger")

    assert "medical_concern" in analysis["flags"]

def test_select_methodology_for_strength():
    router = TrainingAdvisorRouter()
    analysis = {"goal": "strength", "experience_level": "intermediate"}
    methodology = router._select_methodology(analysis)
    assert methodology == "strength"

def test_select_methodology_for_running():
    router = TrainingAdvisorRouter()
    analysis = {"goal": "marathon", "experience_level": "advanced"}
    methodology = router._select_methodology(analysis)
    assert methodology == "running"

def test_select_methodology_for_recovery_priority():
    router = TrainingAdvisorRouter()
    analysis = {"goal": "strength", "flags": ["recovery_concern"]}
    methodology = router._select_methodology(analysis)
    assert methodology == "recovery"
