# Capability Index

追加能力の目次。ここには **what / when / path / profile** だけを置く。  
host で足りるなら何も load しない。詳細・手順・注意は該当 path へ。

| id | use when | path | profile |
|---|---|---|---|
| bootstrap | CLI/Python 拡張の install が必要 | caps/bootstrap.md | — |
| workspace-search | ローカル tree の文字列・記号を横断検索 | caps/workspace-search.md | cli-min |
| json-pipe | 単発 JSON の field 抽出・整形 | caps/json-pipe.md | cli-min |
| data-sql | 中〜大 CSV / 複数 file の SQL 集計 | caps/data-sql.md | data |
| pdf-extract | 既存 PDF の text / table 抽出 | caps/pdf-extract.md | — |
| jp-encoding | SJIS/EUC 等を UTF-8 へ変換 | caps/jp-encoding.md | jp-text |
| docs-convert | 多数 Markdown の機械的変換 | caps/docs-convert.md | docs-extra |
| ocr-scan | text layer のない scan / image OCR | caps/ocr-scan.md | ocr |
| media-ffmpeg | 明示された media batch conversion | caps/media-ffmpeg.md | media |
| keyless-open-data | host に専用 tool がない keyless public API | caps/keyless-open-data.md | — |

## Optional

| id | use when | path | profile |
|---|---|---|---|
| jp-law-egov | 日本法令の一次条文・法令番号が必要 | caps/jp-law-egov.md | — |
| estat-series | user-provided appId で e-Stat series が必要 | caps/estat-series.md | — |

## Routing note

- 行が無い → **即 host / 接続済み MCP**（一般 web 調査・製品比較はここに入る）。
- cap は sandbox 拡張と特定 public API のみ。ドメイン知識の置き場ではない。

補助は必要な時だけ `ENV.md` / `HARDNO.md`。
