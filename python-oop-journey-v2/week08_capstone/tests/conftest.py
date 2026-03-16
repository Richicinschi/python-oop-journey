"""Pytest configuration for Week 8 Capstone tests."""

from __future__ import annotations

import sys
from pathlib import Path

# Add the week08_capstone directory to the path so imports work
WEEK08_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(WEEK08_DIR))
