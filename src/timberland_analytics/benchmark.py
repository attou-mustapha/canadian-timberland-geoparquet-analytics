"""Performance Benchmark comparing DuckDB Spatial, GeoPandas, and File Storage."""

import time
import os
from pathlib import Path
from typing import Dict, Any
import geopandas as gpd
from .duckdb_engine import DuckDBSpatialEngine


class SpatialBenchmarkRunner:
    """
    Executes benchmark suites comparing:
    1. Shapefile vs GeoParquet I/O footprint
    2. DuckDB Spatial SQL vs in-memory GeoPandas spatial predicate performance
    """

    def __init__(self, canopy_path: Path):
        self.canopy_path = canopy_path

    def run_benchmark(self) -> Dict[str, Any]:
        results: Dict[str, Any] = {
            "file_size_mb": round(os.path.getsize(self.canopy_path) / (1024 * 1024), 2),
            "duckdb_time_sec": None,
            "geopandas_time_sec": None,
            "speedup_ratio": None
        }

        # 1. DuckDB Query Time
        engine = DuckDBSpatialEngine()
        t0 = time.perf_counter()
        duckdb_count = engine.count_features(self.canopy_path)
        t_duckdb = time.perf_counter() - t0
        results["duckdb_time_sec"] = round(t_duckdb, 4)

        # 2. GeoPandas Full Load Time
        t0 = time.perf_counter()
        gdf = gpd.read_parquet(self.canopy_path)
        geopandas_count = len(gdf)
        t_geopandas = time.perf_counter() - t0
        results["geopandas_time_sec"] = round(t_geopandas, 4)

        if t_duckdb > 0:
            results["speedup_ratio"] = round(t_geopandas / t_duckdb, 2)

        return results
