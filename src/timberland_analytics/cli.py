"""CLI Interface for Canadian Timberland Analytics Engine."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table

from .etl import GeoParquetETL
from .duckdb_engine import DuckDBSpatialEngine
from .benchmark import SpatialBenchmarkRunner

app = typer.Typer(help="Canadian Timberland & Forest GeoParquet Analytics CLI")
console = Console()


@app.command()
def convert(
    source_file: Path = typer.Argument(..., help="Path to raw Shapefile or GeoPackage"),
    output_parquet: Path = typer.Argument(..., help="Path for destination GeoParquet file"),
    partition_by: Optional[str] = typer.Option(None, "--partition-by", "-p", help="Column name to partition dataset by")
):
    """ETL: Ingest raw vector GIS files and export partitioned GeoParquet."""
    etl = GeoParquetETL()
    etl.convert_to_geoparquet(source_file, output_parquet, partition_col=partition_by)
    console.print(f"[bold green]✅ Transformed to GeoParquet: {output_parquet}[/bold green]")


@app.command()
def benchmark(
    parquet_file: Path = typer.Argument(..., help="Path to GeoParquet file to benchmark")
):
    """Run execution speed and memory benchmark: DuckDB Spatial vs GeoPandas."""
    console.print("[bold cyan]🚀 Running Spatial Benchmark...[/bold cyan]")
    runner = SpatialBenchmarkRunner(parquet_file)
    res = runner.run_benchmark()

    table = Table(title="GeoParquet Analytical Engine Benchmark")
    table.add_column("Metric", style="cyan")
    table.add_column("Measurement", style="magenta")
    table.add_row("Dataset File Size", f"{res['file_size_mb']} MB")
    table.add_row("DuckDB Spatial Scan", f"{res['duckdb_time_sec']}s")
    table.add_row("GeoPandas Full Load", f"{res['geopandas_time_sec']}s")
    table.add_row("Relative Speedup", f"{res['speedup_ratio']}x Faster")
    console.print(table)


if __name__ == "__main__":
    app()
