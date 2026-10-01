# Databricks notebook source
"""Build business-ready Gold aggregates for dashboards."""

from pyspark.sql import functions as F


CATALOG = "databricks_course"
GOLD_ROOT = "abfss://gold@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi"
trips = spark.table(f"{CATALOG}.silver.trips_enriched")

daily_kpis = trips.groupBy("pickup_date").agg(
    F.count("*").alias("total_trips"),
    F.round(F.sum("total_amount"), 2).alias("total_revenue"),
    F.round(F.avg("trip_distance"), 2).alias("avg_trip_distance"),
    F.round(F.avg("trip_duration_minutes"), 2).alias("avg_trip_duration_minutes"),
    F.round(F.avg("tip_percentage"), 2).alias("avg_tip_percentage"),
)

zone_performance = trips.groupBy("pickup_borough", "pickup_zone").agg(
    F.count("*").alias("total_pickups"),
    F.round(F.sum("total_amount"), 2).alias("total_revenue"),
    F.round(F.avg("total_amount"), 2).alias("avg_ticket"),
    F.round(F.avg("trip_distance"), 2).alias("avg_distance"),
).orderBy(F.desc("total_pickups"))

payment_summary = trips.groupBy("payment_type").agg(
    F.count("*").alias("total_trips"),
    F.round(F.sum("total_amount"), 2).alias("total_revenue"),
    F.round(F.avg("tip_amount"), 2).alias("avg_tip"),
)

outputs = {
    "daily_kpis": daily_kpis,
    "zone_performance": zone_performance,
    "payment_summary": payment_summary,
}

for table_name, dataframe in outputs.items():
    (
        dataframe.write.format("delta").mode("overwrite")
        .option("overwriteSchema", "true")
        .option("path", f"{GOLD_ROOT}/{table_name}")
        .saveAsTable(f"{CATALOG}.gold.{table_name}")
    )
    print(f"{table_name}: {dataframe.count()} rows")

