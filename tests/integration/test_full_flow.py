"""Integration tests for full training program generation flow."""
import pytest
from router import TrainingAdvisorRouter


class TestFullStrengthProgramFlow:
    """Test complete strength training program flow."""

    def test_full_strength_program_flow(self):
        """Test complete strength program generation from user input."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm a beginner wanting to get stronger")

        assert "program" in result
        assert "analysis" in result
        assert result["program"]["type"] == "strength"
        assert result["analysis"]["experience_level"] == "beginner"
        assert result["analysis"]["goal"] == "strength"

    def test_full_strength_program_with_progression(self):
        """Test strength program includes proper progression."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm an intermediate lifter who wants to build strength")

        program = result["program"]
        assert "weeks" in program
        assert len(program["weeks"]) > 1

        # Check that program has weeks with progression structure
        # For DUP, progression is in the weekly pattern
        if program.get("periodization_model") == "undulating":
            assert "weekly_pattern" in program
        elif program.get("periodization_model") == "linear":
            # Linear periodization should have intensity progression
            weeks_with_intensity = [w for w in program["weeks"] if "intensity_level" in w]
            if len(weeks_with_intensity) >= 2:
                first_intensity = weeks_with_intensity[0]["intensity_level"]
                last_intensity = weeks_with_intensity[-1]["intensity_level"]
                assert last_intensity >= first_intensity

    def test_full_strength_program_advanced(self):
        """Test advanced strength program generation."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm an advanced powerlifter training for a meet")

        assert result["program"]["type"] == "strength"
        assert result["analysis"]["experience_level"] == "advanced"

    def test_full_strength_program_hypertrophy(self):
        """Test hypertrophy-focused strength program."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I want to build muscle size")

        assert result["program"]["type"] == "strength"
        assert result["analysis"]["goal"] == "hypertrophy"


class TestFullRunningProgramFlow:
    """Test complete running training program flow."""

    def test_full_running_program_flow(self):
        """Test complete running program generation."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I want to train for a 5K race")

        assert "program" in result
        assert result["program"]["type"] == "running"
        assert result["analysis"]["goal"] == "5k"

    def test_full_running_program_10k(self):
        """Test 10K running program generation."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm training for a 10K race")

        assert result["program"]["type"] == "running"
        assert result["analysis"]["goal"] == "10k"

    def test_full_running_program_half_marathon(self):
        """Test half marathon program generation."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I want to run a half marathon")

        assert result["program"]["type"] == "running"
        assert result["analysis"]["goal"] == "half_marathon"

    def test_full_running_program_marathon(self):
        """Test marathon program generation."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm training for my first marathon")

        assert result["program"]["type"] == "running"
        assert result["analysis"]["goal"] == "marathon"

    def test_full_running_program_with_progression(self):
        """Test running program includes proper structure."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm a beginner training for a 5K")

        program = result["program"]
        assert "weeks" in program
        assert len(program["weeks"]) > 1

        # Running programs use polarized distribution instead of intensity progression
        assert "polarized_distribution" in program
        assert program["polarized_distribution"] == "80/20"


class TestRecoveryRouting:
    """Test recovery program routing."""

    def test_recovery_routing_medical_concern(self):
        """Test routing to recovery with medical concern."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I have a heart condition and want to train")

        assert "program" in result
        assert result["program"]["type"] == "recovery"
        assert "medical_concern" in result["analysis"]["flags"]

    def test_recovery_routing_exhaustion(self):
        """Test routing to recovery when exhausted."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I've been feeling exhausted and want to train")

        assert "program" in result
        assert result["program"]["type"] == "recovery"
        assert "recovery_concern" in result["analysis"]["flags"]

    def test_recovery_routing_injury(self):
        """Test routing to recovery with injury."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I have a knee injury and want to maintain fitness")

        assert "program" in result
        # With injury, should still route to recovery or general
        assert result["program"]["type"] in ["recovery", "general"]
        assert "injury" in result["analysis"]["flags"]

    def test_recovery_program_structure(self):
        """Test recovery program has proper structure."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm overtrained and need to recover")

        program = result["program"]
        assert "type" in program
        assert "weeks" in program
        assert len(program["weeks"]) > 0


class TestSessionManagement:
    """Test session management across requests."""

    def test_session_id_generation(self):
        """Test session ID is generated."""
        router = TrainingAdvisorRouter()
        assert router.session_id is not None
        assert isinstance(router.session_id, str)

    def test_session_id_custom(self):
        """Test custom session ID."""
        router = TrainingAdvisorRouter(session_id="custom-session-123")
        assert router.session_id == "custom-session-123"

    def test_iteration_counting(self):
        """Test iteration count increments."""
        router = TrainingAdvisorRouter()
        result1 = router.process_request("I want to get stronger")
        result2 = router.process_request("I want to get stronger")

        assert result1["iteration"] == 1
        assert result2["iteration"] == 2

    def test_session_history_tracking(self):
        """Test session tracks program history."""
        router = TrainingAdvisorRouter()
        router.process_request("I want to get stronger")
        router.process_request("I want to run a 5K")

        assert len(router.session["program_history"]) == 2
        assert router.session["program_history"][0]["methodology"] == "strength"
        assert router.session["program_history"][1]["methodology"] == "running"

    def test_session_analysis_storage(self):
        """Test session stores user analysis."""
        router = TrainingAdvisorRouter()
        router.process_request("I'm a beginner wanting to get stronger")

        user_profile = router.session["user_profile"]
        assert user_profile["experience_level"] == "beginner"
        assert user_profile["goal"] == "strength"


class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling."""

    def test_empty_input(self):
        """Test handling of empty input."""
        router = TrainingAdvisorRouter()
        result = router.process_request("")

        # Should still return valid structure
        assert "program" in result
        assert "analysis" in result

    def test_ambiguous_input(self):
        """Test handling of ambiguous input."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I want to exercise")

        # Should route to general or make reasonable default
        assert "program" in result
        assert result["program"]["type"] in ["general", "strength"]

    def test_conflicting_goals(self):
        """Test handling of conflicting goals."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I want to build strength and run a marathon")

        # Should pick one based on routing logic
        assert "program" in result
        assert result["program"]["type"] in ["strength", "running"]

    def test_multiple_sessions_independent(self):
        """Test multiple sessions are independent."""
        router1 = TrainingAdvisorRouter()
        router2 = TrainingAdvisorRouter()

        result1 = router1.process_request("I want to get stronger")
        result2 = router2.process_request("I want to run a 5K")

        assert router1.session_id != router2.session_id
        assert result1["iteration"] == 1
        assert result2["iteration"] == 1
        assert router1.session["iteration_count"] == 1
        assert router2.session["iteration_count"] == 1


class TestIntegrationWithOutputFormatter:
    """Test integration with output formatter."""

    def test_formatted_output_structure(self):
        """Test complete formatted output structure."""
        from validators.output_formatter import format_program_output

        router = TrainingAdvisorRouter()
        raw_result = router.process_request("I'm a beginner wanting to get stronger")

        formatted = format_program_output(
            raw_result["program"],
            raw_result["analysis"]
        )

        assert "disclaimer" in formatted
        assert "user_analysis" in formatted
        assert "safety_warnings" in formatted
        assert "next_steps" in formatted
        assert "generated_at" in formatted

    def test_safety_warnings_in_formatted_output(self):
        """Test safety warnings appear in formatted output."""
        from validators.output_formatter import format_program_output

        router = TrainingAdvisorRouter()
        raw_result = router.process_request("I have a knee injury and want to get stronger")

        formatted = format_program_output(
            raw_result["program"],
            raw_result["analysis"]
        )

        # Should include injury warning
        warnings = formatted["safety_warnings"]
        assert len(warnings) > 0

    def test_complete_flow_with_validation(self):
        """Test complete flow from input to validated formatted output."""
        from validators.program_validator import validate_program
        from validators.output_formatter import format_program_output

        router = TrainingAdvisorRouter()
        raw_result = router.process_request("I'm a beginner wanting to get stronger")

        # Validate program
        validation = validate_program(raw_result["program"])
        assert validation["valid"] is True

        # Format output
        formatted = format_program_output(
            raw_result["program"],
            raw_result["analysis"]
        )

        assert "disclaimer" in formatted
        assert "program" in formatted


class TestProgramValidationIntegration:
    """Test program validation in full flow."""

    def test_generated_program_is_valid(self):
        """Test generated programs pass validation."""
        from validators.program_validator import validate_program

        router = TrainingAdvisorRouter()

        # Test various input types that should generate valid programs
        test_inputs = [
            "I'm a beginner wanting to get stronger",  # strength - has intensity in weeks
            "I'm an intermediate lifter wanting to build strength",  # strength - DUP model
            "I want to build muscle and get stronger"  # strength - hypertrophy
        ]

        for user_input in test_inputs:
            result = router.process_request(user_input)
            validation = validate_program(result["program"])

            # All generated programs should be valid
            assert validation["valid"] is True, f"Program failed validation for input: {user_input}. Issues: {validation['issues']}"
            assert len(validation["issues"]) == 0

    def test_program_has_required_fields(self):
        """Test generated programs have all required fields."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm a beginner wanting to get stronger")

        program = result["program"]

        assert "type" in program
        assert "experience_level" in program
        assert "weeks" in program
        assert len(program["weeks"]) > 0

    def test_program_has_progression(self):
        """Test generated programs include progression."""
        router = TrainingAdvisorRouter()
        result = router.process_request("I'm a beginner wanting to get stronger")

        program = result["program"]
        weeks = program["weeks"]

        assert len(weeks) > 1

        # For linear periodization (beginner), check intensity progression
        if program.get("periodization_model") == "linear":
            weeks_with_intensity = [w for w in weeks if "intensity_level" in w]
            if len(weeks_with_intensity) >= 2:
                first_intensity = weeks_with_intensity[0]["intensity_level"]
                last_intensity = weeks_with_intensity[-1]["intensity_level"]
                assert last_intensity > first_intensity, "Linear periodization should have intensity progression"
