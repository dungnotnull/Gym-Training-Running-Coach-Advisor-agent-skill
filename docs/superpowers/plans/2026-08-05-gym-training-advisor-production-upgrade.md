# Gym Training & Running Coach Advisor - Production Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the Gym Training & Running Coach Advisor skill to production-grade, open-source standards with complete implementation of all 7 phases including router architecture, methodology functions, tool system, validation layer, and production features.

**Architecture:** Lightweight Router Pattern with domain-specialized methodology functions, shared utilities, clean error boundaries, and comprehensive validation. Main orchestrator routes requests to appropriate methodology modules (strength training, running training, recovery) which call tools as needed and return validated programs.

**Tech Stack:** Python 3.9+, pytest for testing, JSON schemas for validation, type-safe configuration management

---

## File Structure Overview

```
gym-running-training-advisor/
├── router.py                         # NEW - Main orchestrator
├── methodologies/                    # NEW - Domain logic
│   ├── __init__.py
│   ├── strength_training.py
│   ├── running_training.py
│   ├── recovery.py
│   ├── general.py
│   ├── shared_utils.py
│   └── templates/
├── tools/                            # NEW - Executable tools
│   ├── __init__.py
│   ├── vdot_calculator.py
│   ├── one_rm_estimator.py
│   ├── recovery_status.py
│   └── progression_planner.py
├── validators/                       # NEW - Quality layer
│   ├── __init__.py
│   ├── program_validator.py
│   ├── safety_checker.py
│   └── output_formatter.py
├── hooks/                            # NEW - Hook implementations
│   ├── __init__.py
│   ├── pre_processing.py
│   ├── post_processing.py
│   ├── error_handlers.py
│   └── state_management.py
├── config/
│   ├── settings.json                 # NEW
│   └── hooks-system.md              # EXISTING
├── assets/
│   ├── schemas/                      # EXISTING + NEW
│   └── templates/                    # NEW
├── scripts/                          # NEW
├── tests/                            # NEW
└── docs/                             # NEW
```

---

## Phase 1: Foundation (Core Router & Analysis)

### Task 1.1: Create Project Structure

**Files:**
- Create: `methodologies/__init__.py`
- Create: `tools/__init__.py`
- Create: `validators/__init__.py`
- Create: `hooks/__init__.py`
- Create: `scripts/__init__.py`
- Create: `tests/__init__.py`
- Create: `docs/`
- Create: `assets/templates/`

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p methodologies templates tools validators hooks scripts tests docs assets/templates
```

- [ ] **Step 2: Create __init__.py files**

```bash
touch methodologies/__init__.py tools/__init__.py validators/__init__.py hooks/__init__.py scripts/__init__.py tests/__init__.py
```

- [ ] **Step 3: Verify structure**

Run: `ls -la methodologies/ tools/ validators/ hooks/ scripts/ tests/`
Expected: All directories with __init__.py files

- [ ] **Step 4: Commit**

```bash
git add methodologies/ tools/ validators/ hooks/ scripts/ tests/ docs/ assets/templates/
git commit -m "feat: create project directory structure"
```

---

### Task 1.2: Create Configuration System

**Files:**
- Create: `config/settings.json`
- Modify: `config/hooks-system.md` (add reference to settings.json)

- [ ] **Step 1: Write configuration schema**

```json
{
  "system": {
    "version": "1.0.0",
    "environment": "production"
  },
  "performance": {
    "token_budget": 3000,
    "cache_size": 5,
    "lazy_loading": true
  },
  "validation": {
    "strict_mode": false,
    "fallback_enabled": true,
    "safety_first": true
  },
  "logging": {
    "level": "INFO",
    "structured": true,
    "include_timestamps": true
  },
  "session": {
    "persistence_enabled": true,
    "session_dir": ".sessions",
    "max_history": 10
  },
  "hooks": {
    "before_program_generation": {
      "enabled": true,
      "strict_validation": true
    },
    "after_program_generation": {
      "enabled": true,
      "validation_level": "standard"
    },
    "on_error": {
      "enabled": true,
      "fallback_enabled": true,
      "verbose_errors": false
    }
  }
}
```

- [ ] **Step 2: Create config loader**

```python
# config/__init__.py
import json
from pathlib import Path
from typing import Dict, Any

class Config:
    _instance = None
    _config: Dict[str, Any] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def load(self) -> Dict[str, Any]:
        if self._config is None:
            config_path = Path(__file__).parent / "settings.json"
            with open(config_path) as f:
                self._config = json.load(f)
        return self._config
    
    def get(self, key: str, default=None) -> Any:
        config = self.load()
        keys = key.split(".")
        value = config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

config = Config()
```

- [ ] **Step 3: Write test for config loading**

```python
# tests/test_config.py
import pytest
from config import config

def test_config_loads():
    assert config.get("system.version") == "1.0.0"
    assert config.get("performance.token_budget") == 3000

def test_config_get_with_default():
    assert config.get("nonexistent.key", "default") == "default"

def test_config_nested_get():
    assert config.get("logging.level") == "INFO"
```

- [ ] **Step 4: Run tests to verify config system**

Run: `pytest tests/test_config.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add config/ tests/test_config.py
git commit -m "feat: add configuration system with type-safe loading"
```

---

### Task 1.3: Implement Shared Utilities

**Files:**
- Create: `methodologies/shared_utils.py`
- Test: `tests/test_methodologies/test_shared_utils.py`

- [ ] **Step 1: Write test for experience classification**

```python
# tests/test_methodologies/test_shared_utils.py
import pytest
from methodologies.shared_utils import classify_experience

def test_classify_beginner():
    assert classify_experience("I'm new to lifting") == "beginner"
    assert classify_experience("just starting out") == "beginner"
    assert classify_experience("never worked out before") == "beginner"

def test_classify_intermediate():
    assert classify_experience("I've been training for 2 years") == "intermediate"
    assert classify_experience("consistent for 18 months") == "intermediate"

def test_classify_advanced():
    assert classify_experience("I've been training 5 years") == "advanced"
    assert classify_experience("competitive lifter") == "advanced"

def test_classify_unknown_defaults_to_intermediate():
    assert classify_experience("not sure about my experience") == "intermediate"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_shared_utils.py::test_classify_beginner -v`
Expected: FAIL with "classify_experience not defined"

- [ ] **Step 3: Implement experience classification**

```python
# methodologies/shared_utils.py
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
    r"3\+.*years?|advanced|competitive|elite",
    r"trained for.*long time"
]

def classify_experience(user_input: str) -> str:
    """Classify user experience level."""
    user_input_lower = user_input.lower()
    
    # Check for advanced patterns first
    for pattern in ADVANCED_PATTERNS:
        if re.search(pattern, user_input_lower):
            return "advanced"
    
    # Check for beginner patterns
    for pattern in BEGINNER_PATTERNS:
        if re.search(pattern, user_input_lower):
            return "beginner"
    
    # Check for intermediate patterns
    for pattern in INTERMEDIATE_PATTERNS:
        if re.search(pattern, user_input_lower):
            return "intermediate"
    
    # Default to intermediate
    return "intermediate"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_methodologies/test_shared_utils.py -v`
Expected: PASS

- [ ] **Step 5: Write test for goal classification**

```python
def test_classify_strength_goal():
    assert classify_goal("I want to get stronger") == "strength"
    assert classify_goal("build strength") == "strength"
    assert classify_goal("increase my squat") == "strength"

def test_classify_hypertrophy_goal():
    assert classify_goal("build muscle mass") == "hypertrophy"
    assert classify_goal("get bigger") == "hypertrophy"
    assert classify_goal("hypertrophy") == "hypertrophy"

def test_classify_running_goals():
    assert classify_goal("train for a 5K") == "5k"
    assert classify_goal("run a marathon") == "marathon"
    assert classify_goal("half marathon training") == "half_marathon"

def test_classify_general_fitness():
    assert classify_goal("just get fit") == "general"
    assert classify_goal("overall health") == "general"
```

- [ ] **Step 6: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_shared_utils.py::test_classify_strength_goal -v`
Expected: FAIL with "classify_goal not defined"

- [ ] **Step 7: Implement goal classification**

```python
# Add to methodologies/shared_utils.py

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
    
    # Check specific running goals first
    for goal in ["marathon", "half_marathon", "10k", "5k"]:
        for pattern in GOAL_PATTERNS[goal]:
            if re.search(pattern, user_input_lower):
                return goal
    
    # Check strength/hypertrophy
    if any(re.search(p, user_input_lower) for p in GOAL_PATTERNS["strength"]):
        return "strength"
    if any(re.search(p, user_input_lower) for p in GOAL_PATTERNS["hypertrophy"]):
        return "hypertrophy"
    
    # Default to general
    return "general"
```

- [ ] **Step 8: Run all shared_utils tests**

Run: `pytest tests/test_methodologies/test_shared_utils.py -v`
Expected: All PASS

- [ ] **Step 9: Commit**

```bash
git add methodologies/shared_utils.py tests/test_methodologies/test_shared_utils.py
git commit -m "feat: implement experience and goal classification"
```

---

### Task 1.4: Implement Constraint Extraction

**Files:**
- Modify: `methodologies/shared_utils.py` (add constraint extraction)
- Test: `tests/test_methodologies/test_shared_utils.py`

- [ ] **Step 1: Write test for constraint extraction**

```python
def test_extract_time_constraint():
    result = extract_constraints("I can train 3 days per week")
    assert result["time_available"] == "3 days per week"

def test_extract_equipment_constraint():
    result = extract_constraints("I have dumbbells and a bench")
    assert "dumbbells" in result["equipment"]
    assert "bench" in result["equipment"]

def test_extract_health_constraints():
    result = extract_constraints("I have a bad shoulder")
    assert "shoulder" in result.get("health_conditions", [])

def test_no_constraints_returns_empty():
    result = extract_constraints("I want to get stronger")
    assert result["time_available"] is None
    assert result["equipment"] == []
    assert result["health_conditions"] == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_shared_utils.py::test_extract_time_constraint -v`
Expected: FAIL with "extract_constraints not defined"

- [ ] **Step 3: Implement constraint extraction**

```python
# Add to methodologies/shared_utils.py

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
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_methodologies/test_shared_utils.py::test_extract -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add methodologies/shared_utils.py tests/test_methodologies/test_shared_utils.py
git commit -m "feat: implement constraint extraction"
```

---

### Task 1.5: Implement Safety Flag Detection

**Files:**
- Modify: `methodologies/shared_utils.py` (add safety detection)
- Test: `tests/test_methodologies/test_shared_utils.py`

- [ ] **Step 1: Write test for safety flag detection**

```python
def test_detect_medical_concern_flag():
    flags = detect_safety_flags("I have diabetes and want to train")
    assert "medical_concern" in flags

def test_detect_injury_flag():
    flags = detect_safety_flags("I'm recovering from a knee injury")
    assert "injury" in flags

def test_detect_recovery_concern_flag():
    flags = detect_safety_flags("I've been feeling exhausted lately")
    assert "recovery_concern" in flags

def test_no_flags_returns_empty():
    flags = detect_safety_flags("I want to get stronger")
    assert flags == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_shared_utils.py::test_detect_medical_concern_flag -v`
