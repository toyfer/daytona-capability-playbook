# keyless-geo-open-data

**What:** Query simple keyless public APIs with `curl`.  
**When:** host lacks a dedicated tool and one public endpoint answers the task.  
**Not when:** authentication is required, rate limits would be abused, or a host tool is better.

## Use

```bash
# Postal code → address
curl -fsSL 'https://zipcloud.ibsnet.co.jp/api/search?zipcode=1000001' | python3 -m json.tool

# Open-data catalog search
curl -fsSL --get 'https://data.e-gov.go.jp/data/api/action/package_search' \
  --data-urlencode 'q=人口' --data-urlencode 'rows=5' | python3 -m json.tool | head -100

# JMA forecast JSON (Tokyo)
curl -fsSL 'https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json' | python3 -m json.tool | head -80
```

Extract only needed fields; do not paste whole API responses or ignore provider rate limits.
