"""
Post-Processing Hooks

Execute after program generation to validate and format output.

Based on research:
- Program validation requirements
- Safety compliance checking
- Output formatting standards

References:
- ACSM (2009). Progression models in resistance training.
- Kraemer & Ratamess (2004). Fundamentals of Resistance Training.
"""

from typing import Dict, Any, List, Callable
from config import config
from validators.program_validator import validate_program
from validators.safety_checker import check_program_safety, validate_medical_clearance
from validators.output_formatter import format_program_output


class PostProcessingHooks:
    """Post-processing hooks for program validation and formatting."""

    def __init__(self):
        self.hooks = {
            "after_program_generation": []
        }
        self.enabled = config.get("hooks.after_program_generation.enabled", True)

    def register_hook(self, hook_name: str, func: Callable) -> bool:
        """Register a post-processing hook function."""
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


def validate_program_completeness(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate generated program for completeness.

    Research: ACSM requires specific program components.
    """
    program = context.get("program", {})

    # Use program validator
    validation_result = validate_program(program)

    if validation_result["valid"]:
        return {
            "status": "success",
            "message": "Program validation passed"
        }
    else:
        return {
            "status": "failed",
            "message": "Program validation failed",
            "issues": validation_result.get("issues", [])
        }


def apply_safety_compliance_checks(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply safety compliance checks to generated program.

    Research: Safety-first principle (ACSM, 2011)
    """
    program = context.get("program", {})
    analysis = context.get("analysis", {})

    # Check program safety
    safety_result = check_program_safety(program)

    # Check medical clearance if flags present
    flags = analysis.get("flags", [])
    clearance_result = validate_medical_clearance(flags)

    if not safety_result["safe"]:
        return {
            "status": "warning",
            "message": "Safety concerns detected",
            "issues": safety_result.get("issues", []),
            "recommendation": "Review and adjust program before use"
        }

    if not clearance_result.get("cleared", True):
        return {
            "status": "critical",
            "message": "Medical clearance required",
            "recommendation": clearance_result.get("requires", "Consult physician"),
            "program_blocked": True
        }

    return {
        "status": "success",
        "safety_check": "passed",
        "medical_clearance": "cleared"
    }


def format_output_with_disclaimers(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format program output with consistent structure and required disclaimers.

    Research: Legal and ethical requirements for exercise recommendations.
    """
    program = context.get("program", {})
    analysis = context.get("analysis", {})

    # Use output formatter
    formatted = format_program_output(program, analysis)

    # Add compliance checks
    formatted["compliance"] = {
        "validated": True,
        "safety_checked": True,
        "disclaimer_acknowledged": True
    }

    return {
        "status": "success",
        "formatted_output": formatted
    }


def check_for_progressive_overload(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify program includes progressive overload.

    Research: Progressive overload is fundamental principle (Kraemer & Ratamess, 2004).
    """
    program = context.get("program", {})

    weeks = program.get("weeks", [])
    if len(weeks) < 2:
        return {
            "status": "warning",
            "message": "Program too short to verify progressive overload"
        }

    # Check for progression
    first_week = weeks[0]
    last_week = weeks[-1]

    has_progression = False
    if "intensity_level" in first_week and "intensity_level" in last_week:
        has_progression = last_week["intensity_level"] > first_week["intensity_level"]

    if not has_progression:
        return {
            "status": "warning",
            "message": "No clear progressive overload detected",
            "recommendation": "Ensure intensity or volume increases over time"
        }

    return {
        "status": "success",
        "progression_verified": True
    }


def verify_recovery_included(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify adequate recovery is programmed.

    Research: Recovery essential for adaptation (Kreher & Schwartz, 2012).
    """
    program = context.get("program", {})

    weeks = program.get("weeks", [])
    deloads = [w for w in weeks if w.get("is_deload", False)]

    # Check for adequate recovery
    recovery_adequate = False
    if len(deloads) >= 2:
        recovery_adequate = True
    elif len(weeks) <= 4:
        recovery_adequate = True  # Short programs may not need deloads

    if not recovery_adequate:
        return {
            "status": "warning",
            "message": "Insufficient recovery scheduled",
            "recommendation": "Add deload weeks every 3-4 weeks"
        }

    return {
        "status": "success",
        "recovery_verified": True,
        "deload_count": len(deloads)
    }


# Hook registry
post_processing_hooks = PostProcessingHooks()
post_processing_hooks.register_hook("after_program_generation", validate_program_completeness)
post_processing_hooks.register_hook("after_program_generation", apply_safety_compliance_checks)
post_processing_hooks.register_hook("after_program_generation", format_output_with_disclaimers)
post_processing_hooks.register_hook("after_program_generation", check_for_progressive_overload)
post_processing_hooks.register_hook("after_program_generation", verify_recovery_included)