Expected: FAIL with "detect_safety_flags not defined"

- [ ] **Step 3: Implement safety flag detection**

```python
# Add to methodologies/shared_utils.py

def detect_safety_flags(user_input: str) -> List[str]:
    """Detect safety flags requiring special attention."""
    user_input_lower = user_input.lower()
    flags = []
    
    # Medical concerns
    medical_keywords = ["diabetes", "heart condition", "hypertension", "asthma",
                       "medical condition", "doctor", "physician", "medication"]
    if any(keyword in user_input_lower for keyword in medical_keywords):
        flags.append("medical_concern")
    
    # Injury flags
    injury_keywords = ["injury", "injured", "recovering from", "rehab", "physical therapy"]
    if any(keyword in user_input_lower for keyword in injury_keywords):
        flags.append("injury")
    
    # Recovery concerns
    recovery_keywords = ["exhausted", "overtrained", "fatigue", "burnout", 
                        "tired all the time", "no energy"]
    if any(keyword in user_input_lower for keyword in recovery_keywords):
        flags.append("recovery_concern")
    
    # Eating disorder red flags
    ed_keywords = ["anorexic", "bulimic", "eating disorder", "lose weight fast"]
    if any(keyword in user_input_lower for keyword in ed_keywords):
        flags.append("eating_disorder_concern")
    
    return flags
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_methodologies/test_shared_utils.py::test_detect -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add methodologies/shared_utils.py tests/test_methodologies/test_shared_utils.py
git commit -m "feat: implement safety flag detection"
```

---

### Task 1.6: Create Main Router Class

**Files:**
- Create: `router.py`
- Test: `tests/test_router.py`

- [ ] **Step 1: Write test for router initialization**

```python
# tests/test_router.py
import pytest
from router import TrainingAdvisorRouter

def test_router_initialization():
    router = TrainingAdvisorRouter()
    assert router.session_id is not None
    assert router.session == {}
    assert len(router.session) == 0

def test_router_generates_unique_session_ids():
    router1 = TrainingAdvisorRouter()
    router2 = TrainingAdvisorRouter()
    assert router1.session_id != router2.session_id
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_router.py::test_router_initialization -v`
Expected: FAIL with "TrainingAdvisorRouter not defined"

- [ ] **Step 3: Implement router initialization**

```python
# router.py
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from methodologies.shared_utils import (
    classify_experience, 
    classify_goal, 
    extract_constraints,
    detect_safety_flags
)

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
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_router.py -v`
Expected: PASS

- [ ] **Step 5: Write test for analyze_input method**

```python
def test_analyze_input_returns_analysis():
    router = TrainingAdvisorRouter()
    analysis = router.analyze_input("I'm a beginner wanting to get stronger")
    
    assert analysis["experience_level"] == "beginner"
    assert analysis["goal"] == "strength"
    assert "constraints" in analysis
    assert "flags" in analysis

def test_analyze_input_extracts_constraints():
    router = TrainingAdvisorRouter()
    analysis = router.analyze_input("I can train 3 days per week with dumbbells")
    
    assert analysis["constraints"]["time_available"] == "3 days per week"
    assert "dumbbells" in analysis["constraints"]["equipment"]

def test_analyze_input_detects_flags():
    router = TrainingAdvisorRouter()
    analysis = router.analyze_input("I have diabetes and want to get stronger")
    
    assert "medical_concern" in analysis["flags"]
```

- [ ] **Step 6: Run test to verify it fails**

Run: `pytest tests/test_router.py::test_analyze_input_returns_analysis -v`
Expected: FAIL with "analyze_input method not defined"

- [ ] **Step 7: Implement analyze_input method**

```python
# Add to router.py

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
```

- [ ] **Step 8: Run tests**

Run: `pytest tests/test_router.py -v`
Expected: All PASS

- [ ] **Step 9: Commit**

```bash
git add router.py tests/test_router.py
git commit -m "feat: implement main router class with input analysis"
```

---

### Task 1.7: Implement Methodology Routing

**Files:**
- Modify: `router.py` (add routing logic)
- Test: `tests/test_router.py`

- [ ] **Step 1: Write test for methodology selection**

```python
def test_select_methodology_for_strength():
    router = TrainingAdvisorRouter()
    analysis = {"goal": "strength", "experience_level": "intermediate"}
    methodology = router._select_methodology(analysis)
    assert methodology == "strength"

def test_select_methodology_for_running():
    router = TrainingAdvisorRouter()
    analysis = {"goal": "marathon", "experience_level": "advanced"}
    methodology = router._select_methodology(analysis)
    assert methodology == "running"

def test_select_methodology_for_recovery_priority():
    router = TrainingAdvisorRouter()
    analysis = {"goal": "strength", "flags": ["recovery_concern"]}
    methodology = router._select_methodology(analysis)
    assert methodology == "recovery"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_router.py::test_select_methodology_for_strength -v`
Expected: FAIL with "_select_methodology method not defined"

- [ ] **Step 3: Implement methodology selection**

```python
# Add to router.py

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
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_router.py::test_select_methodology -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add router.py tests/test_router.py
git commit -m "feat: implement methodology selection logic"
```

---

### Task 1.8: Implement Process Request Method

**Files:**
- Modify: `router.py` (add main processing method)
- Create: `methodologies/general.py` (basic implementation for testing)
- Test: `tests/test_router.py`

- [ ] **Step 1: Create placeholder methodology modules**

```python
# methodologies/strength_training.py
def generate_strength_program(analysis):
    return {"type": "strength", "status": "placeholder"}

# methodologies/running_training.py
def generate_running_program(analysis):
    return {"type": "running", "status": "placeholder"}

# methodologies/recovery.py
def generate_recovery_plan(analysis):
    return {"type": "recovery", "status": "placeholder"}

# methodologies/general.py
def generate_general_program(analysis):
    return {"type": "general", "status": "placeholder"}
```

- [ ] **Step 2: Write test for process_request**

```python
def test_process_request_generates_program():
    router = TrainingAdvisorRouter()
    result = router.process_request("I'm a beginner wanting to get stronger")
    
    assert "program" in result
    assert result["program"]["type"] == "strength"
    assert "session_id" in result

def test_process_request_updates_session():
    router = TrainingAdvisorRouter()
    result = router.process_request("I want to run a marathon")
    
    assert router.session["iteration_count"] == 1
    assert len(router.session["program_history"]) == 1
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_router.py::test_process_request_generates_program -v`
Expected: FAIL with "process_request method not defined"

- [ ] **Step 4: Implement process_request method**

```python
# Add to router.py
import methodologies.strength_training as strength_training
import methodologies.running_training as running_training
import methodologies.recovery as recovery
import methodologies.general as general

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
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_router.py -v`
Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add router.py methodologies/ tests/test_router.py
git commit -m "feat: implement main process_request method"
```

---

## Phase 2: Periodization Models (Strength Training)

### Task 2.1: Implement Linear Periodization

**Files:**
- Modify: `methodologies/strength_training.py`
- Create: `methodologies/templates/strength_programs.md`
- Test: `tests/test_methodologies/test_strength_training.py`

- [ ] **Step 1: Write test for linear periodization**

```python
# tests/test_methodologies/test_strength_training.py
import pytest
from methodologies.strength_training import build_linear_program

def test_linear_program_for_beginner():
    analysis = {
        "experience_level": "beginner",
        "goal": "strength",
        "constraints": {"time_available": "3 days per week"}
    }
    program = build_linear_program(analysis)
    
    assert program["periodization_model"] == "linear"
    assert len(program["weeks"]) >= 8
    assert program["weeks"][0]["phase"] == "hypertrophy"
    assert program["weeks"][-1]["phase"] == "peaking"

def test_linear_program_has_deload():
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)
    
    deload_weeks = [w for w in program["weeks"] if w.get("is_deload")]
    assert len(deload_weeks) >= 2  # At least 2 deload weeks

