# PROJECT-detail.md — Gym Training & Running Coach Advisor

## 1. Problem Statement

A skill helping gym-goers and runners design safe, effective training programs, grounded in exercise-physiology and sports-science research (progressive overload, periodization, running-economy training). Explicitly disclaims that it is not a substitute for a certified personal trainer, physician clearance before starting a new exercise program, or in-person coaching for technique correction, and avoids providing specific numeric diet/weight-loss targets that could support disordered eating or exercise patterns.

## 2. Target Users

Describe the primary user personas for this skill (fill in based on real usage once built): e.g., students, professionals, hobbyists, or practitioners in the relevant domain.

## 3. Functional Specification

### 3.1 Core Capabilities

- Design progressive-overload strength-training programs appropriate to experience level
- Explain periodization models (linear, undulating, block) for strength and endurance training
- Design running-training plans (base building, tempo work, intervals, taper) grounded in exercise-physiology research
- Explain recovery principles (sleep, deload weeks, overtraining-syndrome warning signs)
- Explain proper warm-up/mobility principles to reduce injury risk
- Recommend consulting a physician before starting a new program, especially for those with health conditions
- Avoid providing specific numeric calorie/weight targets; redirect nutrition-specific questions to a registered dietitian

### 3.2 Key Methodologies & Frameworks Applied

- **Progressive overload principle (Delorme; ACSM guidelines)**
- **Periodization theory (linear, undulating/DUP, block periodization)**
- **Running-economy and polarized-training-model research (Seiler)**
- **Overtraining syndrome / recovery-monitoring research**
- **ACSM (American College of Sports Medicine) exercise-prescription guidelines**

Each framework above should be operationalized as a concrete step, checklist, or template inside the skill's SKILL.md and reference files once this scaffold is turned into a runnable skill (see `DEVELOPMENT-TASK-BY-PHASES.md`).

### 3.3 Expected Input

Typical user requests this skill should handle (fill in with real example prompts during development and testing).

### 3.4 Expected Output Format

Define the structured output format(s) this skill should produce (e.g., structured report, checklist, scored recommendation, memo). Align with the methodologies above so outputs are consistent and auditable.

## 4. Out of Scope / Guardrails

- Always include the standing disclaimer for this domain (see CLAUDE.md).
- Never present output as a certified/professional determination (e.g., not a diagnosis, not a legal opinion, not a guaranteed forecast).
- Where the skill involves a named third party (e.g., a partner, a suspect, a specific person), do not produce a definitive judgment about that individual — stay at the level of general, population-based information and structured reasoning support.
- Flag explicitly when a licensed professional (doctor, lawyer, engineer, certified analyst, etc.) should be consulted.

## 5. Knowledge Base Dependency

This skill's reasoning quality depends on the research foundations catalogued in `SECOND-BRAIN-KNOWLEDGE-PAPER.md`. When building the actual skill (SKILL.md + references/), extract the operational principles from each paper into concrete reference files rather than leaving them as a flat reading list.

## 6. Success Criteria

- Output correctly applies the named methodologies rather than generic reasoning.
- Output is well-structured and consistent across repeated runs on similar inputs.
- Domain-appropriate guardrails/disclaimers are respected in every response.
- Test prompts (see `DEVELOPMENT-TASK-BY-PHASES.md`, Phase 5) produce outputs a subject-matter-competent reviewer would rate as sound.
