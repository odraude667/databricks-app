# Databricks notebook source
"""Download the two public sources and copy the immutable files to ADLS raw."""

from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


SOURCES = {
    "yellow_tripdata_2024-01.parquet": (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/"
        "yellow_tripdata_2024-01.parquet"
    ),
    "taxi_zone_lookup.csv": (
        "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    ),
}

RAW_ROOT = "abfss://raw@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi"
LOCAL_ROOT = Path("/tmp/nyc_taxi")
LOCAL_ROOT.mkdir(parents=True, exist_ok=True)

for filename, url in SOURCES.items():
    local_path = LOCAL_ROOT / filename
    try:
        urlretrieve(url, local_path)
        if local_path.stat().st_size == 0:
            raise ValueError(f"Downloaded file is empty: {filename}")
        file_size = local_path.stat().st_size
        if local_path.suffix == ".parquet":
            source_df = spark.createDataFrame(pd.read_parquet(local_path))
            source_df.write.mode("overwrite").parquet(f"{RAW_ROOT}/{filename}")
        else:
            source_df = spark.createDataFrame(pd.read_csv(local_path))
            (
                source_df.write.mode("overwrite")
                .option("header", True)
                .csv(f"{RAW_ROOT}/{filename}")
            )
        print(
            f"Landed {filename} ({file_size:,} downloaded bytes, "
            f"{source_df.count():,} rows) in raw"
        )
    finally:
        local_path.unlink(missing_ok=True)
