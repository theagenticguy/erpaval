# Python Data Pipeline Stack

For data processing, ETL, and analytical workloads.

## Core: polars

Default for all tabular data. Faster, more ergonomic, and more memory-efficient than pandas.

```python
import polars as pl

# Read and transform
df = (
    pl.scan_csv("data.csv")
    .filter(pl.col("status") == "active")
    .group_by("region")
    .agg(
        pl.col("revenue").sum().alias("total_revenue"),
        pl.col("id").count().alias("count"),
    )
    .sort("total_revenue", descending=True)
    .collect()
)
```

Key patterns:

- Use `scan_csv` / `scan_parquet` (lazy) over `read_csv` (eager) for large files
- Chain operations with lazy evaluation, call `.collect()` at the end
- Use `.with_columns()` for adding/transforming columns
- Use `.pipe()` for composable transformations

## Embedded Analytics: DuckDB

In-process analytical database. Query CSV, Parquet, JSON directly without loading into memory.

```python
import duckdb

# Query files directly
result = duckdb.sql("""
    SELECT region, SUM(revenue) as total
    FROM 'data/*.parquet'
    GROUP BY region
    ORDER BY total DESC
""").fetchdf()

# Query polars DataFrames
import polars as pl
df = pl.read_csv("data.csv")
result = duckdb.sql("SELECT * FROM df WHERE revenue > 1000").pl()
```

## Data Format: Apache Arrow / Parquet

- **Parquet** for storage (columnar, compressed, fast reads)
- **Arrow** for in-memory interchange (zero-copy between polars, DuckDB, pandas)

```python
# polars reads/writes Parquet natively
df.write_parquet("output.parquet")
df = pl.read_parquet("output.parquet")

# DuckDB reads Parquet natively
duckdb.sql("SELECT * FROM 'data.parquet'")
```

## When to Use What

| Scenario                         | Tool                                  |
| -------------------------------- | ------------------------------------- |
| DataFrame operations, transforms | polars                                |
| SQL queries on files             | DuckDB                                |
| Large file scanning              | polars lazy or DuckDB                 |
| Cross-tool interchange           | Arrow/Parquet format                  |
| Legacy pandas interop            | `df.to_pandas()` / `pl.from_pandas()` |