def test_linear_program_progression():
    analysis = {"experience_level": "beginner", "goal": "strength"}
    program = build_linear_program(analysis)
    
    # Check intensity increases over time
    week1_intensity = program["weeks"][0"]["intensity_level"]
    week8_intensity = program["weeks"][7]["intensity_level"]
    assert week8_intensity > week1_intensity
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_strength_training.py::test_linear_program_for_beginner -v`
Expected: FAIL with "build_linear_program not defined"

- [ ] **Step 3: Implement linear periodization**

```python
# methodologies/strength_training.py
from typing import Dict, Any, List

def generate_strength_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate strength training program based on analysis."""
    experience = analysis.get("experience_level", "intermediate")
    
    if experience == "beginner":
        return build_linear_program(analysis)
    elif experience == "intermediate":
        return build_undulating_program(analysis)
    else:  # advanced
        return build_block_program(analysis)

def build_linear_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build linear periodization program for beginners."""
    weeks = []
    
    # Phase 1: Hypertrophy/Endurance (weeks 1-4)
    for week in range(1, 5):
        weeks.append(_create_hypertrophy_week(week, analysis))
    
    # Deload week 4
    weeks[3]["is_deload"] = True
    weeks[3]["deload_reduction"] = 0.5
    
    # Phase 2: Strength (weeks 5-8)
    for week in range(5, 9):
        weeks.append(_create_strength_week(week, analysis))
    
    # Deload week 8
    weeks[7]["is_deload"] = True
    weeks[7]["deload_reduction"] = 0.5
    
    # Phase 3: Peaking (weeks 9-12)
    for week in range(9, 13):
        weeks.append(_create_peaking_week(week, analysis))
    
    return {
        "periodization_model": "linear",
        "experience_level": "beginner",
        "goal": analysis.get("goal", "strength"),
        "weeks": weeks,
        "progression_rules": _get_linear_progression_rules(),
        "deload_schedule": [4, 8, 12],
        "total_duration": "12 weeks"
    }

def _create_hypertrophy_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a hypertrophy-focused week."""
    days = _get_available_days(analysis)
    return {
        "week_number": week_num,
        "phase": "hypertrophy",
        "intensity_level": 0.65,  # 65% 1RM
        "volume": "high",
        "reps_per_set": "10-12",
        "sets_per_exercise": 3,
        "rest_interval": "90 seconds",
        "sessions": _create_sessions(days, "hypertrophy"),
        "focus": "Work capacity and muscle development"
    }

def _create_strength_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a strength-focused week."""
    days = _get_available_days(analysis)
    return {
        "week_number": week_num,
        "phase": "strength",
        "intensity_level": 0.80,  # 80% 1RM
        "volume": "moderate",
        "reps_per_set": "5-8",
        "sets_per_exercise": 4,
        "rest_interval": "3 minutes",
        "sessions": _create_sessions(days, "strength"),
        "focus": "Maximal strength development"
    }

def _create_peaking_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a peaking-focused week."""
    days = _get_available_days(analysis)
    return {
        "week_number": week_num,
        "phase": "peaking",
        "intensity_level": 0.90,  # 90% 1RM
        "volume": "low",
        "reps_per_set": "2-5",
        "sets_per_exercise": 3,
        "rest_interval": "5 minutes",
        "sessions": _create_sessions(days, "peaking"),
        "focus": "Maximal strength expression"
    }

def _get_available_days(analysis: Dict) -> List[str]:
    """Determine available training days."""
    time_constraint = analysis.get("constraints", {}).get("time_available", "")
    
    if "3" in time_constraint:
        return ["monday", "wednesday", "friday"]
    elif "4" in time_constraint:
        return ["monday", "tuesday", "thursday", "friday"]
    else:
        return ["monday", "wednesday", "friday"]  # Default to 3 days

def _create_sessions(days: List[str], phase: str) -> List[Dict]:
    """Create training sessions for the week."""
    sessions = []
    exercises = _get_exercises_for_phase(phase)
    
    for day in days:
        sessions.append({
            "day": day,
            "exercises": exercises,
            "warmup": "5-10 min light cardio + dynamic stretching",
            "cooldown": "5-10 min stretching"
        })
    
    return sessions

def _get_exercises_for_phase(phase: str) -> List[Dict]:
    """Get exercises appropriate for the training phase."""
    base_exercises = [
        {"name": "Squat", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Bench Press", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Deadlift", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Overhead Press", "sets": 3, "reps": "per_phase", "rest": "per_phase"},
        {"name": "Barbell Row", "sets": 3, "reps": "per_phase", "rest": "per_phase"}
    ]
    
    if phase == "hypertrophy":
        for ex in base_exercises:
            ex["reps"] = "10-12"
            ex["rest"] = "90 seconds"
    elif phase == "strength":
        for ex in base_exercises:
            ex["reps"] = "5-8"
            ex["rest"] = "3 minutes"
            if ex["name"] == "Squat":
                ex["sets"] = 4
    elif phase == "peaking":
        for ex in base_exercises:
            ex["reps"] = "3-5"
            ex["rest"] = "5 minutes"
    
    return base_exercises

def _get_linear_progression_rules() -> Dict[str, str]:
    """Get progression rules for linear periodization."""
    return {
        "load_progression": "Increase weight when 2+ reps above target with good form",
        "increment": "Upper: 2.5-5 lbs, Lower: 5-10 lbs",
        "deload_frequency": "Every 4 weeks",
        "deload_protocol": "Reduce volume by 50%, maintain intensity",
        "form_priority": "Never sacrifice form for load increases"
    }
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_methodologies/test_strength_training.py::test_linear -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add methodologies/strength_training.py tests/test_methodologies/test_strength_training.py
git commit -m "feat: implement linear periodization for beginners"
```

---

### Task 2.2: Implement Undulating Periodization (DUP)

**Files:**
- Modify: `methodologies/strength_training.py`
- Test: `tests/test_methodologies/test_strength_training.py`

- [ ] **Step 1: Write test for undulating periodization**

```python
def test_undulating_program_for_intermediate():
    analysis = {
        "experience_level": "intermediate",
        "goal": "strength",
        "constraints": {"time_available": "4 days per week"}
    }
    program = build_undulating_program(analysis)
    
    assert program["periodization_model"] == "undulating"
    assert "weekly_pattern" in program
    assert program["weekly_pattern"]["monday"] == "heavy"
    assert program["weekly_pattern"]["friday"] == "light"

def test_undulating_program_intensity_variation():
    analysis = {"experience_level": "intermediate", "goal": "strength"}
    program = build_undulating_program(analysis)
    
    # Check weekly intensity varies
    week = program["weeks"][0]
    monday_session = next(s for s in week["sessions"] if s["day"] == "monday")
    friday_session = next(s for s in week["sessions"] if s["day"] == "friday")
    
    assert monday_session["intensity"] == "heavy"
    assert friday_session["intensity"] == "light"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_strength_training.py::test_undulating_program_for_intermediate -v`
Expected: FAIL with "build_undulating_program not defined"

- [ ] **Step 3: Implement undulating periodization**

```python
# Add to methodologies/strength_training.py

def build_undulating_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build undulating (DUP) program for intermediate lifters."""
    weeks = []
    
    for week_num in range(1, 13):
        if week_num % 4 == 0:
            weeks.append(_create_dup_deload_week(week_num, analysis))
        else:
            weeks.append(_create_dup_week(week_num, analysis))
    
    return {
        "periodization_model": "undulating",
        "experience_level": "intermediate",
        "goal": analysis.get("goal", "strength"),
        "weekly_pattern": {
            "monday": "heavy",
            "wednesday": "medium",
            "friday": "light"
        },
        "weeks": weeks,
        "progression_rules": _get_dup_progression_rules(),
        "deload_schedule": [4, 8],
        "total_duration": "12 weeks"
    }

def _create_dup_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a DUP week with heavy/medium/light pattern."""
    days = _get_available_days(analysis)
    sessions = []
    
    intensity_pattern = {
        "monday": "heavy",
        "wednesday": "medium",
        "friday": "light"
    }
    
    for day in days:
        if day in intensity_pattern:
            intensity = intensity_pattern[day]
            sessions.append(_create_dup_session(day, intensity, analysis))
    
    return {
        "week_number": week_num,
        "sessions": sessions,
        "pattern": "heavy/medium/light",
        "focus": "Variation in intensity for adaptation"
    }

def _create_dup_session(day: str, intensity: str, analysis: Dict) -> Dict[str, Any]:
    """Create a single DUP session."""
    intensity_params = {
        "heavy": {"percent": 0.85, "reps": "3-5", "rest": "3-5 min"},
        "medium": {"percent": 0.75, "reps": "6-8", "rest": "2-3 min"},
        "light": {"percent": 0.60, "reps": "10-12", "rest": "1-2 min"}
    }
    
    params = intensity_params[intensity]
    exercises = _get_exercises_for_dup(params)
    
    return {
        "day": day,
        "intensity": intensity,
        "exercises": exercises,
        "warmup": "5-10 min light cardio + dynamic stretching",
        "cooldown": "5-10 min stretching"
    }

def _get_exercises_for_dup(params: Dict) -> List[Dict]:
    """Get exercises for DUP session with given parameters."""
    return [
        {
            "name": "Squat",
            "sets": 4,
            "reps": params["reps"],
            "percent_1rm": params["percent"],
            "rest": params["rest"]
        },
        {
            "name": "Bench Press",
            "sets": 4,
            "reps": params["reps"],
            "percent_1rm": params["percent"],
            "rest": params["rest"]
        },
        {
            "name": "Deadlift",
            "sets": 3,
            "reps": params["reps"],
            "percent_1rm": params["percent"],
            "rest": params["rest"]
        }
    ]

def _create_dup_deload_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a deload week for DUP."""
    days = _get_available_days(analysis)
    sessions = []
    
    for day in days:
        sessions.append({
            "day": day,
            "intensity": "light",
            "is_deload": True,
            "exercises": _get_exercises_for_dup({"percent": 0.60, "reps": "8-10", "rest": "2 min"}),
            "note": "Reduce volume, focus on technique"
        })
    
    return {
        "week_number": week_num,
        "is_deload": True,
        "sessions": sessions,
        "deload_reduction": 0.40
    }

def _get_dup_progression_rules() -> Dict[str, str]:
    """Get progression rules for DUP."""
    return {
        "weekly_progression": "Increase heavy day load by 2.5-5 lbs when target reps achieved",
        "medium_day_adjustment": "Maintain at ~80% of heavy day load",
        "light_day_adjustment": "Maintain at ~60% of heavy day load",
        "deload_frequency": "Every 4 weeks",
        "deload_protocol": "Reduce all session loads by 40%, maintain volume",
        "form_priority": "Technique quality over load increases"
    }
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_methodologies/test_strength_training.py::test_undulating -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add methodologies/strength_training.py tests/test_methodologies/test_strength_training.py
git commit -m "feat: implement undulating periodization (DUP) for intermediate"
```

---

### Task 2.3: Implement Block Periodization

**Files:**
- Modify: `methodologies/strength_training.py`
- Test: `tests/test_methodologies/test_strength_training.py`

- [ ] **Step 1: Write test for block periodization**

```python
def test_block_program_for_advanced():
    analysis = {
        "experience_level": "advanced",
        "goal": "strength",
        "constraints": {"time_available": "5 days per week"}
    }
    program = build_block_program(analysis)
    
    assert program["periodization_model"] == "block"
    assert len(program["blocks"]) == 3
    assert program["blocks"][0]["type"] == "accumulation"
    assert program["blocks"][2]["type"] == "realization"

def test_block_program_sequential_focus():
    analysis = {"experience_level": "advanced", "goal": "strength"}
    program = build_block_program(analysis)
    
    # Each block has distinct focus
    assert program["blocks"][0]["focus"] != program["blocks"][1]["focus"]
    assert program["blocks"][1]["focus"] != program["blocks"][2]["focus"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_strength_training.py::test_block_program_for_advanced -v`
Expected: FAIL with "build_block_program not defined"

- [ ] **Step 3: Implement block periodization**

```python
# Add to methodologies/strength_training.py

def build_block_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build block periodization program for advanced lifters."""
    blocks = []
    
    # Block 1: Accumulation (4 weeks)
    blocks.append(_create_accumulation_block(1, analysis))
    
    # Block 2: Transmutation (4 weeks)
    blocks.append(_create_transmutation_block(2, analysis))
    
    # Block 3: Realization (4 weeks)
    blocks.append(_create_realization_block(3, analysis))
    
    return {
        "periodization_model": "block",
        "experience_level": "advanced",
        "goal": analysis.get("goal", "strength"),
        "blocks": blocks,
        "total_duration": "12 weeks",
        "progression_rules": _get_block_progression_rules(),
        "block_structure": "accumulation → transmutation → realization"
    }

def _create_accumulation_block(block_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create accumulation block for building work capacity."""
    weeks = []
    for week in range(1, 5):
        weeks.append({
            "week_number": week,
            "focus": "volume",
            "intensity": "moderate",
            "exercises": _get_accumulation_exercises(),
            "sessions_per_week": len(_get_available_days(analysis))
        })
    
    return {
        "block_number": block_num,
        "type": "accumulation",
        "duration": "4 weeks",
        "weeks": weeks,
        "focus": "Build work capacity and general preparation",
        "volume": "high",
        "intensity": "low to moderate",
        "exercise_variety": "high"
    }

def _create_transmutation_block(block_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create transmutation block for converting qualities."""
    weeks = []
    for week in range(1, 5):
        weeks.append({
            "week_number": week + 4,
            "focus": "strength conversion",
            "intensity": "high",
            "exercises": _get_transmutation_exercises(),
            "sessions_per_week": len(_get_available_days(analysis))
        })
    
    return {
        "block_number": block_num,
        "type": "transmutation",
        "duration": "4 weeks",
        "weeks": weeks,
        "focus": "Convert general qualities to specific strength",
        "volume": "moderate",
        "intensity": "moderate to high",
        "exercise_variety": "moderate"
    }

def _create_realization_block(block_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create realization block for peaking."""
    weeks = []
    for week in range(1, 5):
        weeks.append({
            "week_number": week + 8,
            "focus": "maximal strength",
            "intensity": "very high",
            "exercises": _get_realization_exercises(),
            "sessions_per_week": len(_get_available_days(analysis))
        })
    
    return {
        "block_number": block_num,
        "type": "realization",
        "duration": "4 weeks",
        "weeks": weeks,
        "focus": "Maximize specific performance",
        "volume": "low",
        "intensity": "high",
        "exercise_variety": "low (competition specific)"
    }

def _get_accumulation_exercises() -> List[Dict]:
    """Get exercises for accumulation block."""
    return [
        {"name": "Squat", "sets": 4, "reps": "8-10", "percent_1rm": 0.70},
        {"name": "Bench Press", "sets": 4, "reps": "10", "percent_1rm": 0.65},
        {"name": "Deadlift", "sets": 4, "reps": "6-8", "percent_1rm": 0.70},
        {"name": "Rows", "sets": 4, "reps": "12", "percent_1rm": 0.60},
        {"name": "Overhead Press", "sets": 3, "reps": "10", "percent_1rm": 0.65}
    ]

def _get_transmutation_exercises() -> List[Dict]:
    """Get exercises for transmutation block."""
    return [
        {"name": "Squat", "sets": 5, "reps": "5", "percent_1rm": 0.80},
        {"name": "Bench Press", "sets": 5, "reps": "5", "percent_1rm": 0.80},
        {"name": "Deadlift", "sets": 4, "reps": "4", "percent_1rm": 0.80},
        {"name": "Rows", "sets": 4, "reps": "8", "percent_1rm": 0.70},
        {"name": "Close-Grip Bench", "sets": 3, "reps": "8", "percent_1rm": 0.70}
    ]

def _get_realization_exercises() -> List[Dict]:
    """Get exercises for realization block."""
    return [
        {"name": "Squat", "sets": 3, "reps": "3", "percent_1rm": 0.90},
        {"name": "Bench Press", "sets": 3, "reps": "3", "percent_1rm": 0.90},
        {"name": "Deadlift", "sets": 2, "reps": "2-3", "percent_1rm": 0.90},
        {"name": "Overhead Press", "sets": 3, "reps": "5", "percent_1rm": 0.85}
    ]

def _get_block_progression_rules() -> Dict[str, str]:
    """Get progression rules for block periodization."""
    return {
        "accumulation_progression": "Increase volume first, then intensity",
        "transmutation_progression": "Focus on intensity increases",
        "realization_progression": "Peak at specific competition weights",
        "deload_between_blocks": "1 week reduced volume between blocks",
        "exercise_selection": "High specificity in realization block"
    }
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_methodologies/test_strength_training.py::test_block -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add methodologies/strength_training.py tests/test_methodologies/test_strength_training.py
git commit -m "feat: implement block periodization for advanced"
```

---

## Phase 3: Running Training

### Task 3.1: Implement VDOT Calculator Tool

**Files:**
- Create: `tools/vdot_calculator.py`
- Create: `assets/schemas/training-zones-schema.json`
- Test: `tests/test_tools/test_vdot_calculator.py`

- [ ] **Step 1: Write VDOT zones schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Training Zones Output",
  "type": "object",
  "properties": {
    "vdot_score": {"type": "number"},
    "zones": {
      "type": "object",
      "properties": {
        "zone1_easy": {"type": "object"},
        "zone2_marathon": {"type": "object"},
        "zone3_threshold": {"type": "object"},
        "zone4_interval": {"type": "object"},
        "zone5_repetition": {"type": "object"}
      }
    },
    "calculated_at": {"type": "string"}
  },
  "required": ["vdot_score", "zones"]
}
```

- [ ] **Step 2: Write test for VDOT calculator**

```python
# tests/test_tools/test_vdot_calculator.py
import pytest
from tools.vdot_calculator import calculate_training_zones, estimate_vdot_from_race_time

def test_calculate_zones_from_vdot():
    result = calculate_training_zones(45.0)
    
    assert result["vdot_score"] == 45.0
    assert "zones" in result
    assert "zone1_easy" in result["zones"]
    assert result["zones"]["zone1_easy"]["vo2_range"] == "59-74%"

def test_invalid_vdot_raises_error():
    with pytest.raises(ValueError):
        calculate_training_zones(150)  # Too high

def test_estimate_vdot_from_5k():
    vdot = estimate_vdot_from_race_time("5k", "22:00")
    assert 40 <= vdot <= 50  # Reasonable range
```

- [ ] **Step 3: Run test to verify it fails**

Run: `pytest tests/test_tools/test_vdot_calculator.py::test_calculate_zones_from_vdot -v`
Expected: FAIL with modules not found

- [ ] **Step 4: Implement VDOT calculator**

```python
# tools/vdot_calculator.py
from datetime import datetime
from typing import Dict, Any

def calculate_training_zones(vdot_score: float) -> Dict[str, Any]:
    """Calculate training zones from VDOT score using Daniels' formulas."""
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
    """Zone 1: Easy/Recovery (59-74% VO2max)"""
    # Simplified Daniels formula for example
    min_pace = _vdot_to_pace(vdot * 0.74)  # Easier pace
    max_pace = _vdot_to_pace(vdot * 0.59)  # Slower pace
    
    return {
        "vo2_range": "59-74%",
        "description": "Easy/recovery pace",
        "purpose": "Aerobic base building, recovery",
        "talk_test": "Can hold full conversation easily",
        "typical_use": "Recovery runs, warm-up, cool-down",
        "duration_range": "20-60 minutes"
    }

def _calculate_zone2(vdot: float) -> Dict[str, Any]:
    """Zone 2: Marathon (75-82% VO2max)"""
    return {
        "vo2_range": "75-82%",
        "description": "Marathon pace",
        "purpose": "Endurance building, stamina",
        "talk_test": "Can converse in short sentences",
        "typical_use": "Long runs, marathon-pace work",
        "duration_range": "60-180 minutes"
    }

def _calculate_zone3(vdot: float) -> Dict[str, Any]:
    """Zone 3: Threshold (83-88% VO2max)"""
    return {
        "vo2_range": "83-88%",
        "description": "Threshold/tempo pace",
        "purpose": "Lactate threshold improvement",
        "talk_test": "One-word answers only",
        "typical_use": "Tempo runs, cruise intervals",
        "duration_range": "20-60 minutes"
    }

def _calculate_zone4(vdot: float) -> Dict[str, Any]:
    """Zone 4: Interval (89-94% VO2max)"""
    return {
        "vo2_range": "89-94%",
        "description": "Interval/VO2max pace",
        "purpose": "VO2max improvement, economy",
        "talk_test": "Cannot talk",
        "typical_use": "Track intervals, hill repeats",
        "duration_range": "15-40 minutes (excluding rest)"
    }

def _calculate_zone5(vdot: float) -> Dict[str, Any]:
    """Zone 5: Repetition (95-100% VO2max)"""
    return {
        "vo2_range": "95-100%",
        "description": "Repetition/speed pace",
        "purpose": "Neuromuscular coordination, speed",
        "talk_test": "Impossible",
        "typical_use": "Strides, short sprints, form drills",
        "duration_range": "10-20 minutes (excluding rest)"
    }

def _vdot_to_pace(vdot_value: float) -> str:
    """Convert VDOT value to pace (simplified for example)."""
    # In production, use full Daniels formula
    # This is a placeholder
    min_per_mile = 8.0 - (vdot_value - 40) * 0.1
    return f"{min_per_mile:.1f} min/mile"

def estimate_vdot_from_race_time(distance: str, time: str) -> float:
    """Estimate VDOT from recent race performance."""
    # Parse time (format: "MM:SS" or "HH:MM:SS")
    time_parts = time.split(":")
    if len(time_parts) == 2:
        minutes, seconds = map(int, time_parts)
        total_seconds = minutes * 60 + seconds
    else:
        hours, minutes, seconds = map(int, time_parts)
        total_seconds = hours * 3600 + minutes * 60 + seconds
    
    # Distance in meters
    distance_map = {"5k": 5000, "10k": 10000, "half_marathon": 21097, "marathon": 42195}
    distance_m = distance_map.get(distance.lower(), 5000)
    
    # Calculate velocity in m/s
    velocity = distance_m / total_seconds
    
    # Simplified VDOT estimation (production would use full Daniels formula)
    vdot = velocity * 0.15  # Rough approximation
    
    return round(vdot, 1)
```

- [ ] **Step 5: Run tests**

Run: `pytest tests/test_tools/test_vdot_calculator.py -v`
Expected: All PASS

- [ ] **Step 6: Commit**

```bash
git add tools/vdot_calculator.py assets/schemas/training-zones-schema.json tests/test_tools/test_vdot_calculator.py
git commit -m "feat: implement VDOT calculator tool"
```

---

### Task 3.2: Implement Running Training Methodology

**Files:**
- Modify: `methodologies/running_training.py`
- Create: `methodologies/templates/running_programs.md`
- Test: `tests/test_methodologies/test_running_training.py`

- [ ] **Step 1: Write test for running program generation**

```python
# tests/test_methodologies/test_running_training.py
import pytest
from methodologies.running_training import generate_running_program

def test_5k_program_for_beginner():
    analysis = {
        "experience_level": "beginner",
        "goal": "5k",
        "constraints": {"time_available": "4 days per week"}
    }
    program = generate_running_program(analysis)
    
    assert program["race_distance"] == "5k"
    assert program["experience_level"] == "beginner"
    assert len(program["weeks"]) >= 8

def test_polarized_distribution_maintained():
    analysis = {"experience_level": "intermediate", "goal": "marathon"}
    program = generate_running_program(analysis)
    
    # Check 80/20 distribution
    total_volume = sum(w["volume_km"] for w in program["weeks"])
    easy_volume = sum(
        w["volume_km"] for w in program["weeks"] 
        if w.get("intensity_distribution") == "low"
    )
    
    # Should be roughly 80% low intensity
    polarized_ratio = easy_volume / total_volume
    assert 0.70 <= polarized_ratio <= 0.90  # Allow some variance
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_methodologies/test_running_training.py::test_5k_program_for_beginner -v`
Expected: FAIL with module not found

- [ ] **Step 3: Implement running program generation**

```python
# methodologies/running_training.py
from typing import Dict, Any
import tools.vdot_calculator as vdot_calc

def generate_running_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate running training program based on analysis."""
    goal = analysis.get("goal", "5k")
    experience = analysis.get("experience_level", "intermediate")
    
    if experience == "beginner":
        return build_base_building_program(analysis)
    else:
        return build_race_preparation_program(analysis)

def build_base_building_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build base building program for beginners."""
    weeks = []
    
    for week in range(1, 13):
        if week % 4 == 0:
            weeks.append(_create_deload_week(week, analysis))
        else:
            weeks.append(_create_base_week(week, analysis))
    
    return {
        "race_distance": analysis.get("goal", "5k"),
        "experience_level": "beginner",
        "program_type": "base_building",
        "weeks": weeks,
        "total_duration": "12 weeks",
        "focus": "Aerobic base development",
        "polarized_distribution": "100% low intensity (Zone 1-2)"
    }

def build_race_preparation_program(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build race preparation program with polarized training."""
    goal = analysis.get("goal", "marathon")
    weeks = []
    
    for week in range(1, 17):
        if week % 4 == 0:
            weeks.append(_create_deload_week(week, analysis))
        else:
            weeks.append(_create_polarized_week(week, analysis, goal))
    
    return {
        "race_distance": goal,
        "experience_level": "intermediate_or_advanced",
        "program_type": "race_preparation",
        "weeks": weeks,
        "total_duration": "16 weeks",
        "focus": "Race-specific preparation",
        "polarized_distribution": "80% low, 20% high intensity"
    }

def _create_base_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create a base building week."""
    days = _get_running_days(analysis)
    sessions = []
    
    for i, day in enumerate(days):
        if i == len(days) - 1:  # Last day is long run
            sessions.append({
                "day": day,
                "type": "long_run",
                "distance_km": 8 + week_num * 0.5,  # Progressive
                "intensity": "zone2",
                "description": "Long run at conversational pace"
            })
        else:
            sessions.append({
                "day": day,
                "type": "easy_run",
                "distance_km": 6,
                "intensity": "zone1",
                "description": "Easy recovery run"
            })
    
    total_volume = sum(s["distance_km"] for s in sessions)
    
    return {
        "week_number": week_num,
        "sessions": sessions,
        "volume_km": total_volume,
        "intensity_distribution": "100% low"
    }

def _create_polarized_week(week_num: int, analysis: Dict, goal: str) -> Dict[str, Any]:
    """Create a polarized training week (80/20 split)."""
    days = _get_running_days(analysis)
    sessions = []
    
    # 80% low intensity sessions
    for i, day in enumerate(days[:-1]):  # All but one quality day
        if i == len(days) - 2:  # Long run
            sessions.append({
                "day": day,
                "type": "long_run",
                "distance_km": 16 + week_num * 0.3,
                "intensity": "zone2",
                "description": "Long aerobic run"
            })
        else:
            sessions.append({
                "day": day,
                "type": "easy_run",
                "distance_km": 8,
                "intensity": "zone1",
                "description": "Recovery run"
            })
    
    # 20% high intensity session
    sessions.append(_create_quality_session(days[-1], goal))
    
    total_volume = sum(s["distance_km"] for s in sessions)
    low_volume = sum(s["distance_km"] for s in sessions if s["intensity"] in ["zone1", "zone2"])
    
    return {
        "week_number": week_num,
        "sessions": sessions,
        "volume_km": total_volume,
        "intensity_distribution": f"{round(low_volume/total_volume*100)}% low"
    }

def _create_quality_session(day: str, goal: str) -> Dict[str, Any]:
    """Create high-intensity quality session."""
    if goal in ["5k", "10k"]:
        return {
            "day": day,
            "type": "interval_workout",
            "structure": "6x400m @ Zone 4 with 400m jog recovery",
            "intensity": "zone4",
            "description": "VO2max intervals"
        }
    else:  # half marathon, marathon
        return {
            "day": day,
            "type": "tempo_run",
            "structure": "20-30 min continuous @ Zone 3",
            "intensity": "zone3",
            "description": "Threshold tempo run"
        }

def _create_deload_week(week_num: int, analysis: Dict) -> Dict[str, Any]:
    """Create deload week."""
    return {
        "week_number": week_num,
        "is_deload": True,
        "sessions": [
            {
                "day": day,
                "type": "easy_run",
                "distance_km": 5,
                "intensity": "zone1",
                "description": "Very easy recovery run"
            }
            for day in _get_running_days(analysis)[:3]
        ],
        "volume_km": 15,
        "note": "Reduce volume, focus on recovery"
    }

def _get_running_days(analysis: Dict) -> list:
    """Get running days based on constraints."""
    time_constraint = analysis.get("constraints", {}).get("time_available", "")
    
    if "4" in time_constraint:
        return ["tuesday", "wednesday", "friday", "sunday"]
    elif "5" in time_constraint:
        return ["monday", "tuesday", "wednesday", "friday", "sunday"]
    else:
        return ["tuesday", "thursday", "sunday"]  # Default 3 days
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_methodologies/test_running_training.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add methodologies/running_training.py tests/test_methodologies/test_running_training.py methodologies/templates/running_programs.md
git commit -m "feat: implement running training methodology with polarized model"
```

---

## Phase 4: Recovery & Safety

### Task 4.1: Implement Recovery Status Tool

**Files:**
- Create: `tools/recovery_status.py`
- Create: `assets/schemas/recovery-status-schema.json`
- Test: `tests/test_tools/test_recovery_status.py`

- [ ] **Step 1: Write recovery status schema**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Recovery Status Output",
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["excellent", "good", "fair", "poor"]},
    "recommendations": {"type": "array"},
    "warnings": {"type": "array"},
    "assessed_at": {"type": "string"}
  },
  "required": ["status"]
}
```

- [ ] **Step 2: Write test for recovery status**

```python
# tests/test_tools/test_recovery_status.py
import pytest
from tools.recovery_status import determine_recovery_status

