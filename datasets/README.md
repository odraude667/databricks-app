# Datasets

## Yellow Taxi Trip Records

- Fuente oficial: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Archivo usado: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet
- Formato: Parquet
- Destino raw: `abfss://raw@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi/yellow_tripdata_2024-01.parquet`

## Taxi Zone Lookup

- Fuente oficial: https://www.nyc.gov/assets/tlc/downloads/pdf/trip_record_user_guide.pdf
- Archivo usado: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
- Formato: CSV
- Destino raw: `abfss://raw@stdatabrickspy2026.dfs.core.windows.net/nyc_taxi/taxi_zone_lookup.csv`

Los archivos originales se conservan sin modificación en `raw`. Las capas siguientes usan Delta Lake.

