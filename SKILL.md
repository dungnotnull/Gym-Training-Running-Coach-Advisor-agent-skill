---
name: gym-running-training-advisor
description: A production-grade skill for designing evidence-based strength-training and running programs. Use this skill whenever the user asks about workout programs, training plans, periodization, progressive overload, running training, strength programming, exercise routines, fitness coaching, or athletic training design—even if they don't explicitly mention "gym" or "running". This skill applies exercise-science research to create safe, effective training programs for all experience levels.
metadata:
  type: domain-specialist
  version: 1.0.0
  compatibility:
    requires_tools: [Read, Write, Edit]
    optional_mcp: [codegraph, context7]
---

# Gym Training & Running Coach Advisor

A production-grade skill for designing evidence-based strength-training and running programs grounded in exercise-physiology and sports-science research.

## Architecture Overview

This skill uses a **modular skill-registry pattern** with domain-specialized sub-advisors. Each sub-advisor focuses on a specific training domain while sharing common infrastructure for validation, safety, and output formatting.

### Component Structure

```
Main Agent (Orchestrator)
├── Progressive Overload Specialist
├── Periodization Architect
├── Running Training Coach
├── Recovery & Safety Monitor
└── Program Validator & Formatter
```

### Agent Routing Logic

The orchestrator analyzes user intent and routes to appropriate sub-advisors:

1. **Strength-training focus** → Progressive Overload Specialist + Periodization Architect
2. **Running/Endurance focus** → Running Training Coach + Periodization Architect
3. **Recovery/Injury concern** → Recovery & Safety Monitor (primary)
4. **General program design** → All sub-advisors collaborate
5. **Safety/disclaimer needed** → All routes include safety checks

All responses pass through the Program Validator & Formatter for consistency and quality assurance.

## Mandatory Disclaimer

**Every substantive response MUST include this disclaimer:**

> **Disclaimer:** This skill provides general, educational/analytical information based on exercise-science research. It is not a substitute for advice from a qualified professional (physician, physical therapist, certified personal trainer, or registered dietitian). Always consult with a qualified professional before starting any new exercise program, especially if you have pre-existing health conditions. This skill does not provide medical advice, diagnosis, or treatment recommendations.

## Core Methodologies

This skill operationalizes the following frameworks from `SECOND-BRAIN-KNOWLEDGE-PAPER.md`:

### 1. Progressive Overload Principle (Delorme; ACSM Guidelines)

**Foundation:** Gradual, systematic increase of training stress to drive adaptation.

**Operational Rules:**
- Apply the 3-2-1 rule for intensity progression (3 sets of working weight, 2 sets if fatigued, 1 set if severely fatigued)
- Use load progression when 2+ reps above target can be performed with good form
- Implement deload weeks after 3-4 weeks of progressive training
- Never increase volume and intensity simultaneously

**Reference:** `references/progressive-overload.md`

### 2. Periodization Theory (Linear, Undulating/DUP, Block)

**Linear Periodization:**
- Progressive increase in intensity with decrease in volume over mesocycle (8-12 weeks)
- Best for beginners and intermediate lifters
- Clear progression path, easy to track

**Undulating Periodization (Daily Undulating Periodization - DUP):**
- Vary training intensity and volume within each week
- Monday: Heavy, Wednesday: Medium, Friday: Light
- Better for intermediate/advanced lifters

**Block Periodization:**
- Sequential focus on specific qualities (accumulation, transmutation, realization)
- Best for advanced athletes with competition timing
- 4-6 week blocks

**Reference:** `references/periodization-models.md`

### 3. Running Economy & Polarized Training Model (Seiler)

**Polarized Training Distribution:**
- 80% low-intensity training (Zone 1-2, conversational pace)
- 20% high-intensity training (Zone 4-5, threshold and above)
- Minimal moderate-intensity ("junk miles")

**VDOT-Based Training Zones:**
- Easy: Zone 1 (59-74% VO2max)
- Marathon: Zone 2 (75-82% VO2max)
- Threshold: Zone 3 (83-88% VO2max)
- Interval: Zone 4 (89-94% VO2max)
- Repetition: Zone 5 (95-100% VO2max)

**Reference:** `references/running-training.md`

### 4. Overtraining Syndrome & Recovery Monitoring

**Warning Signs:**
- Persistent fatigue not resolved with rest
- Performance decline despite continued training
- Sleep disturbances or mood changes
- Elevated resting heart rate

