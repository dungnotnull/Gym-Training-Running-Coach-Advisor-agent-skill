import re
from typing import Dict, List

BEGINNER_PATTERNS = [
    r"new|beginner|just starting|never.*before|first time",
    r"0.*months?|less than.*year"
]

INTERMEDIATE_PATTERNS = [
    r"\d+\s*year[s]?",
    r"\d+\s*month[s]?.*consistently",
    r"intermediate|some experience"
]

ADVANCED_PATTERNS = [
    r"[3-9]\+.*years?|advanced|competitive|elite",
    r"[3-9]\s*years?|10\+.*years?",
    r"trained for.*long time"
]

def classify_experience(user_input: str) -> str:
    """Classify user experience level."""
    user_input_lower = user_input.lower()

    for pattern in ADVANCED_PATTERNS:
        if re.search(pattern, user_input_lower):
            return "advanced"

    for pattern in BEGINNER_PATTERNS:
        if re.search(pattern, user_input_lower):
            return "beginner"

    for pattern in INTERMEDIATE_PATTERNS:
        if re.search(pattern, user_input_lower):
            return "intermediate"

    return "intermediate"

GOAL_PATTERNS = {
    "strength": [r"stronger|strength|squat|bench|deadlift|power"],
    "hypertrophy": [r"muscle|mass|bigger|hypertrophy|size|grow"],
    "5k": [r"5k|5k|5 kilometer"],
    "10k": [r"10k|10 kilometer"],
    "half_marathon": [r"half marathon|half marathon|13.1"],
    "marathon": [r"marathon|26.2|full marathon"],
    "general": [r"fit|fitness|health|overall|general"]
}

def classify_goal(user_input: str) -> str:
    """Classify training goal from user input."""
    user_input_lower = user_input.lower()

    for goal in ["half_marathon", "marathon", "10k", "5k"]:
        for pattern in GOAL_PATTERNS[goal]:
            if re.search(pattern, user_input_lower):
                return goal

    if any(re.search(p, user_input_lower) for p in GOAL_PATTERNS["strength"]):
        return "strength"
    if any(re.search(p, user_input_lower) for p in GOAL_PATTERNS["hypertrophy"]):
        return "hypertrophy"

    return "general"


def extract_constraints(user_input: str) -> Dict[str, any]:
    """Extract training constraints from user input."""
    user_input_lower = user_input.lower()

    constraints = {
        "time_available": None,
        "equipment": [],
        "health_conditions": []
    }

    # Extract time availability
    time_pattern = r"(\d+)\s*(days?|times?|sessions?)\s*(per week|weekly|a week)"
    time_match = re.search(time_pattern, user_input_lower)
    if time_match:
        constraints["time_available"] = f"{time_match.group(1)} days per week"

    # Extract equipment
    equipment_keywords = ["barbell", "dumbbell", "bench", "squat rack", "pull-up bar",
                        "cables", "machine", "kettlebell", "resistance band"]
    for equipment in equipment_keywords:
        if equipment in user_input_lower or equipment.replace(" ", "") in user_input_lower.replace(" ", ""):
            constraints["equipment"].append(equipment)

    # Extract health conditions
    health_keywords = ["shoulder", "knee", "back", "hip", "ankle", "wrist",
                     "injury", "pain", "condition"]
    for keyword in health_keywords:
        if keyword in user_input_lower:
            constraints["health_conditions"].append(keyword)

    return constraints

