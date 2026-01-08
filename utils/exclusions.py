import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

EXCLUSIONS_FILE = DATA_DIR / "exclusions.json"

_EXCLUSIONS: Dict[str, Any] | None = None


def _ensure_loaded():
    global _EXCLUSIONS
    if _EXCLUSIONS is None:
        if EXCLUSIONS_FILE.exists():
            try:
                with EXCLUSIONS_FILE.open("r", encoding="utf-8") as f:
                    _EXCLUSIONS = json.load(f)
            except json.JSONDecodeError:
                _EXCLUSIONS = {}
        else:
            _EXCLUSIONS = {}