# jp-encoding

**What:** 日本語レガシー文字コード・改行を nkf で変換する。  
**When:** SJIS/CP932/EUC の CSV・テキストを UTF-8 にしたいとき。  
**Not when:** 既に UTF-8。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh jp-text
source /workspace/.tools/env
```

## Use

```bash
nkf --guess file.csv
nkf -w -Lu file.csv > file.utf8.csv
```

## Fallback

```bash
iconv -f CP932 -t UTF-8 file.csv > file.utf8.csv
```

当てずっぽうの from コードは壊す。可能なら `nkf --guess` を先に。
