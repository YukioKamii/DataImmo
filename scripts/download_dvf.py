"""Download one Geo-DVF departmental CSV file without adding it to Git."""

import argparse
from pathlib import Path
from urllib.request import urlopen


BASE_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Télécharge un fichier Geo-DVF départemental."
    )
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument(
        "--department",
        required=True,
        help="Code département, par ex. 59, 75, 2A ou 971",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    department = str(args.department).upper()

    url = f"{BASE_URL}/{args.year}/departements/{department}.csv.gz"
    output_dir = Path("data/raw") / str(args.year)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{department}.csv.gz"

    print(f"Téléchargement : {url}")

    with urlopen(url) as response, output_path.open("wb") as destination:
        while chunk := response.read(1024 * 1024):
            destination.write(chunk)

    print(f"Fichier enregistré : {output_path}")


if __name__ == "__main__":
    main()
