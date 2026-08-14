# data-sql

**What:** Run SQL-style aggregation or joins over medium/large CSVs with DuckDB's Python API.  
**When:** pandas is awkward or slow for joins, grouping, or multiple files.  
**Not when:** small CSV inspection (`pandas`), a presentation table (host document tools), or a loaded host analysis skill that already imported duckdb and finished the query.

## Setup

Profile: `data`. Follow [bootstrap](./bootstrap.md) only if needed:

```bash
python3 -c 'import duckdb' 2>/dev/null || bash /tmp/bootstrap.sh data
command -v sqlite3 >/dev/null || bash /tmp/bootstrap.sh data
# ensure bootstrap.sh exists first — see caps/bootstrap.md
```

On current sandboxes, `import duckdb` and `sqlite3` are often already available (see `ENV.md`).

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

Use the Python API; do not add a large DuckDB CLI. Return summarized results, not full source files.
