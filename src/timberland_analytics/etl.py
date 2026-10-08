"""ETL Pipeline: Ingestion and Optimized Spatial Partitioning to GeoParquet."""

from pathlib import Path
from typing import Optional
import geopandas as gpd
import pyarrow as pa
import pyarrow.parquet as pq


class GeoParquetETL:
    """
    Transforms heavy provincial/municipal shapefiles and geopackages into
    Cloud-native GeoParquet format with spatial partitioning.
    """

    def __init__(self, compression: str = "zstd"):
        self.compression = compression

    def convert_to_geoparquet(
        self,
        input_path: Path,
        output_parquet_path: Path,
        partition_col: Optional[str] = None
    ) -> Path:
        """
        Converts vector source to GeoParquet with optional columnar partitioning.
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Source file not found: {input_path}")

        print(f"📦 Reading source dataset: {input_path.name}...")
        gdf = gpd.read_file(input_path)

        # Reproject to standard NAD83 / MTM or WGS84
        if gdf.crs is None:
            gdf = gdf.set_crs("EPSG:4326")

        output_parquet_path.parent.mkdir(parents=True, exist_ok=True)

        if partition_col and partition_col in gdf.columns:
            print(f"🗂️ Partitioning by column: '{partition_col}'...")
            gdf.to_parquet(
                output_parquet_path,
                compression=self.compression,
                partition_cols=[partition_col],
                schema_version="1.0.0"
            )
        else:
            print(f"💾 Saving monolithic GeoParquet: {output_parquet_path}...")
            gdf.to_parquet(
                output_parquet_path,
                compression=self.compression,
                schema_version="1.0.0"
            )

        print(f"✅ Conversion complete! Target: {output_parquet_path}")
        return output_parquet_path
