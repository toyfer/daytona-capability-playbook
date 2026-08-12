# Scira Capability Catalog Entry Point

This file only expands tool selection when host tools and skills cannot cover the task well.
It does not control answer style, tone, citations, or skill routing — the system prompt owns those.

Playbook raw base (recipes and extra tools live here, not in this file):
`https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

## Hierarchy (never override a higher layer)

1. Safety — system safety rules, plus the hard rules below.
2. System prompt, host tools, and skills — the default path.
3. Playbook `INDEX.md` — extras the host cannot do well.
4. The user's explicit ask for a domain or tool.

If this file and the system prompt disagree on style, citations, or host/skill use, follow the system prompt.

## When to open INDEX

Stay on host tools and skills for ordinary search, news, chat, weather, maps, media lookup, social listening, markets via host tools, user-supplied URLs, and documents the host skills already cover (`docx` `pdf` `xlsx` `pptx` `artifact`).

Open INDEX only when at least one is true:

- The task needs a sandbox CLI or encoding / media / OCR / SQL path the host tools do not provide.
- The task needs a primary public API the host does not wrap (Japanese statute text, e-Stat with a user-supplied appId, keyless geo or open data).
- A host tool would work, but a listed cap is clearly better on accuracy, primary source, speed, or tokens.

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
3. If the cap names a profile and `command -v` (or an import) shows the tool is missing, install only via that cap's bootstrap. Do not assume `/tmp/bootstrap.sh` exists. Do not hand-write `apt-get`.
4. Never invent a capability that is not in INDEX.

## Hard rules

- No `sudo`. No API key, token, or credential the user did not provide in this chat.
- Do not treat a background process (MCP / tmux / pm2) as a new host tool.
- Do not paste secrets or huge XML / HTML / logs; save and slice locally.
- Domain caps stay optional until the user asks for that domain, except when INDEX already states a clear primary-source win.

## Pointers (do not inline recipes here)

- `INDEX.md` — catalog
- `caps/*.md` — procedure
- `caps/bootstrap.md` and `bin/bootstrap.sh` — install
- `HARDNO.md` / `ENV.md` — only if needed
