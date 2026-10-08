"""Script to download real Canadian forestry/canopy data from Ville de Montréal / Données Québec."""

from pathlib import Path
import requests

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Montréal Canopy 2019 Open Data GeoJSON
CANOPY_URL = (
    "https://donnees.montreal.ca/fr/dataset/36f48854-474b-43d2-a16d-a433da8a1447/resource/"
    "77e44cc1-56b1-4e83-871d-e3990565563f/download/canopee-2019.zip"
)

DEST_ZIP = DATA_DIR / "canopee_2019.zip"


def download():
    print(f"📥 Downloading Montreal Urban Canopy Layer (Canopée 2019)...")
    print(f"URL: {CANOPY_URL}")
    try:
        r = requests.get(CANOPY_URL, stream=True, timeout=120)
        r.raise_for_status()
        with open(DEST_ZIP, "wb") as f:
            for chunk in r.iter_content(chunk_size=16384):
                f.write(chunk)
        print(f"✅ Downloaded to {DEST_ZIP} ({DEST_ZIP.stat().st_size / (1024*1024):.2f} MB)")
    except Exception as e:
        print(f"⚠️ Direct download failed: {e}")
        print("Note: Access dataset manually at https://donnees.montreal.ca/dataset/canopee")


if __name__ == "__main__":
    download()
