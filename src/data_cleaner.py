"""DVF data cleaning rules for deliverable 1."""

import pandas as pd


class DataCleaner:
    """Clean DVF data and compute the price per square metre."""

    MIN_PRICE_M2 = 100
    MAX_PRICE_M2 = 20_000

    def __init__(self) -> None:
        # Keeps deduplication correct even when the CSV is read in chunks.
        self._seen_mutation_ids: set[str] = set()

    def clean(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Return a cleaned copy of one DVF chunk."""
        df = dataframe.copy()

        self._convert_types(df)

        # Transactions without a usable price or built surface cannot have
        # a meaningful price per square metre.
        df = df.dropna(subset=["valeur_fonciere", "surface_reelle_bati"])
        df = df[df["surface_reelle_bati"] > 0]

        df["prix_m2"] = df["valeur_fonciere"] / df["surface_reelle_bati"]
        df = df[
            df["prix_m2"].between(
                self.MIN_PRICE_M2,
                self.MAX_PRICE_M2,
                inclusive="both",
            )
        ]

        # Keep a single valid row per mutation, first inside the current
        # chunk, then against mutations already kept from previous chunks.
        df = df.drop_duplicates(subset=["id_mutation"], keep="first")
        df = df[~df["id_mutation"].isin(self._seen_mutation_ids)]
        self._seen_mutation_ids.update(
            df["id_mutation"].dropna().astype(str).tolist()
        )

        return df.reset_index(drop=True)

    @staticmethod
    def _convert_types(df: pd.DataFrame) -> None:
        """Convert the main DVF columns to appropriate pandas types."""
        df["date_mutation"] = pd.to_datetime(
            df["date_mutation"], errors="coerce"
        )

        numeric_columns = [
            "valeur_fonciere",
            "surface_reelle_bati",
            "nombre_pieces_principales",
            "longitude",
            "latitude",
        ]

        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors="coerce")
