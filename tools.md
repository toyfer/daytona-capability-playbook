# 追加ツールセット（オンデマンド install）

> 検証日: 2026-08-12。カスタム指示の §3 から、詳細が必要になったら curl で読む。
> 常時コンテキストには載せない。使いどころはカスタム指示 §3 のルーター表に集約。

## 基本方針

- タスク単位で最小 install。`(トークン節約 or 精度向上) > (install 秒数 + ディスク)` でなければ host のまま。
- `sudo` 不要（多くは root 直）。`apt-get` を直接。
- 既に Python に入っているもの（pymupdf / pdfplumber / pandas 等）は install 不要。

## ツール一覧

| ツール | 用途 | インストール | 使いどころ |
|---|---|---|---|
| **ripgrep (rg)** | /workspace 内の文字列・記号検索 | `apt-get install -y ripgrep` | リポジトリ横断 grep。素の grep より約3.8倍速 |
| **jq** | JSON をパイプで切る | `apt-get install -y jq` | 単発ストリーム。多数 JSON は Python 一括 |
| **nkf** | 日本語文字コード・改行変換 | `apt-get install -y nkf` | SJIS/EUC↔UTF-8、`nkf --guess` |
| **duckdb** | 中〜大 CSV の SQL 集計 | `pip install duckdb` | 100万行で pandas の約2倍速。**CLI バイナリは PATH に出ない** → Python API |
| **sqlite3** | 軽量永続 DB | `apt-get install -y sqlite3` | 小規模データの永続化 |
| **pandoc** | md の一括 html/docx 変換 | `apt-get install -y pandoc` | 体裁の良い 1 文書は host docx/pdf 優先 |
| **poppler-utils** | PDF テキスト抽出 | `apt-get install -y poppler-utils` | ただし既備 pymupdf/pdfplumber を先に |
| **tesseract-ocr** | スキャン PDF の OCR | `apt-get install -y tesseract-ocr tesseract-ocr-jpn` | 画像 PDF のみ |
| **qpdf** | PDF 結合・回転 | `apt-get install -y qpdf` | 軽い PDF 操作 |
| **ffmpeg** | 動画・音声処理 | `apt-get install -y ffmpeg` | **重い。明示時のみ** |
| **imagemagick** | 画像処理 | `apt-get install -y imagemagick` | **重い。明示時のみ** |
| **colgrep** | 意図・概念の意味検索 | 公式インストーラ | 同一巨大ツリーに複数回。一発は rg |

## 既に使える（install 不要）

**Python**: `pymupdf` (fitz), `pdfplumber`, `pdfminer`, `pypdfium2`, `tabula`（+Java）, `bs4`, `lxml`, `parsel`, `scrapy`, `httpx`, `requests`, `aiohttp`, `pandas`, `numpy`, `scipy`, `sklearn`, `networkx`, stdlib `sqlite3`/`csv`/`json`/`xml`, `pydantic`, `rich`, `jinja2`, `seaborn`, `matplotlib`, `plotly`, `yfinance`

**CLI**: `bash`, `curl`, `git`, `node`, `npm`, `npx`, `python3`, `pip3`, `uv`, `perl`, `java`, `gcc`/`make`, `tar`/`gzip`/`xz`, `openssl`, `ssh`/`scp`, `iconv`, 基本 GNU coreutils, `nohup`

## キーレス API（install 不要・curl で直接）

| API | 用途 | 例 |
|---|---|---|
| **zipcloud** | 郵便番号→住所 | `curl -sS 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=1000001'` |
| **data.e-gov CKAN** | オープンデータ横断 | `curl -sS --get 'https://data.e-gov.go.jp/data/api/action/package_search' --data-urlencode 'q=自治体' --data-urlencode 'rows=5'` |
| **気象庁 JSON** | 気象 | `curl -sS 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json'` |

## ベンチ（実測）

| タスク | 素のシェル | 拡張 | 勝敗 |
|---|---|---|---|
| 大ツリー grep | grep -R 0.085s | rg 0.022s | **rg 約3.8倍速** |
| ファイル名検索 | find 0.009s | fd 0.15s | **find の勝ち（小規模）** |
| 多数 JSON 集計 | ファイル毎 jq 7.7s/500件 | Python 一括 0.1s | **Python 一括** |
| 100万行 CSV | pandas 0.9-1.1s | duckdb 0.48-0.5s | **duckdb 約2倍** |
| md→html/docx | — | pandoc 0.03-0.04s | pandoc 有効 |
| md→PDF | — | 失敗（pdflatex 不在） | host pdf 優先 |
| MCP 常駐 | — | — | **host tool は増えない** |

## 除外（入れない理由）

| 候補 | 理由 |
|---|---|
| filesystem/memory MCP 常駐 | host の bash/read/write と重複。tool 面も増えない |
| e-Stat をキーレス既定 | 実測 STATUS 100（要 appId） |
| selenium/playwright 既定化 | ブラウザバイナリなし / 重い |
| RESAS API | 提供終了・新規停止の案内あり |
| 毎回 colgrep init | 一発クエリでは rg の方が安い |
| cargo 依存の大量 CLI | toolchain 前提が脆い |
| フル texlive で pandoc PDF | ディスク破壊的。1 本の PDF は host pdf スキル |
