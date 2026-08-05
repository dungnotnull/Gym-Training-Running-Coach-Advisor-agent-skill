from datetime import datetime
from typing import Dict, Any

def calculate_training_zones(vdot_score: float) -> Dict[str, Any]:
    """Calculate training zones from VDOT score."""
    if not vdot_score or vdot_score < 10 or vdot_score > 80:
        raise ValueError(f"Invalid VDOT score: {vdot_score}")

    return {
        "vdot_score": vdot_score,
        "zones": {
            "zone1_easy": _calculate_zone1(vdot_score),
            "zone2_marathon": _calculate_zone2(vdot_score),
            "zone3_threshold": _calculate_zone3(vdot_score),
            "zone4_interval": _calculate_zone4(vdot_score),
            "zone5_repetition": _calculate_zone5(vdot_score)
        },
        "calculated_at": datetime.now().isoformat()
    }

def _calculate_zone1(vdot: float) -> Dict[str, Any]:
    return {"vo2_range": "59-74%", "description": "Easy/recovery"}

def _calculate_zone2(vdot: float) -> Dict[str, Any]:
    return {"vo2_range": "75-82%", "description": "Marathon pace"}

def _calculate_zone3(vdot: float) -> Dict[str, Any]:
    return {"vo2_range": "83-88%", "description": "Threshold/tempo"}

def _calculate_zone4(vdot: float) -> Dict[str, Any]:
    return {"vo2_range": "89-94%", "description": "Interval/VO2max"}

def _calculate_zone5(vdot: float) -> Dict[str, Any]:
    return {"vo2_range": "95-100%", "description": "Repetition/speed"}

def estimate_vdot_from_race_time(distance: str, time: str) -> float:
    """Estimate VDOT from race time (simplified)."""
    # Parse time (mm:ss or mm:ss.ss)
    minutes, seconds = map(float, time.split(":"))
    total_seconds = minutes * 60 + seconds

    # Simplified VDOT estimation (would use Daniels' formulas in production)
    if distance == "5k":
        return 50.0 - (total_seconds - 1200) / 30  # Rough approximation
    elif distance == "10k":
        return 50.0 - (total_seconds - 2400) / 60
    else:
        return 45.0