"""DuckDB Spatial analytical query engine for GeoParquet files."""

from pathlib import Path
from typing import Any, Dict, List
import duckdb


class DuckDBSpatialEngine:
    """
    Executes in-process analytical spatial queries on GeoParquet datasets using DuckDB Spatial.
    Zero-copy columnar processing with SIMD acceleration.
    """

    def __init__(self, memory_limit: str = "8GB"):
        self.con = duckdb.connect(database=":memory:")
        self.con.execute(f"SET memory_limit = '{memory_limit}';")
        self.con.execute("INSTALL spatial;")
        self.con.execute("LOAD spatial;")

    def query_canopy_coverage(
        self,
        canopy_parquet: Path,
        boundaries_parquet: Path,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Calculates aggregate canopy area and count per administrative boundary or parcel.
        """
        query = f"""
            WITH canopy AS (
                SELECT ST_GeomFromWKB(geometry) AS geom
                FROM read_parquet('{canopy_parquet}')
            ),
            bounds AS (
                SELECT id, name, ST_GeomFromWKB(geometry) AS geom
                FROM read_parquet('{boundaries_parquet}')
            )
            SELECT 
                b.name AS boundary_name,
                COUNT(c.geom) AS tree_crown_count,
                ROUND(SUM(ST_Area(c.geom)), 2) AS total_canopy_area_m2
            FROM bounds b
            JOIN canopy c 
              ON ST_Intersects(b.geom, c.geom)
            GROUP BY b.name
            ORDER BY total_canopy_area_m2 DESC
            LIMIT {limit};
        """
        df = self.con.execute(query).df()
        return df.to_dict(orient="records")

    def count_features(self, parquet_path: Path) -> int:
        """Instant metadata-based count without scanning raw geometries."""
        res = self.con.execute(f"SELECT count(*) FROM read_parquet('{parquet_path}')").fetchone()
        return res[0] if res else 0
