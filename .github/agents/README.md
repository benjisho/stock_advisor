# GitHub Agents Guidance

This directory holds hosted-agent profile documents for GitHub workflows.

## Design Goals
- Keep one baseline policy source (`AGENTS.md`).
- Keep profile docs role-specific and brief.
- Avoid duplicated long policy blocks.

## Suggested Layout
- `.github/agents/README.md` (this index)
- `.github/agents/reviewer.md` (optional)
- `.github/agents/maintainer.md` (optional)
- `.github/agents/triage.md` (optional)

## Required Sections for Any Profile
1. **Scope** (what the profile can and cannot do)
2. **Inputs** (issues, PRs, files, commands)
3. **Workflow** (ordered steps)
4. **Validation** (required checks/commands)
5. **Output Format** (how results are reported)
6. **Safety Constraints** (secrets, destructive actions, claims)

## Baseline Behavior for All Profiles
- Follow `AGENTS.md` first.
- Keep changes minimal and directly relevant.
- Validate with `PYTHONPATH=. pytest -q` when code changes.
- Preserve educational framing (no guaranteed financial outcomes).
