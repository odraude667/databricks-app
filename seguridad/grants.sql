-- Databricks notebook source
-- Ejecutar como propietario del catálogo. Sustituir los grupos si se crean nombres distintos.

GRANT USE CATALOG ON CATALOG databricks_course TO `account users`;
GRANT USE SCHEMA, SELECT ON SCHEMA databricks_course.gold TO `account users`;

-- Ejemplo de segregación para un grupo de ingeniería creado en Entra/Databricks:
-- GRANT USE CATALOG ON CATALOG databricks_course TO `data_engineers`;
-- GRANT USE SCHEMA, CREATE TABLE, MODIFY, SELECT ON SCHEMA databricks_course.bronze TO `data_engineers`;
-- GRANT USE SCHEMA, CREATE TABLE, MODIFY, SELECT ON SCHEMA databricks_course.silver TO `data_engineers`;
-- GRANT USE SCHEMA, CREATE TABLE, MODIFY, SELECT ON SCHEMA databricks_course.gold TO `data_engineers`;

