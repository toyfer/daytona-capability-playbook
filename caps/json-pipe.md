# json-pipe

**What:** 単発 JSON ストリームを `jq` で切る。  
**When:** API 1 レスポンス・1 ファイルの整形・フィールド抽出。  
**Not when:** 数百ファイルの集計 → Python 一括（`json` モジュール）。小細工なら `python3 -m json.tool` で足りる。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh cli-min
source /workspace/.tools/env
```

## Use

```bash
curl -fsSL 'https://example.com/api.json' | jq '.items[] | {id, title}'
jq -r '.laws[].law_info.law_id' /tmp/laws.json
```

## Fallback

```bash
python3 -m json.tool < file.json | head
python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.keys())'
```

## Hard no

- `find … -exec jq` やファイル毎 jq プロセス大量起動をしない
