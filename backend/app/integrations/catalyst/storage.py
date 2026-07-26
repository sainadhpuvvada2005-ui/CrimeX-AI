import shutil
from pathlib import Path
from typing import BinaryIO


class CatalystStratus:
    """A local fallback implementation for Catalyst Stratus file storage."""

    def __init__(self, storage_root: str | None = None) -> None:
        self.storage_root = Path(storage_root or Path(__file__).resolve().parents[2] / ".stratus")
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def upload(self, destination: str, file_obj: BinaryIO) -> str:
        destination_path = self.storage_root / destination
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        with destination_path.open("wb") as handle:
            shutil.copyfileobj(file_obj, handle)
        return str(destination_path)

    def download(self, source: str) -> bytes:
        source_path = self.storage_root / source
        return source_path.read_bytes() if source_path.exists() else b""

    def exists(self, source: str) -> bool:
        return (self.storage_root / source).exists()