def test_good_recovery_status():
    result = determine_recovery_status(
        sleep_hours=8,
        resting_hr=60,
        mood="good",
        performance_trend="improving"
    )
    
    assert result["status"] == "good"
    assert len(result["recommendations"]) == 0

def test_poor_recovery_triggers_warnings():
    result = determine_recovery_status(
        sleep_hours=5,
        resting_hr=75,
        mood="exhausted",
        performance_trend="declining"
    )
    
    assert result["status"] == "poor"
    assert len(result["warnings"]) > 0
    assert "deload" in str(result["recommendations"]).lower()
```

- [ ] **Step 3: Implement recovery status tool**

```python
# tools/recovery_status.py
from datetime import datetime
from typing import Dict, Any, List

def determine_recovery_status(sleep_hours: int, resting_hr: int, 
                            mood: str, performance_trend: str) -> Dict[str, Any]:
    """Determine recovery status from subjective and objective markers."""
    warnings = []
    recommendations = []
    
    # Assess sleep
    sleep_score = _assess_sleep(sleep_hours)
    
    # Assess resting HR (assuming baseline of 60 for example)
    hr_elevated = resting_hr > 65
    if hr_elevated:
        warnings.append("Elevated resting heart rate detected")
    
    # Assess mood
    mood_score = _assess_mood(mood)
    
    # Assess performance
    performance_score = _assess_performance(performance_trend)
    
    # Overall status
    total_score = sleep_score + mood_score + performance_score
    if hr_elevated:
        total_score -= 1
    
    if total_score >= 3:
        status = "excellent"
    elif total_score >= 2:
        status = "good"
    elif total_score >= 1:
        status = "fair"
        recommendations.append("Consider reducing training volume by 20%")
    else:
        status = "poor"
        warnings.append("Recovery concerns detected")
        recommendations.append("Implement deload week immediately")
        recommendations.append("Prioritize sleep and stress management")
    
    return {
        "status": status,
        "recommendations": recommendations,
        "warnings": warnings,
        "assessed_at": datetime.now().isoformat()
    }

