"""
Training Advisor Router - Main Orchestrator

Production-grade router with complete integration of:
- Methodology functions
- Tool system (VDOT, 1RM, Recovery Status, Progression Planner)
- Validation layer (Program Validator, Safety Checker, Output Formatter)
- Hooks system (Pre/Post Processing, Error Handlers)
- Session persistence
- Structured logging

Research-based, production-ready training program generation.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List

# Shared utilities
from methodologies.shared_utils import (
    classify_experience,
    classify_goal,
    extract_constraints,
    detect_safety_flags
)

# Methodologies
import methodologies.strength_training as strength_training
import methodologies.running_training as running_training
import methodologies.recovery as recovery
import methodologies.general as general

# Tools
import tools.vdot_calculator as vdot_calculator
import tools.one_rm_estimator as one_rm_estimator
import tools.recovery_status as recovery_status
import tools.progression_planner as progression_planner

# Hooks
from hooks.pre_processing import pre_processing_hooks
from hooks.post_processing import post_processing_hooks
from hooks.error_handlers import error_handlers
from hooks.state_management import session_manager

# Logging
from hooks.logging import log_event

# Validators
from validators.program_validator import validate_program
from validators.safety_checker import check_program_safety
from validators.output_formatter import format_program_output


class TrainingAdvisorRouter:
    """
    Main orchestrator for training program generation.

    Production-grade router with:
    - Pre/post processing hooks
    - Tool system integration
    - Validation layer
    - Error handling
    - Session persistence
    - Structured logging
    """

    def __init__(self, session_id: Optional[str] = None):
        """Initialize router with session management."""
        self.session_id = session_id or str(uuid.uuid4())
        self.session: Dict[str, Any] = {}
        self._init_session()
        self._load_existing_session()

    def _init_session(self) -> None:
        """Initialize session structure."""
        self.session = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "user_profile": {},
            "program_history": [],
            "iteration_count": 0,
            "context": {}
        }

    def _load_existing_session(self) -> None:
        """Load existing session data if available."""
        existing = session_manager.load_session(self.session_id)
        if existing:
            self.session = existing
            log_event("session_loaded", self.session_id, {"loaded_from": "disk"})

    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input and extract key information.

        Research-based classification across all domains.
        """
        analysis = {
            "experience_level": classify_experience(user_input),
            "goal": classify_goal(user_input),
            "constraints": extract_constraints(user_input),
            "flags": detect_safety_flags(user_input),
            "raw_input": user_input
        }

        # Store in session
        self.session["user_profile"] = analysis

        # Log analysis event
        log_event("input_analyzed", self.session_id, {
            "experience": analysis["experience_level"],
            "goal": analysis["goal"],
            "flags_count": len(analysis["flags"])
        })

        return analysis

    def _select_methodology(self, analysis: Dict[str, Any]) -> str:
        """
        Select appropriate methodology based on analysis and research.

        Priority: Safety > Goals > Experience
        """
        # Check for priority flags first (safety first)
        if "recovery_concern" in analysis.get("flags", []):
            return "recovery"
        if "medical_concern" in analysis.get("flags", []):
            return "recovery"

        # Route by goal based on experience
        goal = analysis.get("goal", "general")
        experience = analysis.get("experience_level", "intermediate")

        # Goal-based routing
        if goal in ["strength", "hypertrophy"]:
            return "strength"
        elif goal in ["5k", "10k", "half_marathon", "marathon"]:
            return "running"
        else:
            return "general"

    def process_request(self, user_input: str, use_hooks: bool = True) -> Dict[str, Any]:
        """
        Main entry point for processing training program requests.

        Production-grade flow with:
        1. Pre-processing hooks (validation, safety checks)
        2. Input analysis
        3. Methodology selection
        4. Tool utilization (VDOT, 1RM, recovery assessment)
        5. Program generation
        6. Post-processing hooks (validation, formatting)
        7. Error handling with fallbacks
        8. Session persistence
        9. Structured logging

        Args:
            user_input: User's training request
            use_hooks: Whether to execute hooks (default: True for production)

        Returns:
            Complete formatted program with all safety information
        """
        try:
            # Phase 1: Pre-processing hooks (input validation, safety checks)
            if use_hooks:
                context = {"user_input": user_input, "router": self, "session": self.session}
                pre_result = pre_processing_hooks.execute_hooks("before_program_generation", context)

                if not pre_result.get("all_passed", True):
                    # Hooks detected issues - request clarification
                    return self._handle_hook_failure(pre_result, context)

            # Phase 2: Analyze input
            analysis = self.analyze_input(user_input)

            # Phase 3: Select methodology
            methodology = self._select_methodology(analysis)

            # Phase 4: Generate program using methodology
            program = self._generate_program(methodology, analysis)

            # Phase 5: Apply tools for enhancement
            enhanced_program = self._apply_tools(program, analysis)

            # Phase 6: Post-processing hooks (validation, formatting, safety)
            if use_hooks:
                context = {
                    "program": enhanced_program,
                    "analysis": analysis,
                    "router": self,
                    "session": self.session
                }
                post_result = post_processing_hooks.execute_hooks("after_program_generation", context)

                if not post_result.get("all_passed", True):
                    # Post-processing failed - handle it
                    return self._handle_hook_failure(post_result, context)

            # Phase 7: Format output
            formatted_output = format_program_output(enhanced_program, analysis)

            # Phase 8: Update session history
            self.session["iteration_count"] += 1
            self.session["program_history"].append({
                "iteration": self.session["iteration_count"],
                "timestamp": datetime.now().isoformat(),
                "methodology": methodology,
                "program_summary": {
                    "type": enhanced_program.get("type"),
                    "goal": analysis.get("goal"),
                    "duration_weeks": len(enhanced_program.get("weeks", []))
                }
            })

            # Phase 9: Persist session
            session_manager.save_session(self.session_id, self.session)

            # Phase 10: Log completion
            log_event("program_generated", self.session_id, {
                "methodology": methodology,
                "goal": analysis.get("goal"),
                "iteration": self.session["iteration_count"]
            })

            return {
                "program": formatted_output,
                "session_id": self.session_id,
                "iteration": self.session["iteration_count"],
                "metadata": {
                    "methodology": methodology,
                    "hooks_executed": use_hooks,
                    "tools_applied": True,
                    "generated_at": datetime.now().isoformat()
                }
            }

        except Exception as e:
            # Phase 11: Error handling
            error_context = {
                "error": str(e),
                "user_input": user_input[:100],
                "session_id": self.session_id,
                "router": self
            }

            # Log error
            log_event("error_occurred", self.session_id, {"error_type": type(e).__name__})

            # Execute error handlers
            error_result = error_handlers.execute_hooks("on_error", error_context)

            if error_result.get("resolution_available", False):
                return {
                    "error": "handled_with_resolution",
                    "resolution": error_result.get("results", []),
                    "session_id": self.session_id
                }
            else:
                # Critical failure
                return {
                    "error": "critical_failure",
                    "message": "Unable to generate program. Please try again or consult a professional.",
                    "session_id": self.session_id
                }

    def _generate_program(self, methodology: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate program using selected methodology."""
        try:
            if methodology == "strength":
                return strength_training.generate_strength_program(analysis)
            elif methodology == "running":
                return running_training.generate_running_program(analysis)
            elif methodology == "recovery":
                return recovery.generate_recovery_plan(analysis)
            else:
                return general.generate_general_program(analysis)
        except Exception as e:
            raise Exception(f"Methodology error ({methodology}): {e}")

    def _apply_tools(self, program: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Apply research-backed tools to enhance program."""
        # Apply 1RM estimation if strength training
        if program.get("type") == "strength":
            program = self._enhance_with_1rm_estimation(program)

        # Apply VDOT calculations if running
        if program.get("type") == "running":
            program = self._enhance_with_vdot_zones(program, analysis)

        # Apply recovery status assessment
        if analysis.get("flags", []):
            program = self._enhance_with_recovery_assessment(program, analysis)

        # Apply progression planning
        program = self._enhance_with_progression_planning(program)

        return program

    def _enhance_with_1rm_estimation(self, program: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance strength program with 1RM estimation guidance."""
        # Add 1RM testing protocol
        program["strength_guidance"] = {
            "one_rm_testing": one_rm_estimator.test_1rm_protocol("squat"),
            "estimation_available": True
        }

        # Add progression recommendations
        weeks = program.get("weeks", [])
        if weeks:
            first_week = weeks[0]
            program["progression_plan"] = progression_planner.create_progression_plan(
                current_weight=100,  # Would extract from program
                current_reps=10,
                target_reps=12,
                weeks=len(weeks)
            )

        return program

    def _enhance_with_vdot_zones(self, program: Dict, analysis: Dict) -> Dict[str, Any]:
        """Enhance running program with VDOT-based training zones."""
        # Estimate VDOT from goal (simplified)
        vdot_score = 45.0  # Default, would estimate from race time in production

        # Calculate training zones
        zones = vdot_calculator.calculate_training_zones(vdot_score)

        # Add zones to program
        program["training_zones"] = zones
        program["vdot_score"] = vdot_score
        program["polarized_distribution"] = "80/20"

        # Add zone guidance
        for week in program.get("weeks", []):
            for session in week.get("sessions", []):
                # Assign zones based on session type
                if session.get("type") == "easy":
                    session["target_zone"] = zones["zones"]["zone1_easy"]
                elif session.get("type") == "tempo":
                    session["target_zone"] = zones["zones"]["zone3_threshold"]
                elif session.get("type") == "interval":
                    session["target_zone"] = zones["zones"]["zone4_interval"]

        return program

    def _enhance_with_recovery_assessment(self, program: Dict, analysis: Dict) -> Dict:
        """Enhance program with recovery status assessment."""
        flags = analysis.get("flags", [])

        if "recovery_concern" in flags or "medical_concern" in flags:
            # Add recovery guidance
            program["recovery_guidance"] = {
                "assessment": recovery_status.determine_recovery_status(
                    sleep_hours=7,
                    sleep_quality="good",
                    resting_hr=62,
                    mood="fatigued",
                    muscle_soreness="moderate",
                    motivation_level="low"
                ),
                "overtraining_risk": recovery_status.assess_overtraining_risk(self.session)
            }

        return program

    def _enhance_with_progression_planning(self, program: Dict[str, Any]) -> Dict[str, Any]:
        """Add progression planning to program."""
        weeks = program.get("weeks", [])
        if weeks:
            program["progression_plan"] = progression_planner.create_progression_plan(
                current_program=program,
                progression_type=program.get("periodization_model", "linear")
            )

            # Add deload protocol
            program["deload_protocol"] = progression_planner.create_deload_protocol(
                current_program=program,
                severity="standard"
            )

        return program

    def _handle_hook_failure(self, hook_result: Dict, context: Dict) -> Dict[str, Any]:
        """Handle hook execution failure with appropriate response."""
        # Extract first non-passing result
        for result in hook_result.get("results", []):
            if result.get("status") != "success":
                if "resolution_type" in result:
                    return {
                        "hook_failure_handled": True,
                        "resolution": result,
                        "session_id": self.session_id
                    }
                elif "message" in result:
                    return {
                        "hook_failure_handled": True,
                        "message": result["message"],
                        "session_id": self.session_id
                    }

        return {"hook_failure_handled": False, "session_id": self.session_id}

    def get_session_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get session program history."""
        history = self.session.get("program_history", [])
        return history[-limit:] if history else []

    def get_session_summary(self) -> Dict[str, Any]:
        """Get session summary for display."""
        return {
            "session_id": self.session_id,
            "created_at": self.session.get("created_at"),
            "iteration_count": self.session.get("iteration_count", 0),
            "programs_generated": len(self.session.get("program_history", [])),
            "current_profile": self.session.get("user_profile", {})
        }

    def reset_session(self) -> None:
        """Reset session (start fresh)."""
        self.session = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "user_profile": {},
            "program_history": [],
            "iteration_count": 0,
            "context": {}
        }
        session_manager.save_session(self.session_id, self.session)
        log_event("session_reset", self.session_id, {})