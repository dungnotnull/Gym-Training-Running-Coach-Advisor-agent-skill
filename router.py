import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from methodologies.shared_utils import (
    classify_experience,
    classify_goal,
    extract_constraints,
    detect_safety_flags
)
import methodologies.strength_training as strength_training
import methodologies.running_training as running_training
import methodologies.recovery as recovery
import methodologies.general as general

class TrainingAdvisorRouter:
    """Main orchestrator for training program generation."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.session: Dict[str, Any] = {}
        self._init_session()

    def _init_session(self):
        """Initialize session structure."""
        self.session = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "user_profile": {},
            "program_history": [],
            "iteration_count": 0
        }

    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input and extract key information."""
        analysis = {
            "experience_level": classify_experience(user_input),
            "goal": classify_goal(user_input),
            "constraints": extract_constraints(user_input),
            "flags": detect_safety_flags(user_input),
            "raw_input": user_input
        }

        # Store in session
        self.session["user_profile"] = analysis

        return analysis

    def _select_methodology(self, analysis: Dict[str, Any]) -> str:
        """Select appropriate methodology based on analysis."""
        # Check for priority flags first
        if "recovery_concern" in analysis.get("flags", []):
            return "recovery"
        if "medical_concern" in analysis.get("flags", []):
            return "recovery"

        # Route by goal
        goal = analysis.get("goal", "general")

        if goal in ["strength", "hypertrophy"]:
            return "strength"
        elif goal in ["5k", "10k", "half_marathon", "marathon"]:
            return "running"
        else:
            return "general"

    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Main entry point for processing training program requests."""
        self.session["iteration_count"] += 1

        # Analyze input
        analysis = self.analyze_input(user_input)

        # Select methodology
        methodology = self._select_methodology(analysis)

        # Route to appropriate methodology
        if methodology == "strength":
            program = strength_training.generate_strength_program(analysis)
        elif methodology == "running":
            program = running_training.generate_running_program(analysis)
        elif methodology == "recovery":
            program = recovery.generate_recovery_plan(analysis)
        else:
            program = general.generate_general_program(analysis)

        # Update session history
        self.session["program_history"].append({
            "iteration": self.session["iteration_count"],
            "timestamp": datetime.now().isoformat(),
            "methodology": methodology,
            "program_summary": {
                "type": program.get("type"),
                "goal": analysis.get("goal")
            }
        })

        return {
            "program": program,
            "session_id": self.session_id,
            "iteration": self.session["iteration_count"],
            "analysis": analysis
        }
