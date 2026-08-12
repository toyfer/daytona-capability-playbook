# data-sql

**What:** 中〜大 CSV / 複数ファイルを DuckDB（Python API）で SQL 集計する。  
**When:** 行数が多く pandas が重い、SQL 的 JOIN/GROUP BY が自然なとき。  
**Not when:** 小さい CSV の describe → pandas。対話 UI の表 → host 文書 skills。

## Setup

```bash
P=https://raw.githubusercontent.com/toyfer/daytona-capability-playbook/main
curl -fsSL "$P/bin/bootstrap.sh" -o /tmp/bootstrap.sh
bash /tmp/bootstrap.sh data
```

## Use

```python
import duckdb
print(duckdb.sql("""
  SELECT col, count(*) AS n
  FROM 'data.csv'
  GROUP BY 1
  ORDER BY n DESC
  LIMIT 20
""").fetchdf())
```

CLI バイナリを無理に PATH に出さなくてよい。Python API を使う。

## Hard no

- 全 CSV をプロンプトに貼らない。集計結果の要約だけ返す
- 小データで duckdb を儀式的に使わない
