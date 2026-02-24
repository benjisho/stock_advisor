# AI/Agent Instruction Structure Research Notes

This note captures external guidance used to restructure repository AI/agent instruction files.

## Sources Reviewed
- GitHub Docs: **Adding repository instructions for GitHub Copilot**
- GitHub Docs: **Support for different types of custom instructions**
- GitHub Docs: **Using custom instructions to improve Copilot outcomes**
- GitHub Docs: **Best practices for Copilot coding agent task execution**

## Key Takeaways Applied
1. Keep Copilot instructions concise and high-signal.
2. Use a layered policy model to avoid duplication and conflicts.
3. Put operational rules in one canonical file and reference from runtime-specific files.
4. Define explicit validation commands to improve reproducibility.
5. Prefer role/profile docs with a fixed section template for hosted agents.

## Structure Adopted in This Repo
- Canonical operational policy: `AGENTS.md`
- Cross-runtime engineering policy: `AI_INSTRUCTIONS.md`
- Copilot adapter: `.github/copilot-instructions.md`
- Hosted agent profile index: `.github/agents/README.md`
- Skill extension policy: `SKILLS.md`

## Maintenance Rules
- Update canonical policy first (`AGENTS.md`) when constraints change.
- Update adapters next (`.github/*`, `SKILLS.md`) to stay aligned.
- Keep runtime-specific files short and reference canonical docs.
