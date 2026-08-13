"""
Pre-Processing Hooks

Execute before program generation to validate input and check safety.

Based on research:
- ACSM guidelines for exercise prescription
- Safety screening requirements
- Medical clearance validation

References:
- ACSM (2009). Progression models in resistance training.
- ACSM (2011). Quantity and Quality of Exercise.
"""

from typing import Dict, Any, List, Callable
from config import config


class PreProcessingHooks:
    """Pre-processing hooks for input validation and safety checks."""

    def __init__(self):
        self.hooks = {
            "before_program_generation": []
        }
        self.enabled = config.get("hooks.before_program_generation.enabled", True)

    def register_hook(self, hook_name: str, func: Callable) -> bool:
        """Register a pre-processing hook function."""
        if hook_name in self.hooks:
            self.hooks[hook_name].append(func)
            return True
        return False

    def execute_hooks(self, hook_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute all registered hooks for a given hook point."""
        if not self.enabled:
            return {"status": "disabled"}

        results = []
        for hook in self.hooks.get(hook_name, []):
            try:
                result = hook(context)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})

        return {
            "hook_name": hook_name,
            "results": results,
            "all_passed": all(r.get("status", "success") == "success" for r in results)
        }


def validate_input_completeness(user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that user input contains necessary information.

    Research: ACSM guidelines for exercise prescription require goals and experience level.
    """
    input_lower = user_input.lower()

    # Check for minimum requirements
    has_experience = any([
        "beginner" in input_lower or "new" in input_lower or "just starting" in input_lower,
        "intermediate" in input_lower or "some experience" in input_lower,
        "advanced" in input_lower or "trained for" in input_lower or "year" in input_lower
    ])

    has_goal = any([
        "strength" in input_lower or "stronger" in input_lower or "squat" in input_lower,
        "muscle" in input_lower or "hypertrophy" in input_lower or "mass" in input_lower,
        "run" in input_lower or "5k" in input_lower or "10k" in input_lower,
        "marathon" in input_lower or "half marathon" in input_lower,
        "fit" in input_lower or "fitness" in input_lower or "general" in input_lower
    ])

    if not has_experience:
        return {
            "status": "failed",
            "message": "Training experience level not specified",
            "required": "Please provide your training experience (beginner, intermediate, or advanced)"
        }

    if not has_goal:
        return {
            "status": "failed",
            "message": "Training goal not specified",
            "required": "Please provide your training goal (strength, running distance, etc.)"
        }

    return {"status": "success", "experience_detected": has_experience, "goal_detected": has_goal}


def check_medical_clearance_flags(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check for medical concern flags requiring physician clearance.

    Research: Safety screening requirement (ACSM, 2011)
    """
    analysis = context.get("analysis", {})
    flags = analysis.get("flags", [])

    medical_concerns = ["medical_concern"]
    serious_conditions = ["heart condition", "diabetes", "hypertension", "asthma"]

    user_input = analysis.get("raw_input", "").lower()

    has_concern = any(flag in flags for flag in medical_concerns)
    has_condition = any(condition in user_input for condition in serious_conditions)

    if has_concern or has_condition:
        return {
            "status": "warning",
            "requires_clearance": True,
            "message": "Medical concern detected",
            "recommendation": "Please consult with a physician before starting any new exercise program"
        }

    return {"status": "success", "clearance": "not_required"}


def detect_contradictions(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect contradictory information in user input.

    Examples: "I'm brand new but I've been training 5 years"
    """
    analysis = context.get("analysis", {})
    user_input = analysis.get("raw_input", "")
    experience = analysis.get("experience_level", "")

    # Check for experience contradictions
    if experience == "beginner":
        contradictions = [
            ("training for", "year"),
            ("consistent", "month"),
            ("advanced", "experience")
        ]
        for term in contradictions:
            if term in user_input.lower():
                return {
                    "status": "warning",
                    "message": f"Possible contradiction: experience '{experience}' but '{term}' detected",
                    "action": "Clarify training experience before proceeding"
                }

    return {"status": "success", "contradictions": None}


# Hook registry
pre_processing_hooks = PreProcessingHooks()
pre_processing_hooks.register_hook("before_program_generation", validate_input_completeness)
pre_processing_hooks.register_hook("before_program_generation", check_medical_clearance_flags)
pre_processing_hooks.register_hook("before_program_generation", detect_contradictions)