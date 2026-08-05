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


