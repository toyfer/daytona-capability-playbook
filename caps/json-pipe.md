# json-pipe — INDEXから削除（初期shellのPythonで代替）

**Status:** INDEXから外した。初期shellに `python3` があり、bench 2026-08-12 5k件select `jq 0.0065s` vs `python 0.0016s` でpythonが速い。多数fileはPython一括がhost推奨。

使うなら直接このファイルを読む:

```bash
curl -fsSL 'https://example.com/api.json' | jq '.items[] | {id, title}'
jq -r '.laws[].law_info.law_id' /tmp/laws.json
```
代替（初期shellで可）:
```bash
python3 -m json.tool < file.json | head
python3 -c 'import json,pathlib; d=json.loads(pathlib.Path("file.json").read_text()); print([{"id":x["id"],"title":x["title"]} for x in d["items"][:5]])'
```

`jq` が必要なら `bash /tmp/bootstrap.sh cli-min` だが、無理に入れるほどではない。
