from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"

REPORT_DIR = ROOT / "reports"

IMAGE_DIR = DATA_DIR / "images"

RUBRIC = ROOT / "rubrics" / "annotation_rubric.json"
