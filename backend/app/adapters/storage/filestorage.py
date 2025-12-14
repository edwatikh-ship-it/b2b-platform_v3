from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StoredFile:
    storage_key: str
    sha256: str
    size_bytes: int


class LocalAttachmentStorage:
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir

    def _ensure_dir(self) -> None:
        self._base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, original_filename: str, content: bytes) -> StoredFile:
        self._ensure_dir()
        sha = hashlib.sha256(content).hexdigest()
        size = len(content)
        # deterministic-ish name; ok for MVP
        safe_name = original_filename.replace("\\", "_").replace("/", "_")
        storage_key = f"{sha}_{safe_name}"
        path = self._base_dir / storage_key
        path.write_bytes(content)
        return StoredFile(storage_key=storage_key, sha256=sha, size_bytes=size)

    def read(self, storage_key: str) -> bytes:
        path = self._base_dir / storage_key
        return path.read_bytes()
