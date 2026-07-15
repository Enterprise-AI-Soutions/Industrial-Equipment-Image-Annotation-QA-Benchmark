"""
Common helper functions.
"""

from pathlib import Path
import json
import pandas as pd


def ensure_directory(directory: Path) -> None:
    """
    Create directory if it does not exist.
    """

    directory.mkdir(parents=True, exist_ok=True)


def load_json(file_path: Path):

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, file_path: Path):

    ensure_directory(file_path.parent)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_csv(file_path: Path):

    return pd.read_csv(file_path)


def save_csv(df, file_path: Path):

    ensure_directory(file_path.parent)

    df.to_csv(file_path, index=False)


def percentage(value, total):

    if total == 0:
        return 0

    return round((value / total) * 100, 2)


def round_score(value):

    return round(float(value), 3)
