# Evidencia de aprovisionamiento de cómputo

Fecha: 2026-09-30

## Workspace principal: East US 2

- Workspace: `adb-databrickspy2026`
- Se probaron tamaños de hasta 4 vCPU.
- Azure devolvió falta de disponibilidad física (`SkuNotAvailable` / `CLOUD_PROVIDER_RESOURCE_STOCKOUT`).
- Las ejecuciones se cancelaron y el clúster quedó apagado.

## Workspace alternativo: South Central US

- Workspace: `adb-databrickspy2026-scus`
- Job: `493919681472792`
- Se probaron las familias habilitadas `Standard_D4as_v7` (4 vCPU) y `Standard_D2ds_v6` (2 vCPU).
- La ejecución `527751574349057` registró inicialmente `AZURE_QUOTA_EXCEEDED_EXCEPTION` porque la liberación del intento anterior aún ocupaba temporalmente 4 vCPU.
- Después de confirmar que el uso volvió a `0/4`, el reintento de 2 vCPU permaneció en `PENDING` sin asignación física durante el intervalo de control.
- La ejecución se canceló de forma segura y no quedó cómputo activo.

## Componentes validados

- ADLS Gen2 con contenedores `raw`, `bronze`, `silver` y `gold`.
- Access Connector con identidad administrada y RBAC.
- Credencial de almacenamiento de Unity Catalog.
- Ubicaciones externas para las cuatro zonas.
- Catálogo `databricks_course` y esquemas `bronze`, `silver` y `gold`.
- Notebooks y Job desplegados en el workspace alternativo.

Esta evidencia documenta una limitación externa de capacidad de Azure y no un error del código ETL.

## Resolución

- El Job se migró a Databricks Serverless para evitar la dependencia de capacidad de VM de la suscripción.
- Ejecución final: `447409550489431`.
- Reparación: `271483939752289`.
- Resultado final: `SUCCESS` en `setup`, `ingest_raw`, `bronze`, `silver`, `gold` y `quality_checks`.
