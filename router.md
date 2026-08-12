# ルーター（host tool 以外を選ぶべき状況）

> カスタム指示 §2 から、詳細が必要になったら curl で読む。
> 既定は host tool（web_search / retrieve / shell / code_context / github_search / docx/pdf/artifact / weather 等）。
> この表は「host tool が最適でない」ときに代替を選ぶためのもの。

## 判定軸

`(トークン節約 or 精度向上 or 一次ソース) > (setup 秒数 + ディスク)` なら代替を選ぶ。

## ルーター表（Trigger → 代替 → なぜ host でないか）

| Trigger | 代替（Primary） | host でない理由 / host との分離 |
|---|---|---|
| 法令・条文・法令番号・改正 | **e-Gov CLI**（`bin/egov.py`） | 条文の一次ソース。web_search はブログ要約が混ざる。解説・判例・施行通知は host web_search |
| ライブラリ現行 API / 書き方 | Context7 系 docs スライス → host code_context | docs スライスは web_search+全文よりトークン小。ブログは最後 |
| /workspace 内の文字列・記号 | ripgrep（apt-get install -y ripgrep） | 素の grep より速い。GitHub 上のコード検索は host github_search |
| 意図・概念検索（同一巨大ツリーに複数回） | colgrep（index 済みなら） | 一発なら rg。毎回フル再 index する host file query は避ける |
| 中〜大 CSV / SQL 的集計 | duckdb（pip install duckdb → Python API） | pandas より速い。CLI バイナリは PATH に出ないことが多い |
| 既存 PDF のテキスト・表 | 既備 pymupdf / pdfplumber / tabula | install 不要で先に使える |
| 日本語レガシー文字コード | nkf（apt-get install -y nkf） | SJIS/EUC↔UTF-8・改行 |
| 郵便番号→住所 | zipcloud（キーレス） | 宛名リスト実務。host に専用 tool なし |
| オープンデータ横断 | data.e-gov.go.jp CKAN package_search（キーレス） | カタログ探索。host に専用 tool なし |
| 政府統計の数値系列 | e-Stat（要 appId） | appId が無い限り叩かない。あとがき参照 |

## host tool が最適なままの領域（代替しない）

| 領域 | host tool |
|---|---|
| 一般ニュース・事実 | web_search + retrieve |
| ユーザーがくれた URL | retrieve |
| 体裁の良い 1 文書 | docx / pdf / artifact |
| 天気 | weather tool |
| GitHub 上のコード検索 | github_search |
| ワークスペース内のファイル I/O | shell / readFile / writeFile |
