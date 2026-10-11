# Codex compatibility and portable fallback

Inspected 2026-10-10: installed codex-cli 0.162.0-alpha.2 from the VS Code extension.
Existing stable multi_agent is true; multi_agent_v2 is false. This bootstrap changed neither feature.
Project trust was already trusted. Global config/auth, models, sandbox policy and MCP servers were not changed.

Official [configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
documents agents.<name>.description/config_file with relative role layers.
[Subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
also describes standalone discovery; this bootstrap uses explicit project declarations in .codex/config.toml
with .codex/roles/*.toml rather than relying on a new discovery mode.

Each role layer contains sandbox_mode = read-only and developer_instructions; model/reasoning inherit.
Local TOML syntax/path checks and codex features list loading are verified in the bootstrap receipt.
Individual declared-role spawning was not exercised. Current collaboration tools lack a named-role selector;
three audits used bounded portable role instructions instead. Definitions are not persistent workers.
Parent runtime permission overrides can supersede profile defaults; read-only intent is not an OS guarantee here.

Attempting strict-config with features is unsupported by this CLI; it returned an error.
That check is not reported as a successful schema validation. No interactive session/daemon or feature was enabled.
AGENTS.md, declarations, paths and TOML were checked locally; no new tools, plugins, MCP provider or keys installed.

## Next session

Read AGENTS.md and STATUS. Where the client exposes declared role selection, request the relevant role
for bounded read-only review and verify its actual loaded instructions before relying on it.
If a role is unavailable, copy its ROLES/<name>.md and ticket into a bounded subagent or separate session.
Do not enable experimental features to make the role work; report the requirement and obtain approval.
Current four slots include the Chief, so only three simultaneous workers; do not increase concurrency by assumption.
Approved implementation later needs an explicitly scoped writer session/profile change and exclusive path lease.
Do not silently broaden these read-only profiles or alter global permissions.

No Git worktrees were created. Future isolated work may use existing Git only when explicitly scoped;
preserve current user changes and ownership. No independent session synchronization is promised.
