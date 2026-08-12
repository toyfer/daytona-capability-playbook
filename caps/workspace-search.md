# workspace-search

**What:** Search text or symbols across a local workspace with `rg`.  
**When:** a multi-file local grep is needed.  
**Not when:** remote GitHub code (`github_search`), a tiny file (`grep` may suffice), or semantic search.

## Setup

Profile: `cli-min`. Follow [bootstrap](./bootstrap.md).

## Use

```bash
rg -n 'pattern' /workspace
rg -n -C 3 'pattern' /workspace/src
rg -n --type py 'def foo' /workspace
```

## Notes

- Search an explicit local path.
- Narrow the path or pipe to `head` when output is large.
- Do not scan secrets or binaries indiscriminately.
