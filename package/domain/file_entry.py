"""Immutable description of a single filesystem entry considered for renaming."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileEntry:
    """A filesystem item (file or folder) enumerated by the scanner.

    ``extension_label`` is the value used both for display in the UI table and
    for filter matching against common/specific extension lists. It follows the
    original app's convention: real files carry their ``.ext``, files with no
    extension carry ``"Undefined"``, and folders carry the translated word for
    "Folder".
    """

    name: str
    stem: str
    extension: str
    extension_label: str
    is_folder: bool
    directory: Path
    size_bytes: int | None

    @property
    def full_path(self) -> Path:
        return self.directory / self.name

    @property
    def has_real_extension(self) -> bool:
        """True when ``extension`` is an actual ``.ext`` suffix on a file."""
        return bool(self.extension) and self.extension.startswith(".") and not self.is_folder
