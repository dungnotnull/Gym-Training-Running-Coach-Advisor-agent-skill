# Hooks System Definition

This document defines the lifecycle hooks and event system for the Gym Training & Running Coach Advisor skill.

## Hook Architecture

The hooks system provides a way to intercept and modify behavior at key points in the skill execution lifecycle. Hooks enable:

- Input validation and safety checking
- State synchronization between components
- Event emission for monitoring and logging
- Graceful error handling and fallbacks

## Hook Types

### 1. Pre-Processing Hooks

**`before_program_generation(input)`**

Executes before any program generation begins.

**Purpose:**
- Validate user input completeness
- Check for safety concerns requiring disclaimer
- Verify experience level classification
- Detect special considerations flags

**Input Schema:**
```json
{
  "user_request": "string",
  "experience_level": "beginner|intermediate|advanced",
  "training_goal": "string",
  "constraints": {
    "time_available": "string",
    "equipment": ["string"],
    "health_conditions": ["string"]
  }
}
```

**Output:**
- Returns validated input object
- Throws `SafetyConcernError` if medical disclaimer needed
- Throws `InsufficientInfoError` if more information needed

**Implementation:**
```python
def before_program_generation(input):
    # Validate required fields
    if not input.get('experience_level'):
        raise InsufficientInfoError("Experience level not classified")
    
    # Check for medical concerns
    if input.get('health_conditions'):
        return add_medical_disclaimer(input)
    
    # Validate constraints
    validate_training_constraints(input)
    
    return input
```

---

**`before_tool_execution(tool_name, tool_input)`**

Executes before any tool is invoked.

**Purpose:**
- Validate tool input against schema
- Check tool availability
- Log tool usage for monitoring

**Parameters:**
- `tool_name`: Name of tool to be executed
- `tool_input`: Input parameters for the tool

**Output:**
- Returns validated tool input
- Throws `ValidationError` if input doesn't match schema
- Throws `ToolUnavailableError` if tool cannot be executed

---

### 2. Post-Processing Hooks

**`after_program_generation(program)`**

Executes after program generation is complete.

**Purpose:**
- Validate program against safety standards
- Apply consistent formatting
- Add required disclaimers
- Check for completeness

**Input:** Generated program object

**Output:** Finalized program ready for output

**Validation Checklist:**
- [ ] Disclaimer included and prominent
- [ ] Experience level appropriate complexity
- [ ] Progressive overload clearly defined
- [ ] Rest and recovery explicitly scheduled
- [ ] Deload weeks included if applicable
- [ ] Safety warning signs listed
- [ ] Exercise instructions include form cues
- [ ] Progression criteria are objective

**Implementation:**
```python
def after_program_generation(program):
    # Run validation checklist
    validation_results = validate_program(program)
    
    if not validation_results.passed:
        # Add missing elements
        program = add_missing_elements(program, validation_results.missing)
    
    # Apply consistent formatting
    program = format_program(program)
    
    # Add safety disclaimers
    program = add_disclaimers(program)
    
    return program
```

---

**`after_tool_execution(tool_name, result)`**

Executes after tool execution completes.

**Purpose:**
- Validate tool output
- Log results
- Handle errors gracefully

**Parameters:**
- `tool_name`: Name of tool that was executed
- `result`: Result returned by tool

**Output:** Processed result or error fallback

---

### 3. Error Handling Hooks

**`on_error(error, context)`**

Executes when an error occurs during skill execution.

**Purpose:**
- Provide graceful fallback
- Communicate error clearly to user
- Suggest alternative approaches
- Log error for monitoring

**Error Levels:**

**Level 1: User Input Issues**
- Insufficient information
- Contradictory goals
- Missing required fields

**Response:** Ask clarifying questions, present tradeoffs

**Level 2: System Issues**
- Reference file unavailable
- Tool execution failure
- Validation failure

**Response:** Use general knowledge, provide manual guidance

**Level 3: Critical Issues**
- Unable to provide safe guidance
- Out of scope request
- Medical concerns

**Response:** Full disclaimer, recommend professional

**Implementation:**
```python
def on_error(error, context):
    error_level = classify_error(error)
    
    if error_level == 1:
        return handle_input_error(error, context)
    elif error_level == 2:
        return handle_system_error(error, context)
    elif error_level == 3:
        return handle_critical_error(error, context)
    else:
        return handle_unknown_error(error, context)
```

