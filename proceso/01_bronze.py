# Databricks notebook source
"""Load immutable source files and persist minimally transformed Bronze Delta tables."""

from pyspark.sql import functions as F


CATALOG = "databricks_course"
RAW_ROOT = "abfss://raw@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi"
BRONZE_ROOT = "abfss://bronze@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi"

trips = (
    spark.read.parquet(f"{RAW_ROOT}/yellow_tripdata_2024-01.parquet")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

zones = (
    spark.read.option("header", True).option("inferSchema", True)
    .csv(f"{RAW_ROOT}/taxi_zone_lookup.csv")
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

(
    trips.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .option("path", f"{BRONZE_ROOT}/yellow_trips")
    .saveAsTable(f"{CATALOG}.bronze.yellow_trips")
)

(
    zones.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .option("path", f"{BRONZE_ROOT}/taxi_zones")
    .saveAsTable(f"{CATALOG}.bronze.taxi_zones")
)

print({"yellow_trips": trips.count(), "taxi_zones": zones.count()})