def _assess_sleep(hours: int) -> int:
    """Score sleep quality (0-2)."""
    if hours >= 8:
        return 2
    elif hours >= 7:
        return 1
    else:
        return 0

def _assess_mood(mood: str) -> int:
    """Score mood state (0-2)."""
    mood_lower = mood.lower()
    if mood_lower in ["energized", "motivated", "excellent"]:
        return 2
    elif mood_lower in ["good", "normal", "ready"]:
        return 1
    else:
        return 0

def _assess_performance(trend: str) -> int:
    """Score performance trend (0-2)."""
    trend_lower = trend.lower()
    if trend_lower in ["improving", "progressing"]:
        return 2
    elif trend_lower in ["stable", "maintaining"]:
        return 1
    else:
        return 0
```

- [ ] **Step 4: Run tests**

Run: `pytest tests/test_tools/test_recovery_status.py -v`
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add tools/recovery_status.py assets/schemas/recovery-status-schema.json tests/test_tools/test_recovery_status.py
git commit -m "feat: implement recovery status assessment tool"
```

---

### Task 4.2: Implement Recovery Methodology

**Files:**
- Modify: `methodologies/recovery.py`
- Test: `tests/test_methodologies/test_recovery.py`

- [ ] **Step 1: Write test for recovery plan**

```python
# tests/test_methodologies/test_recovery.py
import pytest
from methodologies.recovery import generate_recovery_plan

def test_recovery_plan_for_overtraining():
    analysis = {
        "flags": ["recovery_concern"],
        "constraints": {},
        "goal": "recovery"
    }
    plan = generate_recovery_plan(analysis)
    
    assert plan["type"] == "recovery"
    assert plan["focus"] == "recovery prioritized"
    assert len(plan["weeks"]) >= 2

def test_recovery_plan_includes_deload():
    analysis = {"flags": ["recovery_concern"]}
    plan = generate_recovery_plan(analysis)
    
    assert any("deload" in str(w).lower() for w in plan["weeks"])
```

- [ ] **Step 2: Implement recovery plan**

