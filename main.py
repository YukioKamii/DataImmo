"""Entry point for DataImmo deliverable 1."""

import argparse
from pathlib import Path

import pandas as pd

from src.data_cleaner import DataCleaner
from src.data_exporter import DataExporter
from src.data_loader import DataLoader


def memory_mb(dataframe: pd.DataFrame) -> float:
    """Return the deep memory footprint of a DataFrame in MiB."""
    bytes_used = dataframe.memory_usage(deep=True).sum()
    return bytes_used / (1024**2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ingestion et nettoyage d'un fichier DVF départemental."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Chemin du fichier DVF .csv ou .csv.gz",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Chemin du fichier Parquet de sortie",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=100_000,
        help="Nombre de lignes lues par chunk (défaut : 100000)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    loader = DataLoader(args.input, chunk_size=args.chunk_size)
    cleaner = DataCleaner()
    exporter = DataExporter(args.output)

    cleaned_chunks: list[pd.DataFrame] = []
    rows_before = 0
    peak_raw_chunk_memory = 0.0

    for chunk in loader.load():
        rows_before += len(chunk)
        peak_raw_chunk_memory = max(
            peak_raw_chunk_memory,
            memory_mb(chunk),
        )
        cleaned_chunks.append(cleaner.clean(chunk))

    if not cleaned_chunks:
        raise ValueError("Le fichier source ne contient aucune donnée.")

    cleaned_df = pd.concat(cleaned_chunks, ignore_index=True)
    output_path = exporter.export(cleaned_df)

    rows_after = len(cleaned_df)
    removed_rows = rows_before - rows_after

    print("\n=== Rapport DataImmo - Livrable 1 ===")
    print(f"Fichier source          : {Path(args.input)}")
    print(f"Lignes avant nettoyage  : {rows_before:,}")
    print(f"Lignes après nettoyage  : {rows_after:,}")
    print(f"Lignes supprimées       : {removed_rows:,}")
    print(f"Mémoire max d'un chunk  : {peak_raw_chunk_memory:.2f} MiB")
    print(f"Mémoire données propres : {memory_mb(cleaned_df):.2f} MiB")
    print(f"Parquet généré          : {output_path}")


if __name__ == "__main__":
    main()
