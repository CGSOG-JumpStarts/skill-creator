# skill-creator

Create new skills, modify and improve existing skills, and measure skill performance.

This skill is used when users want to:
- create a skill from scratch,
- edit or optimize an existing skill,
- run evals to test a skill,
- benchmark skill performance with variance analysis,
- improve a skill description for better triggering accuracy.

---

## Overview

`skill-creator` supports the full skill lifecycle:

1. **Design** a new skill from intent to implementation.
2. **Refine** existing skills for better behavior and reliability.
3. **Evaluate** using repeatable tests and scoring.
4. **Benchmark** outcomes and analyze variance across runs.
5. **Optimize triggering** by improving descriptions and routing cues.

---

## Core Capabilities

- **Skill Creation**
  - Define purpose, inputs, outputs, and constraints.
  - Generate initial skill structure and implementation guidance.

- **Skill Editing & Optimization**
  - Improve quality, clarity, and consistency of outputs.
  - Tighten instructions and guardrails.
  - Reduce failure modes and ambiguous behavior.

- **Evaluation (Evals)**
  - Run test scenarios against a skill.
  - Measure success criteria across representative prompts.
  - Track regressions after changes.

- **Performance Benchmarking**
  - Compare versions of a skill over the same eval set.
  - Quantify deltas in quality and reliability.
  - Perform variance analysis for stability across repeated runs.

- **Triggering Accuracy Improvements**
  - Refine skill descriptions for better selection/routing.
  - Improve discoverability through clearer scope definitions.
  - Reduce overlap and unintended triggering with neighboring skills.

---

## When to Use This Skill

Use `skill-creator` when you need to:

- launch a brand-new skill quickly with clear requirements,
- diagnose underperforming skill behavior,
- run structured experiments before shipping changes,
- compare versions to pick the most stable implementation,
- increase trigger precision by rewriting skill descriptions.

---

## Suggested Workflow

1. **Define goal**
   - What user problem should this skill solve?
   - What does success look like?

2. **Create or update skill**
   - Draft or revise instructions, examples, and constraints.

3. **Build eval set**
   - Include happy paths, edge cases, and adversarial cases.

4. **Run benchmarks**
   - Execute multiple runs to capture variance.

5. **Analyze results**
   - Identify quality gaps, inconsistency, and routing errors.

6. **Iterate**
   - Apply focused improvements and re-run evals.

---

## Example Use Cases

- Create a new internal support skill for triaging requests.
- Improve an existing writing skill that is too verbose or inconsistent.
- Benchmark two prompt strategies to select the more robust version.
- Rewrite a skill description to reduce false-positive triggering.

---

## Inputs & Outputs (Typical)

### Inputs
- Skill objective and scope
- Existing skill configuration/instructions (if any)
- Evaluation dataset or test prompts
- Success metrics (e.g., accuracy, consistency, adherence)

### Outputs
- New or updated skill definition
- Recommended instruction changes
- Eval results summary
- Benchmark comparison and variance notes
- Trigger-description optimization suggestions

---

## Best Practices

- Keep skill scope narrow and explicit.
- Encode non-negotiable constraints clearly.
- Evaluate before and after every meaningful change.
- Use repeated runs to distinguish real gains from noise.
- Prefer measurable improvements over subjective edits.
- Continuously refine skill descriptions to improve routing precision.

---