---

### 4. Event Hooks

**`on_progress_update(progress_data)`**

Executed when significant progress milestones are reached.

**Purpose:**
- Emit progress events for monitoring
- Update internal state
- Trigger dependent actions

**Progress Data:**
```json
{
  "stage": "string",
  "percent_complete": 0-100,
  "current_component": "string",
  "estimated_remaining": "string"
}
```

---

**`on_state_change(old_state, new_state)`**

Executed when internal state changes.

**Purpose:**
- Synchronize state across components
- Emit state change events
- Update session context

**State Transitions:**
- IDLE → ANALYZING
- ANALYZING → DESIGNING
- DESIGNING → VALIDATING
- VALIDATING → OUTPUT
- Any state → ERROR

---

## Hook Registration

Hooks are registered in the hooks registry:

```python
HOOKS_REGISTRY = {
    'before_program_generation': before_program_generation,
    'after_program_generation': after_program_generation,
    'before_tool_execution': before_tool_execution,
    'after_tool_execution': after_tool_execution,
    'on_error': on_error,
    'on_progress_update': on_progress_update,
    'on_state_change': on_state_change
}
```

## Hook Execution Flow

```
User Request
    ↓
before_program_generation (validate input)
    ↓
[Component Selection & Routing]
    ↓
before_tool_execution (for each tool)
    ↓
Tool Execution
    ↓
after_tool_execution (for each tool)
    ↓
after_program_generation (validate output)
    ↓
Final Output
```

If error occurs at any stage → `on_error` hook

## State Management

### State Schema

```json
{
  "current_state": "IDLE|ANALYZING|DESIGNING|VALIDATING|OUTPUT|ERROR",
  "user_session": {
    "session_id": "string",
    "start_time": "timestamp",
    "user_profile": {
      "experience_level": "string",
      "training_goals": ["string"],
      "constraints": {}
    }
  },
  "program_context": {
    "current_program": {},
    "iteration_count": 0,
    "validation_results": {}
  },
  "execution_log": [
    {
      "timestamp": "timestamp",
      "event": "string",
      "details": {}
    }
  ]
}
```

### State Transitions

Valid state transitions:
- IDLE → ANALYZING (request received)
- ANALYZING → DESIGNING (input validated)
- DESIGNING → VALIDATING (program drafted)
- VALIDATING → OUTPUT (validation passed)
- VALIDATING → DESIGNING (validation failed, iterating)
- Any → ERROR (error occurred)
- ERROR → IDLE (error resolved)

## Event Emission

Events are emitted for:
- State changes
- Progress updates
- Tool invocations
- Validation results
- Errors

**Event Schema:**
```json
{
  "event_type": "state_change|progress|tool_invocation|validation|error",
  "timestamp": "timestamp",
  "event_data": {},
  "session_context": {}
}
```

## Monitoring & Logging

All hooks emit events that can be captured for monitoring and logging.

**Log Levels:**
- DEBUG: Detailed execution information
- INFO: Normal execution milestones
- WARN: Warning conditions that don't stop execution
- ERROR: Error conditions

**Logging Strategy:**
- Structured logging with JSON format
- Include session_id for correlation
- Log all hook invocations
- Log all tool executions
- Log all state transitions

## Error Recovery

### Automatic Recovery

Certain errors trigger automatic recovery:

**Tool Execution Failure**
1. Log error
2. Attempt alternative calculation method
3. If successful, continue with fallback result
4. If failed, throw error to user

**Validation Failure**
1. Log validation errors
2. Attempt to add missing elements
3. Re-validate
4. If failed, throw error to user

### Manual Recovery

For errors requiring user intervention:
1. Present error clearly
2. Explain what went wrong
3. Suggest resolution options
4. Wait for user response

## Hook Configuration

Hooks can be configured via environment variables or config files:

```yaml
hooks:
  before_program_generation:
    enabled: true
    strict_validation: true
  after_program_generation:
    enabled: true
    validation_level: strict
  on_error:
    enabled: true
    fallback_enabled: true
    verbose_errors: false
```

---

**Version:** 1.0.0
**Last Updated:** 2026-08-04
