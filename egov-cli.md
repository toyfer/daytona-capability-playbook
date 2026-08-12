# e-Gov 法令 API 薄い CLI 手順（検証済み 2026-08-12）

シェルから直接叩く。認証不要（keyless）。

## エンドポイント実測結果

| エンドポイント | 結果 | 用途 |
|---|---|---|
| `GET /api/2/laws?law_title=...&limit=...` | **200 JSON** | 法令検索（推奨） |
| `GET /api/2/laws?keyword=...` | 200（広いヒット） | 広めの探索 |
| `GET /api/1/lawdata/{法令番号 or lawId}` | **200 XML** | 全文 |
| `GET /api/1/articles;lawId=...;article=...` | **200 XML** | 条文だけ |
| `GET /api/1/lawrevisions/{...}` | **404** | 使えない。改正は lawdata 内 or web_search |

## 基本フロー

```bash
# 1) 法令名で検索 → law_title / law_num / law_id を取得
curl -sS --get 'https://laws.e-gov.go.jp/api/2/laws' \
  --data-urlencode 'law_title=個人情報の保護に関する法律' \
  --data-urlencode 'limit=3' | python3 -m json.tool

# 2) 全文を取得（法令番号 or lawId）
curl -sS "https://laws.e-gov.go.jp/api/1/lawdata/415AC0000000057" -o /tmp/law.xml

# 3) 条文だけ取得（lawId + 条番号）
curl -sS "https://laws.e-gov.go.jp/api/1/articles;lawId=415AC0000000057;article=1" -o /tmp/art.xml
```

## 条文 XML から中身を抽出

```bash
python3 - <<'PY'
import urllib.request, re
law_id='415AC0000000057'
xml=urllib.request.urlopen(
  'https://laws.e-gov.go.jp/api/1/articles;lawId=%s;article=1'%law_id,
  timeout=30).read().decode('utf-8','replace')
for m in re.findall(r'<ArticleTitle[^>]*>(.*?)</ArticleTitle>', xml, re.S)[:2]:
    print('Title:', re.sub(r'<[^>]+>','',m).strip())
for m in re.findall(r'<Sentence[^>]*>(.*?)</Sentence>', xml, re.S)[:3]:
    print('Sentence:', re.sub(r'<[^>]+>','',m).strip())
PY
```

## 注意

- **lawrevisions は 404**（法令番号・lawId どちらでも不可）。改正履歴は lawdata の XML 内の改正情報を探すか、host web_search で補完する。
- 全文 XML は数百 KB。プロンプトに全文を貼らない。`/tmp` か `/workspace` に保存し、該当条だけ引用。
- 法令番号・lawId は回答に必ず残す。
- 法律相談・確定解釈の断定はしない。

## 参照

- [e-Gov 法令 API v1 ドキュメント](https://laws.e-gov.go.jp/docs/law-data-basic/8529371-law-api-v1/)
- [e-Gov 法令 API v2 swagger](https://laws.e-gov.go.jp/api/2/swagger-ui)
