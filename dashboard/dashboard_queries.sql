-- Databricks notebook source
-- KPI diarios
SELECT *
FROM databricks_course.gold.daily_kpis
ORDER BY pickup_date;

-- Top 15 zonas por cantidad de viajes
SELECT pickup_borough, pickup_zone, total_pickups, total_revenue, avg_ticket
FROM databricks_course.gold.zone_performance
ORDER BY total_pickups DESC
LIMIT 15;

-- Distribución por método de pago
SELECT payment_type, total_trips, total_revenue, avg_tip
FROM databricks_course.gold.payment_summary
ORDER BY total_trips DESC;

