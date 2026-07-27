"""Configuration helpers for local synthetic compliance experiments."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np


def set_seed(seed: int) -> None:
    """Set deterministic random seeds for reproducible synthetic experiments."""
    random.seed(seed)
    np.random.seed(seed)


def ensure_output_dirs(output_dir: str | Path = "outputs") -> dict[str, Path]:
    """Create standard output folders and return their paths."""
    root = Path(output_dir)
    paths = {
        "root": root,
        "results": root / "results",
        "reports": root / "reports",
        "figures": root / "figures",
        "audit": root / "audit",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths
