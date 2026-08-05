# Gym Training & Running Coach Advisor - Production Upgrade Design

**Date:** 2026-08-05
**Status:** Approved
**Version:** 1.0.0

## Executive Summary

Complete upgrade of the Gym Training & Running Coach Advisor skill to production-grade, open-source standards. Implements a lightweight Router Pattern architecture with domain-specialized methodology functions, comprehensive tool system, validation layer, and production-ready error handling.

## Architecture Overview

### Pattern Selection: Router with Methodology Functions

Selected architecture balances modularity, maintainability, and extensibility:

- **Main Router:** Lightweight orchestrator for request analysis and methodology routing
- **Methodology Functions:** Domain-specific logic in separate, testable modules
- **Tool System:** Reusable calculators and validators with JSON schema validation
- **Validation Layer:** Quality assurance with safety checks and output formatting
- **Hooks System:** Lifecycle hooks for pre-processing, post-processing, and error handling

### Component Architecture

```
TrainingAdvisorRouter (Main Orchestrator)
├── Analysis Layer
│   ├── Experience Classification (beginner/intermediate/advanced)
│   ├── Goal Detection (strength/hypertrophy/running/endurance)
│   ├── Constraint Extraction (time, equipment, health)
│   └── Flag Detection (safety concerns, recovery needs)
│
├── Methodology Router
│   ├── Strength Training (linear/undulating/block periodization)
│   ├── Running Training (polarized model, VDOT-based zones)
│   ├── Recovery Monitoring (overtraining detection, deloads)
│   └── General Fitness (balanced programming)
│
├── Tool System
│   ├── VDOT Calculator (training zones from race times)
│   ├── 1RM Estimator (Epley formula, training percentages)
│   ├── Recovery Status (sleep, RHR, mood assessment)
│   └── Progression Planner (overload protocols)
│
├── Validation Layer
│   ├── Program Validator (completeness, methodology compliance)
│   ├── Safety Checker (contraindications, warning signs)
│   └── Output Formatter (consistent structure, disclaimers)
│
└── Hooks System
    ├── Pre-processing (input validation, safety checks)
    ├── Post-processing (validation, formatting)
    ├── Error Handlers (graceful fallbacks)
    └── State Management (session persistence)
```

## Data Flow

```
User Request
    ↓
[Pre-processing Hook: before_program_generation]
- Validate input completeness
- Check for safety concerns
- Verify experience classification
    ↓
Analysis Layer
- classify_experience()
- classify_goal()
- extract_constraints()
- detect_safety_flags()
    ↓
Methodology Selection
- Route to appropriate methodology based on analysis
- Load methodology module on-demand
    ↓
Methodology Execution
- Call tools as needed (VDOT, 1RM, Recovery Status)
- Apply methodology-specific logic
- Use reference knowledge for principles
- Apply templates for structure
- Return raw program
    ↓
[Post-processing Hook: after_program_generation]
- Validate program completeness
- Apply consistent formatting
- Add required disclaimers
- Check safety compliance
    ↓
Validation Layer
- program_validator.validate()
- safety_checker.check()
- output_formatter.format()
    ↓
Final Output
- Structured program with all required elements
- Disclaimers prominent
- Safety warnings included
- Consistent format
```

## File Structure

```
gym-running-training-advisor/
├── SKILL.md                          # Main skill entry point
├── CLAUDE.md                         # Project instructions
├── PROJECT-detail.md                 # Project specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md
├── README.md                         # Main documentation
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
├── CHANGELOG.md                      # Version history
│
├── router.py                         # Main orchestrator
│
├── methodologies/                    # Domain logic
│   ├── __init__.py
│   ├── strength_training.py         # Strength periodization models
│   ├── running_training.py          # Running & polarized training
│   ├── recovery.py                  # Recovery & overtraining
│   ├── general.py                    # General fitness
│   ├── shared_utils.py              # Common utilities
│   └── templates/
│       ├── strength_programs.md
│       ├── running_programs.md
│       └── recovery_protocols.md
│
├── tools/                            # Executable tools
│   ├── __init__.py
│   ├── vdot_calculator.py           # VDOT zone calculator
│   ├── one_rm_estimator.py          # 1RM estimation
│   ├── recovery_status.py           # Recovery assessment
│   └── progression_planner.py       # Progressive overload plans
│
├── validators/                       # Quality layer
│   ├── __init__.py
│   ├── program_validator.py         # Program validation
│   ├── safety_checker.py            # Safety compliance
│   └── output_formatter.py          # Output formatting
│
├── hooks/                            # Hook implementations
│   ├── __init__.py
│   ├── pre_processing.py            # Input validation hooks
│   ├── post_processing.py           # Output validation hooks
│   ├── error_handlers.py            # Error handling hooks
│   └── state_management.py          # Session state hooks
│
├── config/
│   ├── settings.json                 # Type-safe configuration
│   └── hooks-system.md              # Hooks system documentation
│
├── references/                       # Knowledge base
│   ├── progressive-overload.md
│   ├── periodization-models.md
│   ├── running-training.md
│   ├── recovery-monitoring.md
│   ├── acsm-guidelines.md
│   └── warming-up-mobility.md
│
├── assets/
│   ├── schemas/                      # JSON schemas for validation
│   │   ├── training-zones-schema.json
│   │   ├── 1rm-estimation-schema.json
│   │   ├── recovery-status-schema.json
│   │   └── progression-plan-schema.json
│   └── templates/                    # Output templates
│       ├── program_output.md
│       └── error_messages.md
│
├── scripts/                          # Automation utilities
│   ├── setup_environment.py
│   ├── validate_schemas.py
│   ├── run_tests.py
│   ├── package_skill.py
│   └── seed_database.py
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_router.py
│   ├── test_methodologies/
│   │   ├── test_strength_training.py
│   │   ├── test_running_training.py
│   │   └── test_recovery.py
│   ├── test_tools/
│   ├── test_validators/
│   └── integration/
│       └── test_full_flow.py
│
└── docs/                             # Documentation
    ├── architecture.md
    ├── api_reference.md
    ├── extension_guide.md
    └── examples/
```

## Phase-by-Phase Implementation

### Phase 1: Foundation (Core Router & Analysis)

**Components:**
- `router.py` - TrainingAdvisorRouter class with request processing
- `methodologies/shared_utils.py` - Classification and utility functions
- `config/settings.json` - Configuration management
- `hooks/pre_processing.py` - Input validation hooks
- `hooks/error_handlers.py` - Error handling hooks

**Key Functions:**
```python
def classify_experience(user_input: str) -> str
    # Returns: 'beginner' | 'intermediate' | 'advanced'

def classify_goal(user_input: str) -> str
    # Returns: 'strength' | 'hypertrophy' | '5k' | '10k' | 'half_marathon' | 'marathon'

def extract_constraints(user_input: str) -> dict
    # Returns: {time_available, equipment, health_conditions}

def detect_safety_flags(user_input: str) -> list
    # Returns: [medical_concerns, injuries, recovery_issues]
```

**Deliverable:** Working router that analyzes and classifies user requests.

**Testing:** Test all classification functions with various inputs.

---

### Phase 2: Periodization Models

**Components:**
- `methodologies/strength_training.py` - Complete strength training methodology
- `methodologies/templates/strength_programs.md` - Program templates
- Update references for implementation guidance

**Functions:**
```python
def generate_strength_program(analysis: dict) -> dict
    # Routes to appropriate periodization model

def build_linear_program(analysis: dict) -> dict
    # Beginner-focused, progressive intensity

def build_undulating_program(analysis: dict) -> dict
    # Intermediate DUP pattern (heavy/medium/light)

def build_block_program(analysis: dict) -> dict
    # Advanced accumulation/transmutation/realization
```

**Periodization Models:**
1. Linear: 8-12 weeks, high volume → low volume, low intensity → high intensity
2. Undulating (DUP): Weekly pattern (Mon-heavy, Wed-medium, Fri-light)
3. Block: 4-6 week blocks with sequential focus

**Deliverable:** Complete strength training for all experience levels.

**Testing:** Test each periodization model with appropriate experience levels.

---

### Phase 3: Running Training

**Components:**
- `methodologies/running_training.py` - Running methodology
- `tools/vdot_calculator.py` - VDOT zone calculator
- `methodologies/templates/running_programs.md` - Running templates

**Functions:**
```python
def generate_running_program(analysis: dict) -> dict
    # Routes to appropriate race distance program

def build_base_building_program(analysis: dict) -> dict
    # 8-12 weeks, Zone 1-2 focus

def build_race_preparation_program(analysis: dict) -> dict
    # Polarized 80/20 distribution with intensity

def calculate_taper(race_distance: str, weeks_until_race: int) -> dict
    # Exponential decay taper protocol
```

**VDOT Calculator:**
```python
def calculate_training_zones(vdot_score: float) -> dict
    # Returns zone paces for Z1-Z5

def estimate_vdot_from_race_time(distance: str, time: str) -> float
    # Calculates VDOT from recent performance
```

**Polarized Distribution:**
- 80% low intensity (Zone 1-2)
- 20% high intensity (Zone 4-5)
- Minimal Zone 3 (avoid "junk miles")

**Deliverable:** Complete running training for 5K, 10K, half marathon, marathon.

**Testing:** Test each distance with various experience levels.

---

### Phase 4: Recovery & Safety

**Components:**
- `methodologies/recovery.py` - Recovery methodology
- `tools/recovery_status.py` - Recovery assessment tool
- `validators/safety_checker.py` - Safety validation

**Functions:**
```python
def generate_recovery_plan(analysis: dict) -> dict
    # Recovery-focused programming

def assess_overtraining_risk(session: dict) -> dict
    # OTS warning sign assessment

def determine_deload_need(training_load: dict, recovery_markers: dict) -> bool
    # Deload recommendation

def generate_deload_week(current_program: dict, week_num: int) -> dict
    # Volume reduction protocol
```

**Recovery Status Tool:**
```python
def determine_recovery_status(sleep_hours: int, resting_hr: int, 
                              mood: str, performance_trend: str) -> dict
    # Returns: {status, recommendations, warnings}
```

**Safety Checker:**
- Validate medical clearance requirements
- Check for contraindicated exercises
- Verify appropriate progression rates
- Ensure adequate recovery

**Deliverable:** Complete safety and recovery monitoring system.

**Testing:** Test recovery scenarios, overtraining detection, deload protocols.

---

### Phase 5: Validation & Testing

**Components:**
- `validators/program_validator.py` - Comprehensive validation
- `validators/output_formatter.py` - Consistent formatting
- `tests/` - Complete test suite

**Validation Checklist:**
```python
validation_rules = [
    'disclaimer_included',
    'experience_level_appropriate',
    'progressive_overload_defined',
    'recovery_scheduled',
    'deload_planned',
    'warning_signs_listed',
    'exercise_instructions_complete',
    'progression_criteria_objective',
    'special_considerations_addressed',
    'output_format_consistent'
]
```

**Test Scenarios:**
1. Beginner strength program (linear periodization)
2. Intermediate strength program (DUP)
3. Advanced strength program (block)
4. Beginner 5K program (base building)
5. Advanced marathon program (polarized)
6. Recovery concern (overtraining assessment)
7. Concurrent training (strength + running)

**Deliverable:** Validated, tested programs across all scenarios with >80% test coverage.

**Testing:** Unit tests for each component, integration tests for full flow.

---

### Phase 6: Production Features

**Components:**
- Session persistence system
- Structured logging
- Token optimization (LRU cache)
- Error recovery mechanisms
- Configuration management

**Session Persistence:**
```python
class SessionManager:
    def save_session(session_id: str, session_data: dict)
    def load_session(session_id: str) -> dict
    def update_program_history(session_id: str, program: dict)
```

**Structured Logging:**
```python
def log_event(event_type: str, session_id: str, details: dict)
    # JSON-formatted logs with correlation IDs
```

**Token Optimization:**
```python
class LRUCache:
    def get(methodology_name: str) -> module
    def set(methodology_name: str, module: module)
    # Cache methodology modules, reference files
```

**Error Recovery:**
- Level 1: Input errors → request clarification
- Level 2: System errors → use fallbacks
- Level 3: Critical errors → recommend professional

**Configuration:**
```json
{
  "token_budget": 3000,
  "cache_size": 5,
  "log_level": "INFO",
  "fallback_enabled": true,
  "strict_validation": false
}
```

**Deliverable:** Production-ready system with monitoring, caching, and error handling.

**Testing:** Test session persistence, error recovery, token usage.

---

### Phase 7: Packaging & Distribution

**Components:**
- README.md - Complete documentation
- CONTRIBUTING.md - Contribution guidelines
- LICENSE - MIT license
- CHANGELOG.md - Version history
- Packaging scripts

**Documentation Structure:**
```markdown
# README.md
- Quick Start
- Installation
- Usage Examples
- Architecture Overview
- Contributing
- License

# CONTRIBUTING.md
- Code of Conduct
- Development Setup
- Adding Methodologies
- Testing Guidelines
- Pull Request Process

# docs/architecture.md
- System Architecture
- Component Design
- Data Flow
- Extension Points

# docs/api_reference.md
- Router API
- Tool APIs
- Validator APIs
- Hook APIs

# docs/extension_guide.md
- Adding New Methodologies
- Creating Tools
- Writing Validators
- Contributing Guidelines
```

**Packaging:**
```python
def package_skill():
    # Creates .skill file with all components
    # Validates structure
    # Generates distribution package
```

**Deliverable:** Complete open-source package ready for distribution.

**Testing:** Verify package installation, test all documented examples.

---

## Error Handling Strategy

### Three-Tier Error Handling

**Tier 1: Input-Level Errors**
- Trigger: Insufficient or contradictory user input
- Hook: `before_program_generation`
- Action: Request specific clarification
- Example: "Need your training experience level to design appropriate program"

**Tier 2: System-Level Errors**
- Trigger: Tool failure, reference unavailable
- Hook: `on_error` with fallback
- Action: Use fallback calculation or simplified approach
- Example: VDOT calculator unavailable → use pace zones based on goal pace

