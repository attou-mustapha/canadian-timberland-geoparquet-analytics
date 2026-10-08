"""Unit tests for GeoParquet ETL."""

import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from timberland_analytics.etl import GeoParquetETL


def test_geoparquet_conversion(tmp_path):
    # Create sample polygon
    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
    gdf = gpd.GeoDataFrame(
        [{"id": 101, "borough": "Ahuntsic", "geometry": poly}],
        crs="EPSG:4326"
    )

    src_shp = tmp_path / "sample.shp"
    gdf.to_file(src_shp)

    dest_parquet = tmp_path / "sample.parquet"
    etl = GeoParquetETL()
    etl.convert_to_geoparquet(src_shp, dest_parquet)

    assert dest_parquet.exists()
    read_back = gpd.read_parquet(dest_parquet)
    assert len(read_back) == 1
    assert read_back.iloc[0]["borough"] == "Ahuntsic"
