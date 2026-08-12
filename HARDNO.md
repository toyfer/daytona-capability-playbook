# Hard no

Cross-cutting guardrails. Capability-specific limits belong in the selected cap.

- Do not use `sudo`; this environment is normally root.
- Do not full-bootstrap at session start; install the selected profile only when needed.
- Do not hand-write `apt-get install`; use `caps/bootstrap.md` and `bin/bootstrap.sh`.
- Do not use API keys, tokens, or credentials unless supplied in this chat.
- Do not retrieve this playbook with a page-retrieval tool; use `curl`.
- Do not paste secrets or huge XML / HTML / logs into the answer; save and slice locally.
- For bulk HTML/JSON on disk: `curl` to `/workspace`, then one Python pass to extract; do not dump full pages into the chat and do not run one jq process per file.
- Do not claim a command exists without `command -v` or bootstrap confirmation.
- Do not make background MCP processes appear as new host tools.
- Do not invent or load a capability that is not listed in `INDEX.md`; if no row matches, stay on host tools.
