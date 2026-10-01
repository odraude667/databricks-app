# Databricks notebook source
"""Clean, validate, deduplicate, and enrich the Bronze datasets."""

from pyspark.sql import functions as F


CATALOG = "databricks_course"
SILVER_ROOT = "abfss://silver@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi"

trips = spark.table(f"{CATALOG}.bronze.yellow_trips")
zones = spark.table(f"{CATALOG}.bronze.taxi_zones")

clean_trips = (
    trips
    .filter(F.col("tpep_pickup_datetime").isNotNull())
    .filter(F.col("tpep_dropoff_datetime") > F.col("tpep_pickup_datetime"))
    .filter(F.col("trip_distance") > 0)
    .filter(F.col("fare_amount") >= 0)
    .filter(F.col("total_amount") >= 0)
    .filter(F.col("passenger_count").between(1, 8))
    .filter(F.col("PULocationID").isNotNull() & F.col("DOLocationID").isNotNull())
    .withColumn(
        "trip_duration_minutes",
        (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60,
    )
    .withColumn("pickup_date", F.to_date("tpep_pickup_datetime"))
    .withColumn("pickup_hour", F.hour("tpep_pickup_datetime"))
    .withColumn("tip_percentage", F.when(F.col("fare_amount") > 0, F.col("tip_amount") / F.col("fare_amount") * 100))
    .dropDuplicates([
        "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
        "PULocationID", "DOLocationID", "total_amount",
    ])
)

zones_clean = zones.select(
    F.col("LocationID").cast("int").alias("location_id"),
    F.trim("Borough").alias("borough"),
    F.trim("Zone").alias("zone"),
    F.trim("service_zone").alias("service_zone"),
).dropDuplicates(["location_id"])

pickup_zones = zones_clean.select(
    F.col("location_id").alias("PULocationID"),
    F.col("borough").alias("pickup_borough"),
    F.col("zone").alias("pickup_zone"),
)

dropoff_zones = zones_clean.select(
    F.col("location_id").alias("DOLocationID"),
    F.col("borough").alias("dropoff_borough"),
    F.col("zone").alias("dropoff_zone"),
)

enriched = clean_trips.join(pickup_zones, "PULocationID", "left").join(dropoff_zones, "DOLocationID", "left")

(
    enriched.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .option("path", f"{SILVER_ROOT}/trips_enriched")
    .partitionBy("pickup_date")
    .saveAsTable(f"{CATALOG}.silver.trips_enriched")
)

(
    zones_clean.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .option("path", f"{SILVER_ROOT}/taxi_zones")
    .saveAsTable(f"{CATALOG}.silver.taxi_zones")
)

print({"clean_trips": enriched.count(), "zones": zones_clean.count()})

