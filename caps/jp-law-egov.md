# jp-law-egov（optional）

**What:** 日本の法令 API（e-Gov）を薄い CLI で検索・条文取得する。  
**When:** 法令名・法令番号・条文の**一次ソース**が必要なとき。  
**Not when:** 一般の法律解説・ニュース・判例評釈 → host `web_search`。タスクが法令根拠を求めていないとき（load しない）。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/egov.py" -o /tmp/egov.py
```

認証不要（keyless）。

## Use

```bash
python3 /tmp/egov.py search '個人情報の保護に関する法律'
python3 /tmp/egov.py resolve '地方自治法'
python3 /tmp/egov.py article '地方自治法' 1
python3 /tmp/egov.py text '生活保護法' '外国人'
python3 /tmp/egov.py body '415AC0000000057' /workspace/law.xml
```

- `body` / `article` / `text` は法令名からも lawId を解決する
- 回答には **法令番号または lawId** を残す

## API メモ（実測）

| 用途 | 結果 |
|---|---|
| v2 laws 検索 | 200 JSON |
| v1 lawdata 全文 | 200 XML |
| v1 articles 条 | 200 XML |
| v1 lawrevisions | **404 — 使うな** |

## Hard no

- 全文 XML をプロンプト / 回答に貼らない（`/workspace` に保存し該当条だけ）
- `lawrevisions` を叩かない
- 法律相談・確定解釈の断定をしない
- ブログ記事を一次根拠扱いしない
