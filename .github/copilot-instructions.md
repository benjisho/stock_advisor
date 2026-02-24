# GitHub Copilot Instructions (Repository)

This file is optimized for Copilot context: concise, high-signal, and task-oriented.

## Primary References
1. `AGENTS.md` (operational rules and precedence)
2. `AI_INSTRUCTIONS.md` (engineering quality standards)

When conflicts appear, follow `AGENTS.md`.

## Copilot Coding Rules
- Make small, focused edits; avoid broad refactors.
- Preserve data-source fallback behavior unless explicitly asked to change it.
- Keep strategy logic deterministic and easy to review.
- Validate empty/missing data before indicator/strategy calculations.
- Do not introduce new dependencies unless necessary.

## Python Rules
- Follow PEP 8.
- Prefer clear names and single-purpose functions.
- Catch specific exceptions where practical.
- Remove unused imports/code in touched files.

## Testing Rules
- Add/update tests for behavior changes.
- Prefer deterministic tests (mocks/stubs over live network calls).
- Validation command: `PYTHONPATH=. pytest -q`.

## Documentation Rules
- Update `README.md` when user-visible behavior or setup changes.
- Keep generated docs concise and actionable.
