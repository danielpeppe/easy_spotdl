import sys
from pathlib import Path
import yaml


def load_config(yaml_section: str, config_path: str | Path = "config.yaml") -> dict:
    """Return the specified section of config.yaml (or exit on error)."""
    cfg_path = Path(config_path)
    if not cfg_path.exists():
        sys.exit(f"[ERROR] Config file not found: {config_path}")
    with cfg_path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data.get(yaml_section, {})