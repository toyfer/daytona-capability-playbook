# estat-series (optional)

**What:** Retrieve Japanese government-statistics series through the e-Stat API.  
**When:** the task needs an official series **and** the user supplied an appId in this chat.  
**Not when:** no appId is available; do not probe the API repeatedly.

## Setup

```bash
export ESTAT_APPID='user-provided-value'   # only from this chat; never commit or echo
```

Register an appId at the [e-Stat API site](https://www.e-stat.go.jp/api/) if the user has none. Without a valid appId the API returns authentication failure (`STATUS` 100).

## Use

Official base: `https://api.e-stat.go.jp/rest/3.0/app/json/`.
Save responses under `/workspace` and extract only requested metrics.

```bash
# List tables (example query — adjust searchWord / statsField)
curl -fsSL --get 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList' \
  --data-urlencode "appId=${ESTAT_APPID}" \
  --data-urlencode 'lang=J' \
  --data-urlencode 'searchWord=人口' \
  --data-urlencode 'limit=5' \
  -o /workspace/estat-list.json

# Fetch a known statsDataId (replace with an ID from the list or the user)
curl -fsSL --get 'https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData' \
  --data-urlencode "appId=${ESTAT_APPID}" \
  --data-urlencode 'lang=J' \
  --data-urlencode 'statsDataId=YOUR_STATS_DATA_ID' \
  --data-urlencode 'metaGetFlg=Y' \
  -o /workspace/estat-data.json
```

Full parameter reference: [e-Stat API spec (JP)](https://www.e-stat.go.jp/api/api-info/e-stat-manual3-0).

## Notes

- Do not expose the appId in logs, answers, or commits.
- Include the statistic name, table / statsDataId, and reference date in any reported figures.
- One failed auth check is enough to stop; do not retry with guessed keys.
