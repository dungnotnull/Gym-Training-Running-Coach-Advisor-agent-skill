"""
Error Handling Hooks

Graceful error handling and fallback mechanisms for production reliability.

Based on research:
- Recovery from training errors
- Alternative programming strategies

References:
- Safety principles in exercise prescription
"""

from typing import Dict, Any, List, Callable, Optional
from config import config
from datetime import datetime


class ErrorHandlers:
    """Error handling hooks for graceful fallbacks."""

    def __init__(self):
        self.hooks = {
            "on_error": []
        }
        self.enabled = config.get("hooks.on_error.enabled", True)
        self.error_log = []

    def register_hook(self, hook_name: str, func: Callable) -> bool:
        """Register an error handling hook function."""
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
            "resolution_available": any(r.get("resolution", False) for r in results)
        }


def log_error(error_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """Log error for monitoring and debugging."""
    error_entry = {
        "timestamp": datetime.now().isoformat(),
        "error_type": error_type,
        "session_id": context.get("session_id", "unknown"),
        "context": {
            "user_input": context.get("user_input", "")[:100],  # Truncate for log
            "analysis_keys": list(context.get("analysis", {}).keys())
        }
    }

    # In production, would write to error log file
    print(f"ERROR LOG: {error_entry}")

    return {
        "status": "logged",
        "entry": error_entry
    }


def handle_input_validation_error(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle input validation errors with user-friendly message.

    Tier 1 error: Insufficient input - request clarification.
    """
    missing_info = context.get("missing_information", [])

    return {
        "status": "resolution_available",
        "resolution_type": "request_clarification",
        "message": "I need a bit more information to create your program:",
        "required_information": missing_info,
        "examples": [
            "Please tell me your training experience level (beginner, intermediate, or advanced)",
            "What are your specific training goals?",
            "How many days per week can you train?"
        ]
    }


def handle_safety_concern(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle safety concerns with recommended professional consultation.

    Tier 3 error: Safety concerns - recommend professional.
    """
    flags = context.get("analysis", {}).get("flags", [])

    concern_type = None
    if "medical_concern" in flags:
        concern_type = "medical"
    elif "injury" in flags:
        concern_type = "injury"
    elif "eating_disorder_concern" in flags:
        concern_type = "eating_disorder"

    disclaimers = {
        "medical": """
**MEDICAL DISCLAIMER**

This program is for general information only and is not a substitute
for professional medical advice, diagnosis, or treatment.

Please consult with a physician or qualified healthcare provider before
starting any new exercise program, especially if you have medical
concerns or pre-existing conditions.
        """,
        "injury": """
**INJURY DISCLAIMER**

If you have an injury, please follow the guidance of your physical
therapist or healthcare provider.

This program should not replace professional medical treatment or
rehabilitation protocols.
        """,
        "eating_disorder": """
**EATING DISORDER DISCLAIMER**

If you're struggling with an eating disorder, please seek professional
help. Resources are available:

- National Eating Disorders Association (NEDA): neda.org
- Helpline: (800) 931-2237

This program focuses on healthy training and is not appropriate for
individuals with eating disorders.
        """
    }

    return {
        "status": "resolution_available",
        "resolution_type": "recommend_professional",
        "message": "Based on your input, I recommend consulting with a qualified professional",
        "concern_type": concern_type,
        "disclaimer": disclaimers.get(concern_type, "Please consult a healthcare professional."),
        "resources": _get_professional_resources(concern_type)
    }


def handle_methodology_error(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle methodology generation errors with fallback.

    Tier 2 error: System error - use fallback.
    """
    error = context.get("error", "Unknown error")
    analysis = context.get("analysis", {})

    # Fallback: Create simple program structure
    fallback_program = {
        "type": "general",
        "program_type": "fallback",
        "experience_level": analysis.get("experience_level", "intermediate"),
        "goal": analysis.get("goal", "general"),
        "weeks": _create_fallback_weeks(analysis),
        "note": "This is a simplified program generated due to technical issues.",
        "fallback_reason": error
    }

    return {
        "status": "resolution_available",
        "resolution_type": "use_fallback",
        "fallback_program": fallback_program,
        "message": "I've created a basic program structure. For a complete tailored program, we may need additional information."
    }


def handle_critical_failure(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle critical system failures.

    Tier 3 error: Critical error - recommend professional.
    """
    return {
        "status": "failed",
        "message": "I'm experiencing technical difficulties generating your program.",
        "recommendation": """
For immediate training guidance, please consult with:
- A certified personal trainer
- Sports medicine physician
- Registered dietitian for nutrition guidance

I apologize for the inconvenience.
        """,
        "error_code": "CRITICAL_FAILURE"
    }


def _create_fallback_weeks(analysis: Dict) -> List[Dict]:
    """Create simple fallback week structure."""
    days = ["monday", "wednesday", "friday"]
    weeks = []

    for week_num in range(1, 5):
        sessions = []
        for day in days:
            sessions.append({
                "day": day,
                "type": "easy",
                "focus": "General fitness"
            })

        weeks.append({
            "week_number": week_num,
            "sessions": sessions,
            "note": "Simplified structure - consult professional for complete program"
        })

    return weeks


def _get_professional_resources(concern_type: str) -> List[str]:
    """Get professional resources based on concern type."""
    resources = {
        "medical": [
            "Physician (MD) or Doctor of Osteopathic Medicine (DO)",
            "Sports Medicine Specialist",
            "Physical Therapist (PT)"
        ],
        "injury": [
            "Physical Therapist (PT)",
            "Sports Medicine Physician",
            "Athletic Trainer (ATC)"
        ],
        "eating_disorder": [
            "National Eating Disorders Association (NEDA): neda.org",
            "Helpline: (800) 931-2237",
            "Eating Disorders Hope: eatingdisorderhope.org"
        ]
    }

    return resources.get(concern_type, ["Healthcare Provider"])


# Hook registry
error_handlers = ErrorHandlers()
error_handlers.register_hook("on_error", log_error)
error_handlers.register_hook("on_error", handle_input_validation_error)
error_handlers.register_hook("on_error", handle_safety_concern)
error_handlers.register_hook("on_error", handle_methodology_error)
error_handlers.register_hook("on_error", handle_critical_failure)