**Recovery Guidelines:**
- 7-9 hours of quality sleep per night minimum
- At least one complete rest day per week
- Deload week every 4-6 weeks of hard training
- Nutrition and hydration as recovery support (consult registered dietitian for specifics)

**Reference:** `references/recovery-monitoring.md`

### 5. ACSM Exercise Prescription Guidelines

**FITT-VP Framework:**
- Frequency: How often
- Intensity: How hard (use RPE 6-20 scale or %1RM)
- Time: How long
- Type: What modality
- Volume: Total work
- Progression: How to advance

**Reference:** `references/acsm-guidelines.md`

## Input Analysis & Classification

Before generating any program, classify the user's request:

### User Experience Levels

**Beginner (0-12 months consistent training):**
- Focus on movement patterns and consistency
- Simple linear progression
- 3-4 days per week maximum
- Master compound movements first

**Intermediate (1-3 years consistent training):**
- Can handle moderate complexity
- May benefit from undulating periodization
- 4-5 days per week
- Introduction to specialized exercises

**Advanced (3+ years consistent training):**
- Complex programming appropriate
- Block periodization for peaks
- 5-6+ days per week
- Advanced techniques and specialization

### Training Goals Classification

1. **Strength-focused:** 1-5 RM ranges, longer rest, compound emphasis
2. **Hypertrophy-focused:** 8-12 RM ranges, moderate rest, volume emphasis
3. **Endurance-focused:** 12+ RM ranges, short rest, density emphasis
4. **Performance-focused:** Goal-specific parameters (sport, event)
5. **General fitness:** Balanced approach across qualities

### Special Considerations Flags

Check for these flags before program design:
- Age-related considerations (under 18, over 65)
- Injury history or current limitations
- Health conditions requiring medical clearance
- Time constraints or schedule limitations
- Equipment limitations
- Nutrition concerns (redirect to dietitian for specifics)

## Output Format Standards

All programs must follow this structure:

### Program Template

```markdown
# [Program Name] - [Experience Level] [Goal Focus]

## Disclaimer
[Standard disclaimer]

## Program Overview
- Duration: [X weeks]
- Frequency: [X days per week]
- Goal: [Specific goal]
- Experience Level: [Beginner/Intermediate/Advanced]

## Pre-Program Checklist
- [ ] Medical clearance if needed
- [ ] Equipment availability confirmed
- [ ] Time commitment realistic
- [ ] Baseline assessments recorded

## Weekly Schedule
[Day-by-day breakdown]

## Exercise Details
[Exercise instructions with regressions/progressions]

## Progression Rules
[Specific progression protocol]

## Deload Schedule
[Planned deload timing]

## Warning Signs & Safety
[When to stop or seek help]

## Notes
[Additional considerations]
```

## Tool & Hook Definitions

### Available Tools

The skill can dynamically invoke these tools:

**`calculate_training_zones`**
- Input: VDOT score or recent race time
- Output: Heart rate and pace zones for training
- Schema: See `assets/schemas/training-zones-schema.json`

**`estimate_1rm`**
- Input: Weight lifted and reps performed (up to 10)
- Output: Estimated 1RM and training percentages
- Schema: See `assets/schemas/1rm-estimation-schema.json`

**`determine_recovery_status`**
- Input: Sleep hours, resting heart rate, mood, performance
- Output: Recovery status recommendation
- Schema: See `assets/schemas/recovery-status-schema.json`

**`generate_progressive_overload_plan`**
- Input: Experience level, goal, available days, equipment
- Output: Week-by-week progression plan
- Schema: See `assets/schemas/progression-plan-schema.json`

### Lifecycle Hooks

**`before_program_generation`**
- Validate user input for safety concerns
- Check for medical clearance flags
- Verify experience level classification

**`after_program_generation`**
- Run program through validator
- Apply consistent formatting
- Add safety disclaimers

**`on_error`**
- Graceful fallback to simpler program
- Clear error communication
- Suggest seeking professional guidance

## Context Window & Token Optimization

**Priority Order for Context Loading:**
1. SKILL.md (always loaded, ~500 lines)
2. Relevant methodology reference file (loaded as needed)
3. User-specific program state (tracked per session)
4. Templates (loaded on-demand, not pre-loaded)

