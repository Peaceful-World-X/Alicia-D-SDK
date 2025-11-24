import json
import time
from pathlib import Path
from typing import Dict, List, Optional

from .logger import logger


class ZeroOffsetManager:
    """Manage persistent joint zero offsets for Alicia-D arms."""

    def __init__(self, base_dir: Optional[Path] = None):
        if base_dir is None:
            base_dir = Path.home() / ".config" / "alicia_d"
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.base_dir / "zero_offsets.json"
        self._cache: Dict[str, Dict] = {}
        self._load()

    def _load(self) -> None:
        if not self.file_path.exists():
            self._cache = {}
            return
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                self._cache = json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning(f"零点偏移文件损坏，已忽略: {exc}")
            self._cache = {}

    def _flush(self) -> None:
        try:
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=2)
        except OSError as exc:
            logger.error(f"无法写入零点偏移文件: {exc}")

    def load(self, robot_id: str) -> Optional[List[float]]:
        record = self._cache.get(robot_id)
        if not record:
            return None
        offsets = record.get("offsets")
        if offsets and len(offsets) == 6:
            return [float(x) for x in offsets]
        return None

    def save(self, robot_id: str, offsets: List[float], metadata: Optional[Dict] = None) -> None:
        self._cache[robot_id] = {
            "offsets": [float(x) for x in offsets],
            "timestamp": time.time(),
            "metadata": metadata or {}
        }
        self._flush()

    def list_all(self) -> Dict[str, Dict]:
        return self._cache.copy()
