# Capability INDEX

Scira カスタム指示が最初に curl する**薄いカタログ**。
各行の description は skill metadata と同じく **what + when**。
詳細は path を curl してから使え。ここに手順を増やさない。

**Raw base:** `https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main`

## 読み方

1. タスクに description が当たる行だけ選ぶ（複数可）
2. `path` を curl する（md / sh / py）
3. `profile` があれば、能力を使う直前に `bin/bootstrap.sh <profile>`
4. host で足りるなら何も load しない

## 横断（必要なときだけ）

| id | description | path | profile |
|---|---|---|---|
| env | サンドボックスの実測インベントリ（何が最初からあるか / 無いか）。install 前や「入ってるはず」で迷ったとき | ENV.md | — |
| hardno | 横断の禁止・失敗パターン。能力実行前に一度目を通すとよい | HARDNO.md | — |
| bootstrap | CLI/Python 拡張の唯一 install 入口。jq/rg 等が無く、今のタスクに必要なとき | bin/bootstrap.sh | 引数で指定 |

## コア能力

| id | description | path | profile |
|---|---|---|---|
| workspace-search | `/workspace` 内の高速文字列・記号検索（ripgrep）。リポジトリ横断 grep が要るとき。リモート GitHub コードは host github_search | caps/workspace-search.md | cli-min |
| json-pipe | 単発 JSON をパイプで切る（jq）。API 1 レスポンスの整形。多数ファイル集計は Python 一括 | caps/json-pipe.md | cli-min |
| data-sql | 中〜大 CSV の SQL 集計（duckdb Python）。pandas では重い結合・集計のとき。小 CSV は pandas | caps/data-sql.md | data |
| pdf-extract | 既存 PDF のテキスト・表抽出。**既備** pymupdf / pdfplumber / tabula。install 不要。スキャン画像は ocr | caps/pdf-extract.md | — |
| jp-encoding | 日本語レガシー文字コード・改行変換（nkf）。SJIS/EUC ファイルを UTF-8 にするとき | caps/jp-encoding.md | jp-text |
| keyless-geo-open-data | キーレスの郵便番号→住所・オープンデータカタログ・気象 JSON。host に専用 tool が無いとき | caps/keyless-geo-open-data.md | — |
| docs-convert | md の一括 html/docx 等（pandoc）。体裁の良い 1 文書 PDF/docx は host スキル優先 | caps/docs-convert.md | docs-extra |
| ocr-scan | スキャン PDF / 画像の OCR（tesseract）。テキスト層が無いときだけ。重い | caps/ocr-scan.md | ocr |
| media-ffmpeg | 動画・音声・画像バッチ（ffmpeg / imagemagick）。ユーザーが明示したときだけ。重い | caps/media-ffmpeg.md | media |

## オプション（タスクが明示的に求めるときだけ）

| id | description | path | profile |
|---|---|---|---|
| jp-law-egov | 日本の法令・条文の一次ソース取得（e-Gov API CLI）。法令名/番号/条が要る法的根拠確認のとき。解説・判例は host 検索 | caps/jp-law-egov.md | — |
| estat-series | 日本の政府統計の数値系列（e-Stat API）。**ユーザーが appId をこのチャットで渡したときだけ** | caps/estat-series.md | — |

## install profiles（bootstrap 引数）

| profile | 入るもの | 使う cap 例 |
|---|---|---|
| cli-min | jq, rg（static 優先） | workspace-search, json-pipe |
| cli-dev | + fd, unzip, file | 多ファイル開発 |
| jp-text | nkf | jp-encoding |
| data | duckdb (pip/uv), sqlite3 | data-sql |
| docs-extra | pandoc, poppler-utils, qpdf | docs-convert |
| ocr | tesseract + jpn | ocr-scan |
| media | ffmpeg, imagemagick | media-ffmpeg |

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh cli-min
source /workspace/.tools/env
```

## host のまま（playbook を開かない）

| 領域 | host |
|---|---|
| 一般事実・ニュース | web_search ± retrieve |
| ユーザー提示 URL | retrieve |
| 体裁の良い 1 文書 | docx / pdf / xlsx / pptx / artifact |
| 天気（UI tool がある場合） | weather |
| GitHub 上のコード検索 | github_search |
| 通常の file I/O・図表 | bash / code_interpreter / download_file |
