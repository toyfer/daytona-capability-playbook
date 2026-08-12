# workspace-search — INDEXから削除（host/初期shellで代替）

**Status:** INDEXから外した。初期shellに `grep -R -n` があり、bench 2026-08-12 で 300file 9kヒット `rg 0.009s` vs `grep 0.006s` と互角。わざわざ `rg` を入れる勝ち筋が無い。

使うなら直接このファイルを読む:

```bash
rg -n 'pattern' /workspace
rg -n -C 3 'pattern' /workspace/src
```
代替（初期shellで可）:
```bash
grep -R -n 'pattern' /workspace --include='*.py' | head -n 200
```

`caps/bootstrap.md` profile `cli-min` は他で使わないため、必要な時だけ手動で `bash /tmp/bootstrap.sh cli-min`。
