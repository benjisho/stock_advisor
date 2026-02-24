# AGENTS.md

Guidance for autonomous coding agents working in this repository.

## Scope
This file applies to the entire repository tree rooted at this directory.

## Mission
Maintain a reliable, educational stock-advisor codebase with clear strategy logic,
robust data-source handling, and dependable tests.

## Instruction Hierarchy (Apply in this order)
1. Direct user/developer/system instructions for the current task.
2. This `AGENTS.md` (repo-wide operational contract).
3. Runtime-specific files (for example, `.github/copilot-instructions.md`).
4. Supplemental guidance (`AI_INSTRUCTIONS.md`, `SKILLS.md`, `.github/agents/*`).

If guidance conflicts, follow the highest-priority item and call out the conflict in your summary.

## Working Agreement
1. Make the smallest safe change that solves the requested task.
2. Keep strategy/indicator behavior explicit and testable.
3. Prefer readability over cleverness.
4. Do not perform unrelated cleanup unless requested.

## Project Map
- `main.py`: application entry point and data-source orchestration.
- `indicators/`: technical indicator calculations.
- `strategy/`: recommendation logic.
- `tests/`: behavior and regression tests.

## Implementation Rules
### Code Quality
- Follow PEP 8 and keep functions focused.
- Add comments/docstrings only where they increase clarity.
- Keep imports clean and remove dead code.

### Data and Trading Logic
- Preserve current data-source fallback behavior unless task requires changes.
- Keep recommendations grounded in available indicator values.
- Defensively handle empty/invalid data frames before calculations.

### Dependency Policy
- Avoid introducing new dependencies unless clearly necessary.
- If adding a dependency, update `requirements.txt` and justify it in the PR.

### Testing Policy
- Run test suite for every code change.
- Add or update tests whenever behavior changes.
- Prefer deterministic tests; avoid network dependence in tests.

### Documentation Policy
- Update `README.md` if setup, behavior, or outputs change.
- Keep docs concise and actionable.

## Git and PR Standards
- Use descriptive commit messages in imperative mood.
- Include a PR summary with:
  - change overview,
  - rationale,
  - validation commands/results,
  - known limitations.

## Safety and Compliance
- Never commit secrets or credentials.
- Treat output as educational, not financial advice.
- Avoid claims of guaranteed investment outcomes.

## Companion AI/Agent Files
- `AI_INSTRUCTIONS.md`: cross-runtime AI engineering standards.
- `.github/copilot-instructions.md`: GitHub Copilot/Copilot Chat behavior.
- `.github/agents/README.md`: hosted-agent profile conventions.
- `SKILLS.md`: conventions for introducing repository-local skills.
- `docs/ai/RESEARCH_NOTES.md`: rationale and external guidance used for structure decisions.

## Done Criteria
A task is complete when:
- Requested changes are implemented,
- tests pass,
- documentation is updated if needed,
- diff is minimal and reviewable.
