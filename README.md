# Daytona Capability Playbook

Scira + Daytona 用の追加能力カタログ。host tools と skills が既定。agent は **必要なときだけ INDEX → 該当 cap → 必要なら script** の順で読む。

- **always-on:** [`CUSTOM_INSTRUCTIONS.md`](./CUSTOM_INSTRUCTIONS.md)
- **catalog:** [`INDEX.md`](./INDEX.md)
- **capability guides:** [`caps/`](./caps/)
- **implementation:** [`bin/`](./bin/)

Raw base: `https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

## Agent flow

Host tools and skills are the default. Open INDEX only when a listed cap is needed — sandbox CLI, a primary public API the host does not wrap, or a clear win on accuracy / primary source / speed / tokens.

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/INDEX.md" -o /workspace/.playbook-index.md
# Read only the cap selected from INDEX.
```

A miss is normal: stay on host tools. Do not load a cap just in case.
Overlap routing lives in INDEX `use when` and the routing note, not in custom instructions.

## Repository roles

| path | role |
|---|---|
| `CUSTOM_INSTRUCTIONS.md` | Thin global gate: when to open INDEX. No router or recipes |
| `INDEX.md` | Thin capability catalog: what / when / path / profile |
| `caps/bootstrap.md` | Install contract and profile definitions |
| `caps/*.md` | Task-specific procedure, boundary, and failure prevention |
| `bin/*` | Executable implementation |
| `ENV.md` | Environment snapshot only |
| `HARDNO.md` | Cross-cutting guardrails |
| `OPS.md` | Maintenance rules and history |

## Rules for maintainers

- Do not duplicate a recipe across custom instructions, INDEX, and caps.
- Keep `INDEX.md` as a table of contents, not a router manual. Short overlap examples may live in the routing note.
- Add a capability only with a clear `what`, `when`, `not when`, and an executable or deterministic procedure when appropriate.
- Domain-specific capabilities remain optional unless the task explicitly requests that domain, or INDEX already states a clear primary-source win.
- Deploy `CUSTOM_INSTRUCTIONS.md` to Scira custom instructions in the same commit cycle; record the date in `OPS.md`.
