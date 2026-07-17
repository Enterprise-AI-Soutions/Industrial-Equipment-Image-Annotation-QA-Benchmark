"""
conftest.py — Makes the project root importable when running pytest from any directory.
This ensures 'import src.xxx' works correctly.
"""
import sys
from pathlib import Path

# Add the project root to sys.path so 'src' is always importable
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
