# Databricks notebook source
"""Fail the job when core data-quality expectations are not met."""

from pyspark.sql import functions as F


CATALOG = "databricks_course"
trips = spark.table(f"{CATALOG}.silver.trips_enriched")
zones = spark.table(f"{CATALOG}.silver.taxi_zones")

checks = {
    "silver_has_rows": trips.limit(1).count() == 1,
    "zones_have_rows": zones.limit(1).count() == 1,
    "pickup_datetime_not_null": trips.filter(F.col("tpep_pickup_datetime").isNull()).count() == 0,
    "positive_distance": trips.filter(F.col("trip_distance") <= 0).count() == 0,
    "non_negative_total": trips.filter(F.col("total_amount") < 0).count() == 0,
    "daily_kpis_has_rows": spark.table(f"{CATALOG}.gold.daily_kpis").limit(1).count() == 1,
}

failed = [name for name, passed in checks.items() if not passed]
print(checks)
if failed:
    raise AssertionError(f"Data quality checks failed: {', '.join(failed)}")

