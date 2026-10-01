-- Databricks notebook source
-- Reversión lógica: elimina tablas y esquemas, pero conserva archivos de ADLS.

DROP TABLE IF EXISTS databricks_course.gold.payment_summary;
DROP TABLE IF EXISTS databricks_course.gold.zone_performance;
DROP TABLE IF EXISTS databricks_course.gold.daily_kpis;
DROP TABLE IF EXISTS databricks_course.silver.taxi_zones;
DROP TABLE IF EXISTS databricks_course.silver.trips_enriched;
DROP TABLE IF EXISTS databricks_course.bronze.taxi_zones;
DROP TABLE IF EXISTS databricks_course.bronze.yellow_trips;

DROP SCHEMA IF EXISTS databricks_course.gold;
DROP SCHEMA IF EXISTS databricks_course.silver;
DROP SCHEMA IF EXISTS databricks_course.bronze;
DROP CATALOG IF EXISTS databricks_course;

