# paths.py
from pathlib import Path

# Anchor to this file's own location -- works locally (Spyder/VS Code)
# and on Streamlit Community Cloud, regardless of what folder the app
# was launched from.
ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "Data"
FIGURES_DIR = ROOT_DIR / "Figures"
IMAGES_DIR = ROOT_DIR / "images"
STATIC_DIR = ROOT_DIR / "static"