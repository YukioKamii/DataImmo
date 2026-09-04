"""DVF data export utilities."""

from pathlib import Path

import pandas as pd


class DataExporter:
    """Export cleaned DataFrames to Parquet."""

    def __init__(self, output_path: str | Path) -> None:
        self.output_path = Path(output_path)

    def export(self, dataframe: pd.DataFrame) -> Path:
        """Save a DataFrame as a compressed Parquet file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        dataframe.to_parquet(
            self.output_path,
            engine="pyarrow",
            compression="snappy",
            index=False,
        )
        return self.output_path
