# Daytona Capability Playbook

Scira + Daytona 用の追加能力カタログ。agent は **INDEX → 必要な cap → 必要なら script** の順で読む。

- **always-on:** [`CUSTOM_INSTRUCTIONS.md`](./CUSTOM_INSTRUCTIONS.md)
- **catalog:** [`INDEX.md`](./INDEX.md)
- **capability guides:** [`caps/`](./caps/)
- **implementation:** [`bin/`](./bin/)

Raw base: `https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

## Agent flow

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/INDEX.md" -o /workspace/.playbook-index.md
# Read only the cap selected from INDEX.
```

Host tools are the default. Load a capability only when it materially improves accuracy, primary-source access, speed, or token efficiency.

## Repository roles

| path | role |
|---|---|
| `CUSTOM_INSTRUCTIONS.md` | Thin global entrypoint; no router or recipes |
| `INDEX.md` | Thin capability catalog: what / when / path / profile |
| `caps/bootstrap.md` | Install contract and profile definitions |
| `caps/*.md` | Task-specific procedure, boundary, and failure prevention |
| `bin/*` | Executable implementation |
| `ENV.md` | Environment snapshot only |
| `HARDNO.md` | Cross-cutting guardrails |
| `OPS.md` | Maintenance rules and history |

## Rules for maintainers

- Do not duplicate a recipe across custom instructions, INDEX, and caps.
- Keep `INDEX.md` as a table of contents, not a router manual.
- Add a capability only with a clear `what`, `when`, `not when`, and an executable or deterministic procedure when appropriate.
- Domain-specific capabilities remain optional unless the task explicitly requests that domain.
