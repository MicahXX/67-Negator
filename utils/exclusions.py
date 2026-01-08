import json
from pathlib import Path
from typing import Dict, Any

DATA_DIR = Path("/data")
EXCLUSIONS_FILE = DATA_DIR / "exclusions.json"

_EXCLUSIONS: Dict[str, Any] | None = None


def _ensure_loaded():
    global _EXCLUSIONS
    if _EXCLUSIONS is not None:
        return

    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        if EXCLUSIONS_FILE.exists():
            with EXCLUSIONS_FILE.open("r", encoding="utf-8") as f:
                _EXCLUSIONS = json.load(f)
        else:
            _EXCLUSIONS = {}

    except Exception as e:
        print("Failed to load exclusions:", e)
        _EXCLUSIONS = {}


def save_all() -> None:
    _ensure_loaded()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with EXCLUSIONS_FILE.open("w", encoding="utf-8") as f:
        json.dump(_EXCLUSIONS, f, indent=4)


def get_guild_data(guild_id: int) -> Dict[str, list]:
    _ensure_loaded()
    key = str(guild_id)
    if key not in _EXCLUSIONS:
        _EXCLUSIONS[key] = {"users": [], "channels": []}
        save_all()
    return _EXCLUSIONS[key]