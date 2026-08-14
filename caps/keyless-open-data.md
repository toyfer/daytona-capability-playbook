# keyless-open-data

**What:** Query simple keyless public APIs with `curl`.  
**When:** one keyless public endpoint answers the task and the live host table has no dedicated tool, or a measured residual win applies (JMA JSON vs thick weather, postal code vs a failed or heavy map call).  
**Not when:** authentication is required, rate limits would be abused, or a loaded host tool already returned the needed fields.

## Use

```bash
# Postal code → address
curl -fsSL 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=1000001' -o /workspace/zip.json
python3 - <<'PY'
import json
d=json.load(open('/workspace/zip.json'))
print(d.get('results'))
PY

# Open-data catalog search (slice locally)
curl -fsSL --get 'https://data.e-gov.go.jp/data/api/action/package_search' \
  --data-urlencode 'q=人口' --data-urlencode 'rows=5' -o /workspace/pkg.json
python3 -c 'import json;d=json.load(open("/workspace/pkg.json"));print(d.get("success"), (d.get("result") or {}).get("count"))'

# JMA forecast JSON (Tokyo)
curl -fsSL 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json' -o /workspace/jma.json
python3 -c 'import json;d=json.load(open("/workspace/jma.json"));print(type(d).__name__, len(d))'
```

Save under `/workspace`, extract only needed fields; do not paste whole API responses or ignore provider rate limits.
