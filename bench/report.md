# ベンチ: ルーター文言を決めるための実測

測定: 2026-08-12, Debian sandbox, /workspace
CLIは前後で `time.perf_counter()`、hostは実行直前に `date +%s.%N` を残して `web_search`/`get_weather_data`/`retrieve` を呼び出し、戻り直後に再取得。3回実行の中央値。

## 結果（中央値）

| タスク | cap 経路 | host 経路 | 比 | メモ |
|---|---|---|---|---|
| INDEX peek (2181B) | 0.031s | — | — | 1回peekは安い。毎回強制は不要、当たり所だけで十分 |
| cap本体+egov.py fetch | 0.032+0.032s | — | — | 2本で0.06s。初回のみ |
| egov resolve 地方自治法 | 1.02s +peek0.06=1.08s | web_search 3query合計9.36s → 1クエリ3.12s | cap 2.9x | 出力: `322AC0000000067 地方自治法` 687B。hostは要整形 |
| egov article 地方自治法 1条 | 2.64s | web_search同上 | cap 3.5x / token勝ち | cap 162文字の本文。retrieve e-Govは2MB HTML相当 (102s計測はページ全体) |
| egov search 個人情報保護法 | 1.94s | — | — | total 17, id 415AC0000000057 |
| 300k行 CSV groupby | duckdb 0.118s | pandas 0.373s (warm 0.11) | cap 3.1x | 小CSVはpandasで可。複数file/結合は差が拡大 |
| tree 9k一致 grep | rg 0.0089s | grep 0.0065s | host 1.4x | bootstrap済みでも同等。未installならgrepで可 — INDEXから削除 |
| SJIS→UTF8 | nkf 0.0011s | iconv 0.0015s | 1.1x | 速度は誤差、`nkf --guess`が勝ち筋 |
| JSON 5/5000 select | jq 0.0065s | python 0.0016s | host 4.1x | 1ファイルならpythonが速い。jqはワンライナー向け — INDEXから削除 |
| PDF extract | fitz 0.0027s | pdfplumber 0.102s | fitz 38x | 両方cap内の比較。2026-08-12 は host `pdf` を「作る」側と見たが、後に host skill は extract/OCR を含む。残余（巨大・レイアウト・fitz）を再測定すること |
| keyless zip 100-0001 | 0.12s | find_place(失敗) 5.94s | cap 49x | host mapは課金エラーだが成功しても往復多い |
| keyless JMA 東京 | 0.048s | get_weather 7.05s | cap 147x | hostは5日+大気汚染の濃い出力。JMA JSONだけ欲しいなら圧勝 |

## 判断（初期shell/hostで足りるか）

初期shell: `bash curl git python3 pip3 uv node npm npx perl java tar gzip xz openssl iconv sqlite3` + GNU coreutils(grep等)
初期Python: `pymupdf pdfplumber pdfminer pypdfium2 tabula bs4 lxml httpx requests pandas numpy scipy sklearn matplotlib seaborn plotly yfinance duckdb`
通常不在: `jq rg fd nkf pandoc pdftotext/poppler qpdf tesseract ffmpeg convert`

- **互角/負けはINDEXから削除**: `workspace-search` (rg vs grep 互角)、`json-pipe` (jq vs pythonで負け) は初期shellで足りるため削除。直接capを読めば使える。
- **残すもの**: 初期shell/hostに無い機能か明確な残余勝ちがあるものだけ。`data-sql` (3.1x), `jp-encoding` (--guess), `pdf-extract` (残余: 巨大/レイアウト/fitz。host `pdf` が extract を含むなら通常は host), `docs-convert` (バッチ), `ocr-scan` (tesseract 不在 / jpn+eng), `media-ffmpeg`, `keyless-open-data` (49x/147x), `jp-law-egov` (2.9x)。
- **peekコスト**: 0.03s。web_search 1回3sの1%なので当たり所では元が取れる。外れでは純増なので「当たりそうなときだけpeek」が正しい。
- **host skill は変わる**: 2026-08-12 の「host pdfは作る側」は観測であり、2026-08-14 時点では host `pdf` description が extract/OCR を含む。INDEX `use when` に host 内部事実を固定しない。

## 推奨INDEX表記

`use when` に勝ち筋を1語だけ足し、速度数値はcap本文に退避。INDEXはselector、詳細はcap。host の内部事実は書かない。
