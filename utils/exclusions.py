import json
from pathlib import Path
from typing import Dict, Any

EXCLUSIONS_FILE = Path("exclusions.json")

_EXCLUSIONS: Dict[str, Any] | None = None


def _ensure_loaded():
    global _EXCLUSIONS
    if _EXCLUSIONS is None:
        if EXCLUSIONS_FILE.exists():
            with EXCLUSIONS_FILE.open("r", encoding="utf-8") as f:
                _EXCLUSIONS = json.load(f)
        else:
            _EXCLUSIONS = {}


def get_all() -> Dict[str, Any]:
    _ensure_loaded()
    return _EXCLUSIONS


def save_all() -> None:
    _ensure_loaded()
    with EXCLUSIONS_FILE.open("w", encoding="utf-8") as f:
        json.dump(_EXCLUSIONS, f, indent=4)


def get_guild_data(guild_id: int) -> Dict[str, list]:
    _ensure_loaded()
    key = str(guild_id)
    if key not in _EXCLUSIONS:
        _EXCLUSIONS[key] = {"users": [], "channels": []}
    return _EXCLUSIONS[key]