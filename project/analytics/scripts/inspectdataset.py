from pathlib import Path

import pandas as pd
from fastparquet import ParquetFile

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASETS_DIR = PROJECT_ROOT / "datasets"
CHUNK_SIZE = 100_000


def inspect_csv(path: Path) -> None:
    print(f"\n{'=' * 80}\nCSV: {path.relative_to(PROJECT_ROOT)}")
    chunks = pd.read_csv(path, chunksize=CHUNK_SIZE, na_values=["?"])
    total_rows = 0
    missing_counts = None
    dtypes = None
    sample = None
    for chunk in chunks:
        if sample is None:
            sample = chunk.head(5)
            dtypes = chunk.dtypes
            missing_counts = chunk.isna().sum()
        else:
            missing_counts += chunk.isna().sum()
        total_rows += len(chunk)
    if sample is None:
        print("The CSV has no data rows.")
        return
    print(f"Rows: {total_rows}")
    print(f"Columns: {list(sample.columns)}")
    print("\nInferred column types (from the first chunk):")
    print(dtypes)
    print("\nMissing values:")
    print(missing_counts[missing_counts > 0].to_string() or "None found")
    print("\nFirst five rows:")
    print(sample.to_string(index=False))
def inspect_parquet(path: Path) -> None:
    print(f"\n{'=' * 80}\nParquet: {path.relative_to(PROJECT_ROOT)}")
    parquet_file = ParquetFile(str(path))
    print(f"Rows: {parquet_file.count()}")
    print(f"Row groups: {len(parquet_file.row_groups)}")
    print("Columns:", parquet_file.columns)
    print("Inferred column types:")
    print(parquet_file.dtypes)
def main() -> None:
    if not DATASETS_DIR.exists():
        raise FileNotFoundError(f"Dataset folder not found: {DATASETS_DIR}")

    files = sorted(
        path for path in DATASETS_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".csv", ".parquet"}
    )

    if not files:
        print(f"No CSV or Parquet files found under {DATASETS_DIR}")
        return

    for path in files:
        if path.suffix.lower() == ".csv":
            inspect_csv(path)
        else:
            inspect_parquet(path)


if __name__ == "__main__":
    main()