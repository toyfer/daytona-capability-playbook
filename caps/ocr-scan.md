# ocr-scan

**What:** スキャン PDF / 画像を tesseract で OCR。  
**When:** テキスト層が無く、pymupdf 等で文字が取れないとき。  
**Not when:** テキスト PDF。重いので明示時のみ。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh ocr
source /workspace/.tools/env
```

## Use

```bash
tesseract page.png stdout -l jpn+eng
```

PDF はページ画像化が先（pdftoppm 等が docs-extra / poppler 経由で使える場合あり）。

## Hard no

- 全ページ OCR 結果をプロンプトに貼らない
- テキスト層がある文書に使わない
