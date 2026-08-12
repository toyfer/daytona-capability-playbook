# data-sql

**What:** Run SQL-style aggregation or joins over medium/large CSVs with DuckDB's Python API.  
**When:** pandas is awkward or slow for joins, grouping, or multiple files.  
**Not when:** small CSV inspection (`pandas`) or a presentation table (host document tools).

## Setup

Profile: `data`. Follow [bootstrap](./bootstrap.md).

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
