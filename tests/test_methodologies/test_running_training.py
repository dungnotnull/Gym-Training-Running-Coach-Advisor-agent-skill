import pytest
from methodologies.running_training import build_base_building_program, build_race_preparation_program

def test_base_building_program():
    analysis = {"goal": "marathon", "experience_level": "intermediate"}
    program = build_base_building_program(analysis)
    assert program["program_type"] == "base_building"
    assert len(program["weeks"]) == 12

def test_race_preparation_program():
    analysis = {"goal": "5k", "experience_level": "beginner"}
    program = build_race_preparation_program(analysis)
    assert program["program_type"] == "race_preparation"
    assert len(program["weeks"]) == 11