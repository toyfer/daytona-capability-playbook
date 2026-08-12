# workspace-search

**What:** `/workspace`（および明示パス）を ripgrep (`rg`) で高速文字列・記号検索する。  
**When:** ローカルツリーを横断 grep したいとき。  
**Not when:** リモート GitHub 上のコード → host `github_search`。一発の小ファイル → 素の `grep` で足りることも多い。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh cli-min
source /workspace/.tools/env
```

## Use

```bash
rg -n 'pattern' /workspace
rg -n -C 3 'pattern' /workspace/src
rg -n --type py 'def foo' /workspace
```

## Hard no / notes

- 検索対象は原則ローカルパス。秘密や巨大バイナリを無闇に掘らない
- 結果が巨大なら `| head` やより狭い path
- 意味検索（embedding 系）の代替ではない
