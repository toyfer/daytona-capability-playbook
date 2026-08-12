# json-pipe

**What:** Extract or reshape a single JSON response/file with `jq`.  
**When:** one API response or one local JSON file needs fields selected.  
**Not when:** bulk JSON aggregation (use Python), or basic pretty-printing (`python3 -m json.tool`).

## Setup

Profile: `cli-min`. Follow [bootstrap](./bootstrap.md).

## Use

```bash
curl -fsSL 'https://example.com/api.json' | jq '.items[] | {id, title}'
jq -r '.laws[].law_info.law_id' /tmp/laws.json
```

## Fallback

```bash
python3 -m json.tool < file.json | head
python3 -c 'import json,sys; print(json.load(sys.stdin).keys())'
```

Do not spawn one jq process per file.