```python
# methodologies/recovery.py
from typing import Dict, Any
import tools.recovery_status as recovery_tool

def generate_recovery_plan(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate recovery-focused training plan."""
    flags = analysis.get("flags", [])
    
    if "recovery_concern" in flags:
        return build_active_recovery_plan(analysis)
    else:
        return build_maintenance_plan(analysis)

def build_active_recovery_plan(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build active recovery plan for overtraining concerns."""
    weeks = []
    
    for week in range(1, 5):
        weeks.append({
            "week_number": week,
            "focus": "Active Recovery",
            "sessions": [
                {
                    "day": day,
                    "type": "very_easy",
                    "duration": "20-30 min",
                    "intensity": "zone1",
                    "description": "Very light activity only"
                }
                for day in ["monday", "wednesday", "friday"]
            ],
            "recovery_focus": [
                "8+ hours sleep nightly",
                "Hydration prioritized",
                "Stress management",
                "Light mobility work"
            ]
        })
    
    return {
        "type": "recovery",
        "focus": "Active recovery protocol",
        "duration": "4 weeks",
        "weeks": weeks,
        "recommendations": [
            "Stop all structured training",
            "Focus on sleep and nutrition",
            "Light activity only (walking, stretching)",
            "Monitor resting heart rate daily",
            "Reassess after 2 weeks"
        ],
        "warning_signs_to_monitor": [
            "Persistent fatigue",
            "Sleep disturbances",
            "Elevated resting heart rate",
            "Mood changes",
            "Performance decline"
        ]
    }

def build_maintenance_plan(analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Build light maintenance plan."""
    weeks = []
    
    for week in range(1, 3):
        weeks.append({
            "week_number": week,
            "sessions": [
                {
                    "day": day,
                    "type": "maintenance",
                    "duration": "30-40 min",
                    "intensity": "zone1-2",
                    "description": "Light activity to maintain base"
                }
                for day in ["tuesday", "thursday", "saturday"]
            ]
        })
    
    return {
        "type": "maintenance",
        "focus": "Maintain fitness while prioritizing recovery",
        "weeks": weeks
    }
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_methodologies/test_recovery.py -v`
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add methodologies/recovery.py tests/test_methodologies/test_recovery.py methodologies/templates/recovery_protocols.md
git commit -m "feat: implement recovery methodology with active recovery plans"
```

---

## Phase 5: Validation & Testing

### Task 5.1: Implement Program Validator

**Files:**
- Create: `validators/program_validator.py`
- Test: `tests/test_validators/test_program_validator.py`

- [ ] **Step 1: Write test for program validator**

```python
# tests/test_validators/test_program_validator.py
import pytest
from validators.program_validator import ProgramValidator

def test_validator_passes_complete_program():
    validator = ProgramValidator()
    program = {
        "type": "strength",
        "periodization_model": "linear",
        "weeks": [{"week_number": 1, "sessions": []}],
        "progression_rules": {},
        "deload_schedule": [4, 8],
        "warning_signs": ["Stop if pain persists"]
    }
    
    result = validator.validate(program)
    assert result.passed == True
    assert len(result.missing_elements) == 0

def test_validator_catches_missing_disclaimer():
    validator = ProgramValidator()
    program = {
        "type": "strength",
        "weeks": [{"week_number": 1}]
    }
    
    result = validator.validate(program)
    assert result.passed == False
    assert "disclaimer" in result.missing_elements

def test_validator_checks_deload_schedule():
    validator = ProgramValidator()
    program = {
        "type": "strength",
        "weeks": [{"week_number": 1}, {"week_number": 2}, {"week_number": 3}]
    }
    
    result = validator.validate(program)
    assert "deload_schedule" in result.missing_elements
```

- [ ] **Step 2: Implement program validator**

```python
# validators/program_validator.py
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ValidationResult:
    passed: bool
    missing_elements: List[str]
    warnings: List[str]

class ProgramValidator:
    """Validate training programs for completeness and compliance."""
    
    VALIDATION_RULES = [
        "disclaimer_included",
        "experience_level_appropriate",
        "progressive_overload_defined",
        "recovery_scheduled",
        "deload_planned",
        "warning_signs_listed"
    ]
    
    def validate(self, program: Dict[str, Any]) -> ValidationResult:
        """Validate program against all rules."""
        missing_elements = []
        warnings = []
        
        # Check required fields
        if "disclaimer" not in program:
            missing_elements.append("disclaimer")
        
        if "weeks" not in program or not program["weeks"]:
            missing_elements.append("weeks")
        
        # Check progression rules
        if "progression_rules" not in program:
            missing_elements.append("progression_rules")
        
        # Check deload schedule for strength programs
        if program.get("type") == "strength" and "deload_schedule" not in program:
            missing_elements.append("deload_schedule")
        
        # Check warning signs
        if "warning_signs" not in program:
            missing_elements.append("warning_signs")
        
        # Check for recovery scheduling
        if program.get("weeks"):
            has_recovery = any(
                "rest" in str(week).lower() or "recovery" in str(week).lower()
                for week in program["weeks"]
            )
            if not has_recovery:
                warnings.append("No explicit recovery days scheduled")
        
        passed = len(missing_elements) == 0
        
        return ValidationResult(
            passed=passed,
            missing_elements=missing_elements,
            warnings=warnings
        )
    
    def add_missing_elements(self, program: Dict[str, Any], 
                            missing: List[str]) -> Dict[str, Any]:
        """Add missing required elements to program."""
        if "disclaimer" in missing:
            program["disclaimer"] = self._get_standard_disclaimer()
        
        if "progression_rules" in missing:
            program["progression_rules"] = self._get_default_progression_rules()
        
        if "warning_signs" in missing:
            program["warning_signs"] = self._get_default_warning_signs()
        
        if "deload_schedule" in missing:
            program["deload_schedule"] = [4, 8, 12]
        
        return program
    
    def _get_standard_disclaimer(self) -> str:
        """Get standard medical disclaimer."""
        return "**Disclaimer:** This program provides general educational information. Consult a physician before starting any exercise program, especially if you have pre-existing health conditions."
    
    def _get_default_progression_rules(self) -> Dict[str, str]:
        """Get default progression rules."""
        return {
            "load_progression": "Increase weight when 2+ reps above target",
            "deload_frequency": "Every 4 weeks",
            "form_priority": "Never sacrifice form for load"
        }
    
    def _get_default_warning_signs(self) -> List[str]:
        """Get default warning signs."""
        return [
            "Stop if you experience sharp pain",
            "Consult physician if pain persists",
            "Prioritize form over load"
        ]
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_validators/test_program_validator.py -v`
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add validators/program_validator.py tests/test_validators/test_program_validator.py
git commit -m "feat: implement program validator with completeness checks"
```

---

### Task 5.2: Implement Output Formatter

**Files:**
- Create: `validators/output_formatter.py`
- Test: `tests/test_validators/test_output_formatter.py`

- [ ] **Step 1: Write test for output formatter**

```python
# tests/test_validators/test_output_formatter.py
import pytest
from validators.output_formatter import format_program

def test_formatter_adds_structure():
    program = {"type": "strength", "weeks": [{"week_number": 1}]}
    formatted = format_program(program, "strength")
    
    assert "title" in formatted
    assert "disclaimer" in formatted
    assert "overview" in formatted
    assert "weekly_schedule" in formatted

def test_formatter_maintains_program_content():
    program = {"type": "strength", "weeks": [{"week_number": 1, "sessions": []}]}
    formatted = format_program(program, "strength")
    
    assert len(formatted["weeks"]) == len(program["weeks"])
```

- [ ] **Step 2: Implement output formatter**

```python
# validators/output_formatter.py
from typing import Dict, Any

def format_program(program: Dict[str, Any], methodology: str) -> Dict[str, Any]:
    """Format program into consistent output structure."""
    
    formatted = {
        "title": _generate_title(program, methodology),
        "disclaimer": _get_disclaimer(program),
        "overview": _create_overview(program),
        "weekly_schedule": program.get("weeks", []),
        "exercise_details": _extract_exercise_details(program),
        "progression_rules": program.get("progression_rules", {}),
        "deload_schedule": program.get("deload_schedule", []),
        "warning_signs": program.get("warning_signs", []),
        "notes": _generate_notes(program)
    }
    
    return formatted

def _generate_title(program: Dict, methodology: str) -> str:
    """Generate program title."""
    experience = program.get("experience_level", "intermediate").capitalize()
    goal = program.get("goal", methodology).capitalize()
    return f"{experience} {goal} Training Program"

def _get_disclaimer(program: Dict) -> str:
    """Get disclaimer from program or default."""
    return program.get("disclaimer", 
        "**Disclaimer:** This program provides general educational information. Consult a qualified professional before starting.")

def _create_overview(program: Dict) -> Dict[str, Any]:
    """Create program overview."""
    return {
        "duration": program.get("total_duration", "12 weeks"),
        "frequency": program.get("sessions_per_week", "3-4 days per week"),
        "goal": program.get("goal", "general fitness"),
        "experience_level": program.get("experience_level", "intermediate"),
        "periodization": program.get("periodization_model", "linear")
    }

def _extract_exercise_details(program: Dict) -> list:
    """Extract exercise details from program."""
    exercises = []
    
    for week in program.get("weeks", []):
        for session in week.get("sessions", []):
            for exercise in session.get("exercises", []):
                if exercise not in exercises:
                    exercises.append(exercise)
    
    return exercises

def _generate_notes(program: Dict) -> list:
    """Generate program notes."""
    notes = program.get("notes", [])
    
    if program.get("type") == "running":
        notes.append("Maintain polarized distribution: ~80% easy, 20% hard")
    
    if program.get("experience_level") == "beginner":
        notes.append("Focus on form before load")
    
    return notes
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_validators/test_output_formatter.py -v`
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add validators/output_formatter.py tests/test_validators/test_output_formatter.py
git commit -m "feat: implement output formatter for consistent structure"
```

---

### Task 5.3: Implement Safety Checker

**Files:**
- Create: `validators/safety_checker.py`
- Test: `tests/test_validators/test_safety_checker.py`

- [ ] **Step 1: Write test for safety checker**

```python
# tests/test_validators/test_safety_checker.py
import pytest
from validators.safety_checker import SafetyChecker

def test_medical_concern_triggers_warning():
    checker = SafetyChecker()
    analysis = {"flags": ["medical_concern"]}
    
    result = checker.check(analysis)
    assert result.passed == False
    assert "medical_clearance" in result.warnings

def test_injury_requires_modification():
    checker = SafetyChecker()
    analysis = {"constraints": {"health_conditions": ["knee"]}}
    
    result = checker.check(analysis)
    assert result.modifications_required == True
```

- [ ] **Step 2: Implement safety checker**

```python
# validators/safety_checker.py
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class SafetyCheckResult:
    passed: bool
    warnings: List[str]
    modifications_required: bool
    recommended_modifications: List[str]

class SafetyChecker:
    """Check programs for safety concerns and contraindications."""
    
    def check(self, analysis: Dict[str, Any]) -> SafetyCheckResult:
        """Perform safety check on program analysis."""
        warnings = []
        modifications = []
        
        flags = analysis.get("flags", [])
        health_conditions = analysis.get("constraints", {}).get("health_conditions", [])
        
        # Check for medical concerns
        if "medical_concern" in flags:
            warnings.append("Medical concern detected - physician clearance recommended")
        
        if "eating_disorder_concern" in flags:
            warnings.append("Eating disorder concern - professional help recommended")
        
        # Check for injuries requiring modifications
        if "knee" in health_conditions:
            modifications.append("Avoid high-impact exercises")
            modifications.append("Reduce squat depth if painful")
        
        if "shoulder" in health_conditions:
            modifications.append("Avoid overhead pressing")
            modifications.append("Focus on neutral grip exercises")
        
        if "back" in health_conditions:
            modifications.append("Avoid heavy spinal loading")
            modifications.append("Prioritize core strengthening")
        
        # Check for recovery concerns
        if "recovery_concern" in flags:
            warnings.append("Recovery concern detected - deload recommended")
            modifications.append("Reduce training volume by 50%")
        
        passed = len(warnings) == 0 or all("physician" in w for w in warnings)
        
        return SafetyCheckResult(
            passed=passed,
            warnings=warnings,
            modifications_required=len(modifications) > 0,
            recommended_modifications=modifications
        )
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_validators/test_safety_checker.py -v`
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add validators/safety_checker.py tests/test_validators/test_safety_checker.py
git commit -m "feat: implement safety checker for contraindications"
```

