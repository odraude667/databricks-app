# Datasets

Esta carpeta contiene los dos insumos exigidos para el ETL. Los archivos se
conservan en su formato original y también se copian a la capa `raw` de ADLS
Gen2 durante la ejecución del pipeline.

## Yellow Taxi Trip Records

- Fuente oficial: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Archivo usado: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
- Archivo incluido en tres partes: `yellow_tripdata_2024-01.parquet.part01`,
  `part02` y `part03` (división necesaria por el límite de carga web).
- Reconstrucción local: `python reconstruct_parquet.py`
- Formato: Parquet
- Destino raw: `abfss://raw@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi/yellow_tripdata_2024-01.parquet`

## Taxi Zone Lookup

- Fuente oficial: https://www.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf
- Archivo usado: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
- Archivo incluido: `taxi_zone_lookup.csv`
- Formato: CSV
- Destino raw: `abfss://raw@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi/taxi_zone_lookup.csv`

Los archivos originales se conservan sin modificación en `raw`. Las capas
siguientes usan Delta Lake. El acceso entre Databricks y ADLS se realiza con el
Access Connector y su Managed Identity.

`reconstruct_parquet.py` concatena las partes en orden y valida la firma
Parquet. El ETL de producción descarga la copia íntegra desde la fuente oficial
y la aterriza en ADLS; la división solo afecta a la representación en GitHub.