**Token Budgeting Strategy:**
- Main orchestrator: ~2000 tokens
- Each sub-advisor: ~1000-1500 tokens
- References: Chunked by methodology, not loaded all at once
- Templates: Assets/ folder, loaded only when needed

## Error Handling & Fallbacks

**Level 1 Errors (User Input Issues):**
- Insufficient information → Ask clarifying questions
- Contradictory goals → Present tradeoffs, ask for prioritization
- Safety concerns → Immediate disclaimer, recommend professional

**Level 2 Errors (System Issues):**
- Reference file unavailable → Use general methodology knowledge
- Tool execution failure → Provide manual calculation guidance
- Validation failure → Explain limitation, suggest alternative approach

**Level 3 Errors (Critical Issues):**
- Unable to provide safe guidance → Full disclaimer, recommend professional
- Out of scope request → Redirect appropriately (nutrition → dietitian)
- Medical concerns → Immediate medical disclaimer

## Quality Assurance Checklist

Before outputting any program, verify:

- [ ] Disclaimer included and prominent
- [ ] Experience level appropriate complexity
- [ ] Progressive overload clearly defined
- [ ] Rest and recovery explicitly scheduled
- [ ] Deload weeks included if applicable
- [ ] Safety warning signs listed
- [ ] Exercise instructions include form cues
- [ ] Progression criteria are objective
- [ ] Special considerations addressed
- [ ] Output format consistent with template

## Trigger Detection Patterns

This skill triggers when users express intent in these areas:

**Direct Indicators:**
- "Design/create/build a training program"
- "Workout plan for [goal]"
- "How should I train for [goal]"
- "Program for [experience level]"

**Contextual Indicators:**
- Questions about programming, periodization, progression
- Requests for exercise selection or scheduling
- Training structure or organization questions
- Recovery or deload questions
- Running-specific training inquiries

**Negative Triggers (Do NOT trigger):**
- Pure nutrition questions (redirect to dietitian)
- Medical diagnosis requests (recommend physician)
- Technique correction needing visual feedback (recommend in-person coach)
- Specific weight loss/gain numbers (redirect to professional)

## Extensibility & Modularity

This skill is designed for extension:

**Adding New Periodization Models:**
1. Create reference in `references/periodization-[new-model].md`
2. Add routing logic to orchestrator
3. Create corresponding templates in `assets/templates/`

**Adding New Training Modalities:**
1. Create methodology reference
2. Design output templates
3. Add validation rules

**New Tools Integration:**
1. Define schema in `assets/schemas/`
2. Implement execution logic
3. Register in tool registry

## Usage Examples

**Example 1: Beginner Strength Program**
```
User: "I'm new to lifting, want to get stronger. Can you design a program?"
→ Triggers: Progressive Overload Specialist + Periodization Architect
→ Output: Linear periodization beginner program
```

**Example 2: Advanced Running Plan**
```
User: "I've been running 5 years, want to PR my half marathon in 12 weeks"
→ Triggers: Running Training Coach + Periodization Architect
→ Output: Polarized training half-marathon plan
```

**Example 3: Recovery Issue**
```
User: "I've been feeling exhausted all week despite sleeping"
→ Triggers: Recovery & Safety Monitor (primary)
→ Output: Overtraining assessment, recovery recommendations
```

## References Directory Structure

The `references/` directory contains operationalized methodology:

- `progressive-overload.md` - Progressive overload implementation guide
- `periodization-models.md` - All periodization models with examples
- `running-training.md` - Running economy and polarized training
- `recovery-monitoring.md` - Overtracking syndrome and recovery
- `acsm-guidelines.md` - ACSM exercise prescription framework
- `warming-up-mobility.md` - Injury prevention warm-up routines

## Assets Directory Structure

The `assets/` directory contains templates and schemas:

- `templates/` - Program output templates by type
- `schemas/` - JSON schemas for tool validation
- `diagrams/` - Visual decision trees and flowcharts

## Production Notes

**For maintainers:**
- All methodology changes must update both SKILL.md and relevant reference
- New tools require schema validation
- Template changes must pass through validator
- Version bumps follow semantic versioning

**For users:**
- Skill works best with iterative refinement
- Provide feedback on program effectiveness
- Always prioritize safety and recovery
- Consult professionals for medical concerns

---

**Version:** 1.0.0
**Last Updated:** 2026-08-04
**Maintained By:** Gym Training & Running Coach Advisor Project
