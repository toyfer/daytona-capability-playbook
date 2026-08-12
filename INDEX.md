# Capability Index

追加能力の目次。ここには **what / when / path / profile** だけを置く。  
host / skills で足りるなら何も load しない。詳細・手順・注意は該当 path へ。

| id | use when | path | profile |
|---|---|---|---|
| bootstrap | CLI/Python 拡張の install が必要 | caps/bootstrap.md | — |
| data-sql | 中〜大 CSV / 複数 file の SQL 集計（pandasが重いとき 300kで3.1x） | caps/data-sql.md | data |
| pdf-extract | 既存 PDF の text / table 抽出（host pdfは作成用） | caps/pdf-extract.md | — |
| jp-encoding | SJIS/EUC 等を UTF-8 へ変換（nkf --guess、iconvはguess無し） | caps/jp-encoding.md | jp-text |
| docs-convert | 多数 Markdown の機械的変換（1文書はhost docx/pdf） | caps/docs-convert.md | docs-extra |
| ocr-scan | text layer のない scan / image OCR（hostに無し） | caps/ocr-scan.md | ocr |
| media-ffmpeg | 明示された media batch conversion（hostは単発向け） | caps/media-ffmpeg.md | media |
| keyless-open-data | host に専用 tool がない keyless public API（1 endpointで足りるとき zip 49x / JMA 147x） | caps/keyless-open-data.md | — |

## Optional

| id | use when | path | profile |
|---|---|---|---|
| jp-law-egov | 日本法令の一次条文・法令番号が必要（web_search より先 2.9-3.5x） | caps/jp-law-egov.md | — |
| estat-series | user-provided appId で e-Stat series が必要 | caps/estat-series.md | — |

## 削除したもの（初期shell/hostで足りる）

- `workspace-search` (rg): 初期shellに `grep -R` があり 300file 9kヒットで 0.009s vs 0.006s と互角。`grep -R -n --include='*.py'` で代替。
- `json-pipe` (jq): 初期shellに `python -c` / `python -m json.tool` があり 5k件selectで 0.0016s vs 0.0065s とpythonが速い。多数fileはPython一括がhost推奨。

詳細は `caps/workspace-search.md` / `caps/json-pipe.md` を直接見れば使えるが、INDEXからは外した（host/初期shellで足りるため）。

## Routing note

- 行が無い → **即 host / skills / 接続済み MCP**。一般 web 調査・製品比較はここに入る。
- cap は sandbox 拡張と、host が包んでいない public API だけ。ドメイン知識の置き場ではない。
- 用途が重なるとき: INDEX の use when が一次ソース・決定的手続き・明確な速度勝ちを書いていれば cap。それ以外は host。
- 例: 日本の条文・法令番号 → `jp-law-egov`（web_search より先）。法令の解説・ニュース・判例 → host。
- 例: 体裁の良い 1 文書を「作る」 → host の docx/pdf/xlsx/pptx。既存 PDF から抜く → `pdf-extract`。
- 例: 小CSV/1件JSON → host Python / skills。中〜大CSVの結合・集計 → `data-sql`。

補助は必要な時だけ `ENV.md` / `HARDNO.md`。測定: `bench/report.md`（2026-08-12 INDEX peek 0.03s、egov 1-2s vs web 3s、duckdb 0.12s vs pandas 0.37s）。