**Tier 3: Critical Errors**
- Trigger: Safety concerns, out of scope request
- Hook: `on_error` with critical flag
- Action: Full disclaimer, recommend professional
- Example: Medical concerns → "Please consult with a physician"

### Error Recovery

```python
def safe_execute(main_func, fallback_func, error_type):
    try:
        return main_func()
    except KnownError as e:
        log_warning(f"{error_type}: {e}, using fallback")
        return fallback_func()
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        return critical_fallback()
```

---

## State Management

### Session Schema

```json
{
  "session_id": "uuid",
  "created_at": "timestamp",
  "user_profile": {
    "experience_level": "string",
    "training_goals": ["string"],
    "constraints": {}
  },
  "program_history": [
    {
      "iteration": 1,
      "timestamp": "timestamp",
      "program_summary": {}
    }
  ],
  "iteration_count": 0,
  "context": {}
}
```

### State Transitions

```
IDLE → ANALYZING (request received)
ANALYZING → DESIGNING (input validated)
DESIGNING → VALIDATING (program drafted)
VALIDATING → OUTPUT (validation passed)
VALIDATING → DESIGNING (validation failed, iterate)
Any → ERROR (error occurred)
ERROR → IDLE (error resolved)
```

---

## Token Optimization

### Loading Strategy

**Priority Order:**
1. SKILL.md (always) - ~500 tokens
2. shared_utils.py (on analysis) - ~300 tokens
3. Selected methodology (on demand) - ~800 tokens
4. Reference files (on demand) - ~400 tokens each
5. Templates (on demand) - ~200 tokens each

**LRU Cache:**
- Cache 5 most recent methodologies
- Cache 3 most recent reference files
- Cache all templates (small)

**Target Budget:** <3000 tokens per typical request

---

## Success Criteria

### Technical Criteria

- [ ] All 7 phases marked 100% complete in PROJECT-DEVELOPMENT-PHASE-TRACKING.md
- [ ] All tests passing with >80% code coverage
- [ ] No placeholders, TODOs, or stub functions in code
- [ ] Production-grade error handling with graceful fallbacks
- [ ] Token usage consistently under 3000 per request
- [ ] Structured logging for monitoring and debugging
- [ ] Session persistence working correctly
- [ ] Configuration management with environment-specific overrides

### Functional Criteria

- [ ] Generates valid programs for all experience levels (beginner, intermediate, advanced)
- [ ] Covers all training goals (strength, hypertrophy, 5K, 10K, half marathon, marathon)
- [ ] Includes required disclaimers in every output
- [ ] Safety checks pass for all programs
- [ ] Output format consistent across all program types
- [ ] Progressive overload clearly defined in all programs
- [ ] Recovery and deloads appropriately scheduled
- [ ] Warning signs included for safety

### Open-Source Criteria

- [ ] Complete README with installation and usage
- [ ] CONTRIBUTING.md with clear guidelines
- [ ] LICENSE file (MIT)
- [ ] CHANGELOG.md with version history
- [ ] API documentation complete
- [ ] Extension guide for contributors
- [ ] Examples for common use cases
- [ ] Code follows consistent style and conventions

---

## Implementation Dependencies

**Phase 1 must complete before:** Phase 2, 3, 4 (require router)

**Phase 2 and 3 can be developed in parallel:** Independent methodologies

**Phase 4 requires:** Phase 2 and 3 (integration with existing programs)

**Phase 5 requires:** Phase 1-4 complete (validation of all components)

**Phase 6 can be developed:** Alongside earlier phases (infrastructure)

**Phase 7 requires:** All previous phases complete (final packaging)

---

## Risk Mitigation

**Risk: Token budget exceeded**
- Mitigation: LRU caching, on-demand loading, reference chunking

**Risk: Methodology complexity leading to bugs**
- Mitigation: Comprehensive testing, validation at each phase

**Risk: Safety concerns not adequately addressed**
- Mitigation: Mandatory safety checker, explicit disclaimers, medical flag detection

**Risk: Open-source contribution quality**
- Mitigation: Clear contribution guidelines, required tests, code review process

---

## Version Strategy

**Initial Release:** 1.0.0 (This implementation)

**Future Versions:**
- 1.1.0: Additional methodologies (CrossFit, powerlifting, etc.)
- 1.2.0: Advanced features (AI-driven recommendations, adaptive programming)
- 2.0.0: Major architecture improvements or breaking changes

---

## Maintenance Strategy

**Regular Updates:**
- Keep reference files current with research
- Update schemas as new tools are added
- Maintain test coverage as code grows

**Community Contributions:**
- Clear process for adding methodologies
- Required tests for new features
- Code review standards
- Documentation requirements

**Monitoring:**
- Track token usage patterns
- Monitor error rates
- Collect user feedback
- Measure test coverage

---

**Design Approved:** 2026-08-05
**Implementation Ready:** Yes
**Estimated Effort:** 40-50 hours
