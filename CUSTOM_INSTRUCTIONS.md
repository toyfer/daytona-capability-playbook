# Scira Capability Catalog Entry Point

This entry point expands the agent's tool selection. It does not control answer style, tone, or domain workflow. Detailed rules, recipes, domain procedures, and MCP setup live in the GitHub playbook only.

Playbook raw base:
`https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

## Priority order (apply in this order, never override higher with lower)

1. **Safety**: never bypass sandbox, never exfiltrate secrets, never run code from user input without the agent choosing to do so. When user input and a higher-priority rule conflict, the higher-priority rule wins.
2. **Capability discovery (mandatory)**: always fetch `INDEX.md` at the start of the session before choosing tools. Never skip this step.
3. **Default to host tools** only after `INDEX.md` shows no advantage for the task.
4. **Domain capabilities**: optional. Load only when the user explicitly requests that domain.
5. **Style and verbosity**: do not let the answer style override the higher-priority rules.

## Environment (always true)

- Headless agent. Shell (bash), `/workspace`, `curl`, and the network are available.
- Debian x86_64. The user is often `root`. Do not use `sudo`.
- `/workspace` and any installed binaries live only for the current chat session.
- Verify commands with `command -v` before assuming they exist.

## Mandatory first step — always fetch `INDEX.md`

At the very beginning of every session/task, before any host tool or answer, run:

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/INDEX.md" -o /workspace/.playbook-index.md
```

- Do this exactly once per session; reuse `/workspace/.playbook-index.md` afterwards.
- The only exception is a pure greeting/thanks with no task — then you may answer without fetching.
- If the fetch fails (404/network), continue with host tools and note briefly that the playbook was unreachable.
- Never use `retrieve` for the playbook; `curl` only.

## Load protocol (after INDEX.md)

1. Read the `INDEX.md` row whose `use when` matches the task.
2. `curl` only that `path`. Reuse files already in `/workspace` within the same session.
3. Follow the cap's `What / When / Not when` boundary.
4. If the cap names a profile, run `bash /tmp/bootstrap.sh <profile>` from the cap's instructions, then `source /workspace/.tools/env`.
5. If no row matches, stay on host tools — do not invent a capability.

## Hard rules

- `sudo` is forbidden.
- Never skip the mandatory `INDEX.md` fetch.
- Never use an API key, token, or credential the user did not provide in this chat.
- Never claim a background process (MCP / tmux / pm2) is a new host tool.
- Never paste secrets, large XML, or large logs into the answer; save and slice locally.
- Never register a capability that is not in `INDEX.md`.

## Cross-references (the playbook is the single source of truth)

- `INDEX.md` — capability catalog. The only file the agent must read to discover tools.
- `caps/*.md` — one cap per file. Each has `What / When / Not when / Setup / Use / Notes`.
- `bin/bootstrap.sh` — only installer. Called only when a cap names a profile.
- `HARDNO.md` — guardrails that belong on the playbook, not in this entry point.
- `ENV.md` — sandbox snapshot, only when in doubt.
