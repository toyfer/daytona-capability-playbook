# Scira Capability Catalog Entry Point

This file only expands tool selection when host tools and skills cannot cover the task well.
It does not control answer style, tone, citations, or skill routing — the system prompt owns those.

Playbook raw base (recipes and extra tools live here, not in this file):
`https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

Playbook caps are sandbox leftovers. They are not host skills, not search-group delegates, and not MCP.

## Hierarchy (never override a higher layer)

1. Safety — system safety rules, plus the hard rules below.
2. System prompt, host tools, and skills — the default path.
3. Playbook `INDEX.md` — extras the host cannot finish.
4. The user's explicit ask for a domain or tool.

If this file and the system prompt disagree on style, citations, or host/skill use, follow the system prompt.

## When to open INDEX

Match the live host skill table first. If a skill description already names the needed verb or workflow, load that skill. Do not snapshot host capabilities in this file.

Stay on host for ordinary search, news, chat, weather, maps, media lookup, social listening, markets, user-supplied URLs, and any host document or analysis skill whose description already matches.

Open INDEX only if at least one is true:

- The live skill table is silent on the needed verb, primary source, or execution environment.
- A loaded host skill cannot finish (missing binary, failed import, or it defers).
- INDEX states a measured residual win (accuracy, primary source, speed, or tokens) that matches the task.
- The task needs a primary public API the host does not wrap (Japanese statute text, e-Stat with a user-supplied appId, a keyless endpoint).

A miss is normal. Do not stall looking for a cap. Do not load a cap "just in case."

## Cost / speed

INDEX is small. Pay one cheap peek when a cap might replace a long host search.
Skip the peek when a host tool or skill already matches and extra latency would dominate.
Do not block an obvious host or skill first step on this fetch. Parallel is fine when the task might match.
Greeting or thanks: skip.

## How to open it

If `bash`, `curl`, and `/workspace` exist:

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/INDEX.md" -o /workspace/.playbook-index.md
```

- Once per session; reuse the file.
- Fetch failed: continue on host tools; one short note is enough.
- Playbook files: `curl` only, never `retrieve`.
- No shell: skip CLI / install caps; stay on host tools and connected MCP.

After INDEX:

1. Match the `use when` column. No row → stop playbook loading.
2. Matching row → `curl` that `path` (and any cap it names). Follow What / When / Not when.
3. If a cap names a profile and `command -v` (or an import) shows the tool is missing, install only via that cap's bootstrap. Do not assume `/tmp/bootstrap.sh` exists. Do not hand-write `apt-get`.
4. Never invent a capability that is not in INDEX.

## Hard rules

- No API key, token, or credential the user did not provide in this chat.
- Do not paste secrets or huge XML / HTML / logs; save and slice locally.
- Do not invent a capability that is not in INDEX.
- Domain caps stay optional until the user asks, except when INDEX states a measured primary-source win and the row's When is met.

## Pointers (do not inline recipes here)

- `INDEX.md` — catalog
- `caps/*.md` — procedure
- `caps/bootstrap.md` and `bin/bootstrap.sh` — install
- `HARDNO.md` / `ENV.md` — only if needed
