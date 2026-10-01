"""Reconstruct the original NYC Taxi Parquet file from GitHub-sized parts."""

from pathlib import Path


DATASET_DIR = Path(__file__).resolve().parent
OUTPUT = DATASET_DIR / "yellow_tripdata_2024-01.parquet"
PARTS = sorted(DATASET_DIR.glob("yellow_tripdata_2024-01.parquet.part*"))

if len(PARTS) != 3:
    raise RuntimeError(f"Expected 3 dataset parts, found {len(PARTS)}")

with OUTPUT.open("wb") as destination:
    for part in PARTS:
        with part.open("rb") as source:
            while chunk := source.read(1024 * 1024):
                destination.write(chunk)

with OUTPUT.open("rb") as reconstructed:
    header = reconstructed.read(4)
    reconstructed.seek(-4, 2)
    footer = reconstructed.read(4)

if header != b"PAR1" or footer != b"PAR1":
    OUTPUT.unlink(missing_ok=True)
    raise RuntimeError("Reconstructed file does not have a valid Parquet signature")

print(f"Reconstructed {OUTPUT.name} ({OUTPUT.stat().st_size:,} bytes)")
