import pytest
from tools.vdot_calculator import calculate_training_zones, estimate_vdot_from_race_time

def test_calculate_zones_from_vdot():
    result = calculate_training_zones(45.0)
    assert result["vdot_score"] == 45.0
    assert "zones" in result
    assert "zone1_easy" in result["zones"]

def test_invalid_vdot_raises_error():
    with pytest.raises(ValueError):
        calculate_training_zones(150)

def test_estimate_vdot_from_5k():
    vdot = estimate_vdot_from_race_time("5k", "22:00")
    assert 40 <= vdot <= 50