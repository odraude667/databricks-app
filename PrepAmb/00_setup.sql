-- Databricks notebook source
CREATE CATALOG IF NOT EXISTS databricks_course
MANAGED LOCATION 'abfss://gold@stdatabrickspy2026.dfs.core.windows.net/managed/databricks_course';

CREATE SCHEMA IF NOT EXISTS databricks_course.bronze
COMMENT 'Raw ingested Delta tables with minimal transformation';

CREATE SCHEMA IF NOT EXISTS databricks_course.silver
COMMENT 'Cleaned and conformed Delta tables';

CREATE SCHEMA IF NOT EXISTS databricks_course.gold
COMMENT 'Business-ready analytical Delta tables';

USE CATALOG databricks_course;

