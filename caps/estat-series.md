# estat-series（optional）

**What:** 日本の政府統計（e-Stat API）の数値系列。  
**When:** 公的統計の系列が必要 **かつ** ユーザーがこのチャットで **appId を渡した**とき。  
**Not when:** appId が無い。カタログ探索だけなら `keyless-geo-open-data` の CKAN 等。

## Setup

appId がチャットに無いなら**何もしない**（STATUS 100 で失敗する）。

```bash
# ユーザー提供の appId のみ。ハードコードしない
export ESTAT_APPID='...'   # ユーザーが渡した値
```

## Use

公式の e-Stat API 仕様に従い `curl` で取得。応答は `/workspace` に保存し、必要な指標だけ要約する。

## Hard no

- appId なしで連打しない
- appId をログ・回答・コミットに残さない
- 取得系列の出典（統計名、表 ID、時点）を回答に残す
