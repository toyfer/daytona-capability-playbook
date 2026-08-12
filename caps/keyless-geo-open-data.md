# keyless-geo-open-data

**What:** キー不要の公開 API（郵便番号、オープンデータカタログ、気象 JSON 等）。  
**When:** host に専用 tool が無く、単純な curl で足りるとき。  
**Not when:** 認証必須の統計 API（→ `estat-series` かつ appId 必須）。

## Setup

不要（curl のみ）。

## Use

```bash
# 郵便番号 → 住所
curl -fsSL 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=1000001' | python3 -m json.tool

# data.e-gov CKAN カタログ検索
curl -fsSL --get 'https://data.e-gov.go.jp/data/api/action/package_search' \
  --data-urlencode 'q=人口' --data-urlencode 'rows=5' | python3 -m json.tool | head -100

# 気象庁 JSON（例: 東京）
curl -fsSL 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json' | python3 -m json.tool | head -80
```

jq があれば `cli-min` 後にパイプしてよい。

## Hard no

- レートを無視した連打をしない
- 応答全文をプロンプトに貼らず、必要なフィールドだけ
