# AI Contributor Instructions

This file defines engineering standards for AI-assisted changes in this repository.

## Scope and Role
- Applies to AI coding assistants across local tools, CI automation, and hosted coding agents.
- Complements `AGENTS.md` (operational contract) and runtime-specific files.

## Recommended Documentation Structure
Use a layered model:
1. **Operational contract**: `AGENTS.md` (what every agent must do).
2. **Engineering standards**: this file (how changes should be implemented).
3. **Runtime adapters**:
   - `.github/copilot-instructions.md` for Copilot-specific behavior.
   - `.github/agents/README.md` for hosted-agent profile layout.
4. **Specialized extension policy**: `SKILLS.md` for future repo-local skills.

## Core Principles
- **Safety first:** preserve educational intent; avoid certainty language in financial contexts.
- **Small, reviewable diffs:** prefer scoped changes.
- **Test-backed changes:** behavior updates require validation.
- **Determinism:** avoid flaky and network-dependent tests when possible.
- **Transparency:** state assumptions, limits, and trade-offs.

## Engineering Standards
### Design
- Keep indicator calculations and strategy decisions separated.
- Keep data-fetch/IO boundaries explicit.
- Preserve backward-compatible CLI behavior unless requested otherwise.

### Implementation
- Follow PEP 8.
- Prefer clear naming and small focused functions.
- Catch specific exceptions and return actionable failure context.
- Avoid introducing global mutable state.

### Security and Compliance
- Never commit secrets, credentials, or private keys.
- Keep dependency additions minimal and justified.
- Do not add unrelated telemetry or external calls.

## Validation Expectations
- Run tests before finalizing (`PYTHONPATH=. pytest -q`).
- Add/update tests for behavior changes under `tests/`.
- Prefer behavior assertions over implementation-coupled assertions.

## Documentation Expectations
- Update `README.md` when setup/behavior/output changes.
- Keep docs concise; link to canonical files instead of duplicating policy text.

## PR Expectations
Include:
- what changed,
- why it changed,
- validation commands and outcomes,
- limitations/risks.

## AI Output Quality Checklist
- [ ] Scope fully addressed.
- [ ] No unrelated refactors.
- [ ] Tests passed.
- [ ] Documentation updated as needed.
- [ ] No sensitive data introduced.
- [ ] Assumptions/limitations called out.


## Research Traceability
- See `docs/ai/RESEARCH_NOTES.md` for external guidance summarized for this structure.
