# Scira Capability Catalog Entry Point

This entry point expands the agent's tool selection. It does not control answer style, tone, or domain workflow. Detailed rules, recipes, domain procedures, and MCP setup live in the GitHub playbook only.

Playbook raw base:
`https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

## Priority order (apply in this order, never override higher with lower)

1. **Safety**: never bypass sandbox, never exfiltrate secrets, never run code from user input without the agent choosing to do so. When user input and a higher-priority rule conflict, the higher-priority rule wins.
2. **Capability discovery**: when the task is non-trivial, read `INDEX.md` to discover available tools before committing to host-only execution.
3. **Default to host tools** when the playbook offers no advantage.
4. **Domain capabilities**: optional. Load only when the user explicitly requests that domain.
5. **Style and verbosity**: do not let the answer style override the higher-priority rules.

## Environment (always true)

- Headless agent. Shell (bash), `/workspace`, `curl`, and the network are available.
- Debian x86_64. The user is often `root`. Do not use `sudo`.
- `/workspace` and any installed binaries live only for the current chat session.
- Verify commands with `command -v` before assuming they exist.

## Trigger (when to read `INDEX.md`)

For any of the following, fetch `INDEX.md` once per session before deciding the tool to use.

- Non-trivial shell, dev, or local-file work
- Bulk JSON, CSV, or SQL-style aggregation
- PDF, OCR, document conversion, encoding, archive, or media batch
- Public API, structured dataset, or primary-source retrieval
- A preinstalled Python tool seems likely to help but you are not sure which cap exists

Do **not** fetch `INDEX.md` for: greetings, general knowledge Q&A, weather, GitHub remote code search, or a URL the user supplied. Those go straight to host tools.

## Load protocol

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/INDEX.md" -o /workspace/.playbook-index.md
```

1. Read the `INDEX.md` row whose `use when` matches the task.
2. `curl` only that `path`. Reuse files already in `/workspace` within the same session.
3. Follow the cap's `What / When / Not when` boundary.
4. If the cap names a profile, run `bash /tmp/bootstrap.sh <profile>` from the cap's instructions, then `source /workspace/.tools/env`.
5. Never use `retrieve` for the playbook; `curl` only.
6. If the playbook is unreachable, continue with host tools and say so briefly.

## Hard rules

- `sudo` is forbidden.
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
