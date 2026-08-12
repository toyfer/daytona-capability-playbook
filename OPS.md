# Operations

## Rules

- Keep `CUSTOM_INSTRUCTIONS.md` global, English, and minimal: hierarchy, when to open INDEX, hard rules, pointers only. No skill routing, no style, no recipes.
- Keep `INDEX.md` to `id / use when / path / profile` only, plus a short routing note for host-first misses and host/cap overlap.
- Keep detailed procedures and boundaries in one selected cap.
- Update `ENV.md` only after re-measuring the sandbox.
- If a failure repeats twice, add one targeted line to the owning cap or `HARDNO.md`; do not grow custom instructions. Remove before adding where possible.
- Update pinned tool URLs in `bin/bootstrap.sh` deliberately and record the date below.
- Keep `id` and `caps/<id>.md` aligned when practical; stubs may redirect renames.
- After changing `CUSTOM_INSTRUCTIONS.md`, paste the same bytes into Scira custom instructions and log the deploy date below.

## History

| date | change |
|---|---|
| 2026-08-12 | v1: initial router / tools / e-Gov notes |
| 2026-08-12 | v3: progressive disclosure with INDEX and caps |
| 2026-08-12 | v3.1: bootstrap and legacy cleanup |
| 2026-08-12 | v3.2: compressed always-on and INDEX; bootstrap contract moved to `caps/bootstrap.md`; profiles removed as duplicate metadata |
| 2026-08-12 | fix jp-law-egov CLI (lawId regex, Article split, revisions/keyword) |
| 2026-08-12 | docs: ocr input quality, media convert vs magick, estat minimal curl, ENV re-measure notes |
| 2026-08-12 | v3.3: add discovery trigger to always-on |
| 2026-08-12 | v3.4: rewrite always-on in English with explicit priority stack, minimal rules, and concrete triggers |
| 2026-08-12 | v3.5: enforce mandatory INDEX.md fetch at session start (never skip capability discovery) |
| 2026-08-12 | fix: INDEX routing note + CUSTOM load step for host-first on miss; HARDNO bulk HTML/JSON slice recipe |
| 2026-08-12 | smoke: curl INDEX/caps/bin; bootstrap all profiles; egov/keyless live; ENV drift (sqlite3+duckdb present); CUSTOM bootstrap curl; keyless id/path align |
| 2026-08-12 | v3.6: CUSTOM is a host/skills-first gate (no mandatory INDEX); overlap routing in INDEX; README/OPS aligned; deploy CUSTOM to Scira in the same cycle |
