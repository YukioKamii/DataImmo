"""DVF data loading utilities."""

from collections.abc import Iterator
from pathlib import Path

import pandas as pd


class DataLoader:
    """Load a DVF CSV file, compressed or not, by chunks."""

    STRING_COLUMNS = {
        "id_mutation": "string",
        "code_postal": "string",
        "code_commune": "string",
        "nom_commune": "string",
        "code_departement": "string",
        "type_local": "string",
    }

    def __init__(self, file_path: str | Path, chunk_size: int = 100_000) -> None:
        self.file_path = Path(file_path)
        self.chunk_size = chunk_size

    def load(self) -> Iterator[pd.DataFrame]:
        """Yield the source file as pandas DataFrame chunks.

        Pandas' ``compression='infer'`` handles both regular ``.csv`` files
        and compressed files such as ``.csv.gz`` from their extension.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Fichier DVF introuvable : {self.file_path}"
            )

        return pd.read_csv(
            self.file_path,
            chunksize=self.chunk_size,
            compression="infer",
            dtype=self.STRING_COLUMNS,
            low_memory=False,
        )