---

## Phase 6: Production Features

### Task 6.1: Implement Hooks System

**Files:**
- Create: `hooks/pre_processing.py`
- Create: `hooks/post_processing.py`
- Create: `hooks/error_handlers.py`
- Create: `hooks/state_management.py`
- Modify: `router.py` (integrate hooks)

- [ ] **Step 1: Implement pre-processing hooks**

```python
# hooks/pre_processing.py
from typing import Dict, Any

def before_program_generation(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute pre-processing validation before program generation."""
    warnings = []
    
    # Validate required fields
    if not input_data.get("raw_input"):
        raise ValueError("User input is required")
    
    # Check for medical concerns
    if "medical_concern" in input_data.get("flags", []):
        warnings.append("Medical concern detected - disclaimer will be added")
    
    # Check experience level
    if not input_data.get("experience_level"):
        warnings.append("Experience level not classified - using default")
        input_data["experience_level"] = "intermediate"
    
    # Store warnings in input for later use
    input_data["pre_warnings"] = warnings
    
    return input_data
```

- [ ] **Step 2: Implement post-processing hooks**

```python
# hooks/post_processing.py
from typing import Dict, Any
from validators.program_validator import ProgramValidator

def after_program_generation(program: Dict[str, Any]) -> Dict[str, Any]:
    """Execute post-processing validation and formatting."""
    validator = ProgramValidator()
    
    # Validate program
    validation_result = validator.validate(program)
    
    if not validation_result.passed:
        # Add missing elements
        program = validator.add_missing_elements(
            program, 
            validation_result.missing_elements
        )
    
    # Add validation warnings to program
    if validation_result.warnings:
        program.setdefault("validation_warnings", []).extend(validation_result.warnings)
    
    return program
```

- [ ] **Step 3: Implement error handlers**

```python
# hooks/error_handlers.py
from typing import Dict, Any, Callable
import logging

logger = logging.getLogger(__name__)

def on_error(error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
    """Handle errors during program generation."""
    error_type = type(error).__name__
    
    logger.error(f"Error in program generation: {error_type}: {str(error)}")
    
    # Classify error level
    if "ValueError" in error_type or "KeyError" in error_type:
        # Input validation error
        return {
            "error": True,
            "error_type": "input_error",
            "message": str(error),
            "resolution": "Please provide more specific information"
        }
    elif "FileNotFound" in error_type or "ImportError" in error_type:
        # System error
        return {
            "error": True,
            "error_type": "system_error",
            "message": "System error occurred",
            "resolution": "Using simplified program generation"
        }
    else:
        # Unknown error
        return {
            "error": True,
            "error_type": "unknown_error",
            "message": "An error occurred",
            "resolution": "Please try again or consult support"
        }
```

- [ ] **Step 4: Implement state management**

```python
# hooks/state_management.py
from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path(".sessions")

def save_session(session_id: str, session_data: Dict[str, Any]) -> None:
    """Save session data to disk."""
    SESSIONS_DIR.mkdir(exist_ok=True)
    session_file = SESSIONS_DIR / f"{session_id}.json"
    
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2, default=str)

def load_session(session_id: str) -> Dict[str, Any]:
    """Load session data from disk."""
    session_file = SESSIONS_DIR / f"{session_id}.json"
    
    if session_file.exists():
        with open(session_file) as f:
            return json.load(f)
    
    return None

def update_program_history(session_id: str, program: Dict[str, Any]) -> None:
    """Update program history in session."""
    session = load_session(session_id)
    
    if session:
        session.setdefault("program_history", []).append({
            "timestamp": datetime.now().isoformat(),
            "program_summary": {
                "type": program.get("type"),
                "goal": program.get("goal")
            }
        })
        session["iteration_count"] = len(session["program_history"])
        save_session(session_id, session)
```

- [ ] **Step 5: Integrate hooks into router**

```python
# Modify router.py
import hooks.pre_processing as pre_hooks
import hooks.post_processing as post_hooks
import hooks.error_handlers as error_hooks
import hooks.state_management as state_hooks

    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Main entry point with hooks integration."""
        try:
            # Pre-processing hook
            analysis = self.analyze_input(user_input)
            analysis = pre_hooks.before_program_generation(analysis)
            
            # Select methodology and generate
            methodology = self._select_methodology(analysis)
            
            if methodology == "strength":
                program = strength_training.generate_strength_program(analysis)
            elif methodology == "running":
                program = running_training.generate_running_program(analysis)
            elif methodology == "recovery":
                program = recovery.generate_recovery_plan(analysis)
            else:
                program = general.generate_general_program(analysis)
            
            # Post-processing hook
            program = post_hooks.after_program_generation(program)
            
            # Update session
            self.session["iteration_count"] += 1
            self.session["program_history"].append({
                "iteration": self.session["iteration_count"],
                "timestamp": datetime.now().isoformat(),
                "methodology": methodology,
                "program_summary": {"type": program.get("type")}
            })
            
            # Save session
            state_hooks.save_session(self.session_id, self.session)
            
            return {
                "program": program,
                "session_id": self.session_id,
                "iteration": self.session["iteration_count"]
            }
            
        except Exception as e:
            # Error hook
            context = {"session_id": self.session_id, "input": user_input}
            return error_hooks.on_error(e, context)
```

- [ ] **Step 6: Write tests for hooks**

```python
# tests/test_hooks/test_hooks.py
import pytest
from hooks.pre_processing import before_program_generation
from hooks.post_processing import after_program_generation
from hooks.error_handlers import on_error

def test_pre_processing_validates_input():
    input_data = {"raw_input": "I want to get stronger"}
    result = before_program_generation(input_data)
    assert "experience_level" in result

def test_post_processing_adds_missing_elements():
    program = {"type": "strength"}
    result = after_program_generation(program)
    assert "disclaimer" in result

def test_error_handler_classifies_errors():
    try:
        raise ValueError("Test error")
    except Exception as e:
        result = on_error(e, {})
        assert result["error_type"] == "input_error"
```

- [ ] **Step 7: Run tests**

Run: `pytest tests/test_hooks/ -v`
Expected: All PASS

- [ ] **Step 8: Commit**

```bash
git add hooks/ router.py tests/test_hooks/
git commit -m "feat: implement hooks system with pre/post processing and error handling"
```

---

### Task 6.2: Implement Session Persistence

**Files:**
- Modify: `hooks/state_management.py` (enhance)
- Test: `tests/test_hooks/test_state_management.py`

- [ ] **Step 1: Write test for session persistence**

```python
def test_session_persists_to_disk():
    session_id = "test-session"
    session_data = {"test": "data", "timestamp": "now"}
    
    save_session(session_id, session_data)
    loaded = load_session(session_id)
    
    assert loaded["test"] == "data"

def test_session_history_updates():
    session_id = "test-session-history"
    program = {"type": "strength"}
    
    update_program_history(session_id, program)
    updated = load_session(session_id)
    
    assert len(updated["program_history"]) == 1
```

- [ ] **Step 2: Implement enhanced session management**

```python
# Modify hooks/state_management.py
from typing import Dict, Any
import json
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path(".sessions")

def create_session(session_id: str = None) -> Dict[str, Any]:
    """Create new session."""
    if session_id is None:
        import uuid
        session_id = str(uuid.uuid4())
    
    return {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "user_profile": {},
        "program_history": [],
        "iteration_count": 0
    }

def save_session(session_id: str, session_data: Dict[str, Any]) -> None:
    """Save session data to disk."""
    SESSIONS_DIR.mkdir(exist_ok=True)
    session_file = SESSIONS_DIR / f"{session_id}.json"
    
    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2, default=str)

def load_session(session_id: str) -> Dict[str, Any]:
    """Load session data from disk."""
    session_file = SESSIONS_DIR / f"{session_id}.json"
    
    if session_file.exists():
        with open(session_file) as f:
            return json.load(f)
    
    return None

def update_program_history(session_id: str, program: Dict[str, Any]) -> None:
    """Update program history in session."""
    session = load_session(session_id)
    
    if session is None:
        session = create_session(session_id)
    
    session.setdefault("program_history", []).append({
        "timestamp": datetime.now().isoformat(),
        "iteration": len(session.get("program_history", [])) + 1,
        "program_summary": {
            "type": program.get("type"),
            "goal": program.get("goal"),
            "experience_level": program.get("experience_level")
        }
    })
    
    session["iteration_count"] = len(session["program_history"])
    save_session(session_id, session)
```

- [ ] **Step 3: Run tests**

Run: `pytest tests/test_hooks/test_state_management.py -v`
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add hooks/state_management.py tests/test_hooks/test_state_management.py
git commit -m "feat: implement enhanced session persistence"
```

---

## Phase 7: Packaging & Distribution

### Task 7.1: Create Documentation

**Files:**
- Create: `README.md`
- Create: `CONTRIBUTING.md`
- Create: `LICENSE`
- Create: `CHANGELOG.md`
- Create: `docs/architecture.md`

- [ ] **Step 1: Write README**

```markdown
# Gym Training & Running Coach Advisor

A production-grade skill for designing evidence-based strength-training and running programs grounded in exercise-physiology and sports-science research.

## Features

- **Progressive Overload**: Systematic progression protocols for all experience levels
- **Periodization Models**: Linear, Undulating (DUP), and Block periodization
- **Running Training**: Polarized training model with VDOT-based zones
- **Recovery Monitoring**: Overtraining syndrome detection and deload protocols
- **Safety-First**: Comprehensive validation and disclaimers

## Installation

### For Users

1. Install Claude Code or Claude.ai
2. Add this skill to your skills directory
3. Trigger the skill when asking about training programs

### For Developers

```bash
# Clone repository
git clone <repository-url>
cd gym-running-training-advisor

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Package skill
python scripts/package_skill.py
```

## Usage

### Basic Usage

```
You: "I'm a beginner wanting to get stronger. Can you design a program?"
[Skill generates progressive strength program with linear periodization]
```

### Advanced Usage

```
You: "I've been training 5 years and want to qualify for Boston Marathon. 
     Currently running 40 miles/week but feeling exhausted."
[Skill detects recovery concern, generates polarized marathon plan with recovery adjustments]
```

## Architecture

- **Router Pattern**: Lightweight orchestrator with domain-specific methodologies
- **Tool System**: Reusable calculators (VDOT, 1RM, Recovery Status)
- **Validation Layer**: Comprehensive safety and quality checks
- **Hooks System**: Pre/post-processing and error handling

## Disclaimer

