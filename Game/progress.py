"""Shared save format, validation and atomic persistence."""
from copy import deepcopy
import json
import logging
import math
import os
from pathlib import Path
import tempfile

DEFAULT_PROGRESS = {
    "has_dash": False,
    "level": 1,
    "exp": 0,
    "coins": 0,
    "weapons_purchased": ["Basic Spell"],
    "pets_purchased": ["Dog"],
    "best_time": 0,
    "exp_required": 10,
    "max_health": 100,
}


DEFAULT_SETTINGS = {
    "music_volume": 0.2,
    "fullscreen": False,
    "window_size": [1280, 720],
}


def _read_document(path):
    try:
        with path.open(encoding="utf-8") as stream:
            data = json.load(stream)
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as error:
        logging.warning("Could not read progress from %s: %s", path, error)
        return {}


def _validated_settings(settings):
    result = deepcopy(DEFAULT_SETTINGS)
    if not isinstance(settings, dict):
        return result
    volume = settings.get("music_volume")
    if type(volume) in (int, float) and math.isfinite(volume) and 0 <= volume <= 1:
        result["music_volume"] = float(volume)
    if isinstance(settings.get("fullscreen"), bool):
        result["fullscreen"] = settings["fullscreen"]
    size = settings.get("window_size")
    if (isinstance(size, (list, tuple)) and len(size) == 2
            and all(type(value) is int for value in size)
            and 640 <= size[0] <= 7680 and 360 <= size[1] <= 4320):
        units = max(40, min(480, round(min(size[0] / 16, size[1] / 9))))
        result["window_size"] = [units * 16, units * 9]
    return result


def read_settings(path=None):
    path = Path(path) if path is not None else save_path()
    return _validated_settings(_read_document(path).get("settings", {}))


def save_settings(settings, path=None):
    """Update preferences without resetting upgrades or currency."""
    path = Path(path) if path is not None else save_path()
    data = _read_document(path)
    if not data:
        data = deepcopy(DEFAULT_PROGRESS)
    current = _validated_settings(data.get("settings", {}))
    current.update(settings)
    data["settings"] = _validated_settings(current)
    _write_document(data, path)


def save_path():
    root = Path(os.environ.get("APPDATA", Path.home())) if os.name == "nt" else Path.home()
    return root / ".hitorstand" / "player_progress.json"


def read_progress(path=None):
    """Accept older/incomplete saves without allowing invalid gameplay values."""
    path = Path(path) if path is not None else save_path()
    progress = deepcopy(DEFAULT_PROGRESS)
    saved = _read_document(path)
    for key, default in DEFAULT_PROGRESS.items():
        value = saved.get(key, default)
        if isinstance(default, bool):
            valid = isinstance(value, bool)
        elif isinstance(default, int):
            minimum = 1 if key in ("level", "exp_required", "max_health") else 0
            valid = type(value) is int and value >= minimum
        else:
            valid = isinstance(value, list) and all(isinstance(item, str) for item in value)
        if valid:
            progress[key] = value
    for key in ("weapons_purchased", "pets_purchased"):
        progress[key] = list(dict.fromkeys(DEFAULT_PROGRESS[key] + progress[key]))
    return progress


def write_progress(progress, path=None):
    """Replace saves atomically so an interrupted write cannot truncate progress."""
    path = Path(path) if path is not None else save_path()
    data = dict(progress)
    data["settings"] = read_settings(path)
    _write_document(data, path)


def _write_document(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=path.name, suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
