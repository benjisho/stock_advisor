# Repository Skills Policy

This repo currently has no local runtime skills checked in, but this file defines best-practice structure if skills are added.

## Why This Exists
Skills are useful only for repeated, specialized workflows that benefit from a reusable playbook.

## Standard Location
- Place each skill at: `.codex/skills/<skill-name>/SKILL.md`
- Keep assets/scripts within that same skill folder.

## Required Skill Contents
Each skill should include:
1. Trigger conditions (when to use it)
2. Inputs required from the user/context
3. Step-by-step workflow
4. Validation commands
5. Failure handling/fallback path
6. Output contract (what the agent should return)

## Quality and Safety Rules
- Must not conflict with `AGENTS.md` or `AI_INSTRUCTIONS.md`.
- Must avoid secret handling and unsafe destructive actions.
- Should prefer deterministic checks over network-dependent checks.
- Should reuse existing scripts/templates where possible.

## Review Checklist
- [ ] Trigger is specific and non-overlapping.
- [ ] Steps are reproducible.
- [ ] Validation is measurable.
- [ ] Safety constraints are explicit.
- [ ] References and paths are valid.
