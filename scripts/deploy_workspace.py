"""Import project notebooks into Azure Databricks using the current Azure CLI login."""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
from pathlib import Path

import requests


HOST = os.environ.get(
    "DATABRICKS_HOST",
    "https://adb-7405605618871772.12.azuredatabricks.net",
).rstrip("/")
RESOURCE = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d"
REMOTE_ROOT = "/Shared/databricks-course"
PROJECT_ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "PrepAmb/00_setup.sql",
    "proceso/00_ingest_raw.py",
    "proceso/01_bronze.py",
    "proceso/02_silver.py",
    "proceso/03_gold.py",
    "proceso/04_quality_checks.py",
    "seguridad/grants.sql",
    "dashboard/dashboard_queries.sql",
    "reversion/drop_all.sql",
]


def azure_token() -> str:
    cli = (
        os.environ.get("AZURE_CLI_PATH")
        or shutil.which("az")
        or r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"
    )
    command = [
        cli,
        "account",
        "get-access-token",
        "--resource",
        RESOURCE,
        "--query",
        "accessToken",
        "--output",
        "tsv",
    ]
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout.strip()


def request(method: str, endpoint: str, payload: dict) -> dict:
    response = requests.request(
        method,
        f"{HOST}{endpoint}",
        headers={"Authorization": f"Bearer {TOKEN}"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json() if response.content else {}


TOKEN = azure_token()
request("POST", "/api/2.0/workspace/mkdirs", {"path": REMOTE_ROOT})

for relative_name in FILES:
    local_path = PROJECT_ROOT / relative_name
    relative_path = Path(relative_name).with_suffix("").as_posix()
    remote_path = f"{REMOTE_ROOT}/{relative_path}"
    remote_parent = remote_path.rsplit("/", 1)[0]
    request("POST", "/api/2.0/workspace/mkdirs", {"path": remote_parent})
    request(
        "POST",
        "/api/2.0/workspace/import",
        {
            "path": remote_path,
            "format": "SOURCE",
            "language": "SQL" if local_path.suffix == ".sql" else "PYTHON",
            "overwrite": True,
            "content": base64.b64encode(local_path.read_bytes()).decode("ascii"),
        },
    )
    print(json.dumps({"imported": relative_name, "path": remote_path}))