This skill provides general educational information. It is not a substitute for advice from a qualified professional (physician, physical therapist, certified personal trainer). Always consult with a qualified professional before starting any new exercise program.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - see [LICENSE](LICENSE) file
```

- [ ] **Step 2: Write CONTRIBUTING guide**

```markdown
# Contributing to Gym Training & Running Coach Advisor

## Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Adding New Methodologies

1. Create new file in `methodologies/`
2. Implement `generate_*_program(analysis)` function
3. Add routing logic in `router.py`
4. Write tests in `tests/test_methodologies/`
5. Update documentation

## Adding New Tools

1. Create tool in `tools/`
2. Define JSON schema in `assets/schemas/`
3. Write tests in `tests/test_tools/`
4. Document in `docs/api_reference.md`

## Code Standards

- Follow TDD: Write tests first
- No placeholders or TODOs
- All code must have tests
- Commit messages: `feat:`, `fix:`, `docs:`, `test:`

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific tests
pytest tests/test_methodologies/ -v

# Check coverage
pytest tests/ --cov=methodologies --cov=tools
```

## Pull Request Process

1. Update documentation
2. Ensure all tests pass
3. Add tests for new features
4. Update CHANGELOG.md
```

- [ ] **Step 3: Create LICENSE (MIT)**

```markdown
MIT License

Copyright (c) 2026 Gym Training & Running Coach Advisor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

- [ ] **Step 4: Create CHANGELOG**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-08-05

### Added
- Complete router architecture with methodology routing
- Progressive overload implementation
- Linear, Undulating (DUP), and Block periodization models
- Running training with polarized model
- VDOT-based training zones calculator
- Recovery status assessment tool
- Comprehensive validation and safety checking
- Hooks system for pre/post-processing
- Session persistence
- Complete test suite
- Production documentation

### Tested
- All 7 phases validated and tested
- >80% code coverage achieved
- Integration tests for full flow
```

- [ ] **Step 5: Write architecture documentation**

```markdown
# Architecture

## System Overview

The Gym Training & Running Coach Advisor uses a Router Pattern architecture with domain-specialized methodology functions.

## Components

### Router (`router.py`)
Main orchestrator that:
- Analyzes user input
- Routes to appropriate methodology
- Manages session state
- Coordinates hooks execution

### Methodologies (`methodologies/`)
Domain-specific training logic:
- `strength_training.py`: Linear, DUP, Block periodization
- `running_training.py`: Polarized running programs
- `recovery.py`: Active recovery protocols
- `shared_utils.py`: Classification and utilities

### Tools (`tools/`)
Reusable calculators:
- `vdot_calculator.py`: VDOT-based training zones
- `one_rm_estimator.py`: 1RM estimation
- `recovery_status.py`: Recovery assessment

### Validators (`validators/`)
Quality assurance:
- `program_validator.py`: Completeness checks
- `safety_checker.py`: Contraindication detection
- `output_formatter.py`: Consistent formatting

### Hooks (`hooks/`)
Lifecycle management:
- `pre_processing.py`: Input validation
- `post_processing.py`: Output validation
- `error_handlers.py`: Error handling
- `state_management.py`: Session persistence

## Data Flow

```
User Input → Pre-processing Hook → Analysis → 
Methodology Selection → Program Generation → 
Post-processing Hook → Validation → Output
```

## Extension Points

- New methodology: Add function to `methodologies/`
- New tool: Add to `tools/` with schema
- New validation: Add to `validators/`
```

- [ ] **Step 6: Commit**

```bash
git add README.md CONTRIBUTING.md LICENSE CHANGELOG.md docs/architecture.md
git commit -m "docs: add comprehensive documentation for open-source release"
```

---

### Task 7.2: Update Phase Tracking

**Files:**
- Modify: `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`

- [ ] **Step 1: Mark all phases complete**

```markdown
# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — Gym Training & Running Coach Advisor

## Phase Completion Matrix

| Phase | Status | Completion % | Last Updated |
|-------|--------|--------------|--------------|
| Phase 1 - Foundation | ✅ Complete | 100% | 2026-08-05 |
| Phase 2 - Periodization Models | ✅ Complete | 100% | 2026-08-05 |
| Phase 3 - Running Training | ✅ Complete | 100% | 2026-08-05 |
| Phase 4 - Recovery & Safety | ✅ Complete | 100% | 2026-08-05 |
| Phase 5 - Testing & Polish | ✅ Complete | 100% | 2026-08-05 |
| Phase 6 - Architecture & Productionization | ✅ Complete | 100% | 2026-08-05 |
| Phase 7 - Packaging & Distribution | ✅ Complete | 100% | 2026-08-05 |

## Project Status

**Status:** ✅ PRODUCTION COMPLETE
**Version:** 1.0.0
**Completion Date:** 2026-08-05

All 7 phases completed to production-grade standards.
```

- [ ] **Step 2: Commit**

```bash
git add PROJECT-DEVELOPMENT-PHASE-TRACKING.md
git commit -m "docs: mark all phases complete (100%)"
```

---

### Task 7.3: Final Integration Test

**Files:**
- Create: `tests/integration/test_full_flow.py`

- [ ] **Step 1: Write comprehensive integration test**

```python
# tests/integration/test_full_flow.py
import pytest
from router import TrainingAdvisorRouter

def test_full_flow_beginner_strength():
    """Test complete flow for beginner strength program."""
    router = TrainingAdvisorRouter()
    
    result = router.process_request(
        "I'm a beginner wanting to get stronger, can train 3 days per week"
    )
    
    # Verify structure
    assert "program" in result
    assert "session_id" in result
    assert "iteration" in result
    
    # Verify program content
    program = result["program"]
    assert program["type"] == "strength"
    assert program["periodization_model"] == "linear"
    assert "disclaimer" in program
    assert "weeks" in program
    assert len(program["weeks"]) >= 8
    
    # Verify validation passed
    assert "warning_signs" in program
    assert "progression_rules" in program

def test_full_flow_intermediate_running():
    """Test complete flow for intermediate running program."""
    router = TrainingAdvisorRouter()
    
    result = router.process_request(
        "I want to run a marathon, been training 2 years"
    )
    
    program = result["program"]
    assert program["type"] == "running"
    assert program["race_distance"] == "marathon"
    assert "polarized_distribution" in program

def test_session_persistence_across_requests():
    """Test session persists across multiple requests."""
    router = TrainingAdvisorRouter()
    
    result1 = router.process_request("I want to get stronger")
    session_id = result1["session_id"]
    
    # Create new router with same session
    router2 = TrainingAdvisorRouter(session_id=session_id)
    result2 = router2.process_request("Can you make it 4 days per week instead?")
    
    assert result2["iteration"] == 2

def test_recovery_concern_routing():
    """Test recovery concerns route correctly."""
    router = TrainingAdvisorRouter()
    
    result = router.process_request(
        "I've been feeling exhausted all week despite sleeping"
    )
    
    program = result["program"]
    assert program["type"] == "recovery"
    assert "recommendations" in program

def test_error_handling_invalid_input():
    """Test error handling for invalid input."""
    router = TrainingAdvisorRouter()
    
    # Should handle gracefully, not crash
    result = router.process_request("")
    
    assert "error" in result or "program" in result

@pytest.mark.parametrize("experience,goal,expected_periodization", [
    ("beginner", "strength", "linear"),
    ("intermediate", "strength", "undulating"),
    ("advanced", "strength", "block"),
])
def test_periodization_routing(experience, goal, expected_periodization):
    """Test periodization models route correctly."""
    router = TrainingAdvisorRouter()
    
    result = router.process_request(
        f"I'm {experience} wanting to improve {goal}"
    )
    
    program = result["program"]
    if program["type"] == "strength":
        assert program["periodization_model"] == expected_periodization
```

- [ ] **Step 2: Run integration tests**

Run: `pytest tests/integration/test_full_flow.py -v`
Expected: All PASS

- [ ] **Step 3: Run all tests for final verification**

Run: `pytest tests/ -v --cov=.`
Expected: All PASS, >80% coverage

- [ ] **Step 4: Commit**

```bash
git add tests/integration/test_full_flow.py
git commit -m "test: add comprehensive integration tests for full flow validation"
```

---

### Task 7.4: Final Code Review

**Files:**
- All project files

- [ ] **Step 1: Run final review checklist**

```bash
# Check for any remaining TODOs or placeholders
grep -r "TODO\|FIXME\|PLACEHOLDER\|XXX" methodologies/ tools/ validators/ hooks/ router.py

# Verify all tests pass
pytest tests/ -v

# Check code coverage
pytest tests/ --cov=. --cov-report=term-missing

# Verify documentation is complete
ls -la README.md CONTRIBUTING.md LICENSE CHANGELOG.md docs/

# Verify phase tracking is complete
cat PROJECT-DEVELOPMENT-PHASE-TRACKING.md
```

- [ ] **Step 2: Verify no placeholders**

Expected: No TODO, FIXME, PLACEHOLDER, or XXX found

- [ ] **Step 3: Final commit**

```bash
git add .
git commit -m "feat: complete production-grade upgrade (v1.0.0)

- Implemented complete Router Pattern architecture
- Added all periodization models (linear, DUP, block)
- Added running training with polarized model
- Added recovery monitoring and safety checks
- Added comprehensive validation layer
- Added hooks system with pre/post processing
- Added session persistence
- Achieved >80% test coverage
- Complete documentation for open-source release

All 7 phases marked 100% complete in PROJECT-DEVELOPMENT-PHASE-TRACKING.md"
```

---

### Task 7.5: Tag Release

**Files:**
- Git repository

- [ ] **Step 1: Create version tag**

```bash
git tag -a v1.0.0 -m "Production release v1.0.0

Complete gym-running-training-advisor skill with:
- Progressive overload for all experience levels
- Complete periodization models
- Running training with polarized distribution
- Recovery and safety monitoring
- Production-grade validation and error handling
- Comprehensive documentation"

git push origin v1.0.0
```

---

## Summary

This implementation plan contains **50+ tasks** broken down into bite-sized steps following TDD principles:

**Phase 1 (8 tasks):** Foundation - Router, shared utilities, configuration
**Phase 2 (3 tasks):** Periodization - Linear, DUP, Block models
**Phase 3 (2 tasks):** Running - VDOT calculator, polarized training
**Phase 4 (2 tasks):** Recovery - Status tool, recovery plans
**Phase 5 (3 tasks):** Validation - Program validator, formatter, safety checker
**Phase 6 (2 tasks):** Production - Hooks system, session persistence
**Phase 7 (5 tasks):** Packaging - Documentation, testing, release

**Total:** 25 major tasks with 150+ individual steps

Each step:
- Takes 2-5 minutes to complete
- Follows TDD (test first, then implement)
- Includes exact file paths and complete code
- Has verification steps
- Ends with commit

**Success Criteria:**
- All tests passing (>80% coverage)
- No placeholders or TODOs
- All phases marked 100% complete
- Production documentation complete
- Ready for open-source distribution

**Estimated Effort:** 40-50 hours for complete implementation
