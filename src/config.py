"""
Global configuration for the benchmark.
"""

from pathlib import Path

# -------------------------------------------------------
# Root directories
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
IMAGE_DIR = DATA_DIR / "images"
ANNOTATION_DIR = DATA_DIR / "annotations"

REPORT_DIR = PROJECT_ROOT / "reports"

# -------------------------------------------------------
# Thresholds
# -------------------------------------------------------

IOU_THRESHOLD = 0.50

QUALITY_PASS_SCORE = 0.80

REVIEW_QUEUE_THRESHOLD = 0.70

# -------------------------------------------------------
# Supported classes
# -------------------------------------------------------

VALID_CLASSES = {

    "pump",
    "motor",
    "valve",
    "bearing",
    "compressor",
    "gearbox",
    "generator",
    "turbine",
    "conveyor",
    "pipeline",
    "heat exchanger",
    "heat_exchanger",
    "electrical panel",
    "electrical_panel",

}

# -------------------------------------------------------
# Default report names
# -------------------------------------------------------

ANNOTATION_REPORT = REPORT_DIR / "annotation_report.md"

REVIEW_QUEUE = REPORT_DIR / "review_queue.csv"

AGREEMENT_REPORT = REPORT_DIR / "agreement_summary.csv"
