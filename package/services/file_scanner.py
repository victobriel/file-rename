"""Walks a directory tree and yields :class:`FileEntry` objects.

The scanner respects the same ignore rules as the original implementation:
hidden files/folders (dot-prefixed or with the Windows hidden attribute set),
ignored repo-style folders (``.git``, ``node_modules``…), and a small block
list of "noise" file names (``README.md``, ``config.ini``…).
"""
from __future__ import annotations

import os
import stat
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path

from package.domain.file_entry import FileEntry

# The label provider is given (extension, is_folder) and returns the label
# used both for the file-type filter and the UI table's extension column.
LabelProvider = Callable[[str, bool], str]
ProgressCallback = Callable[[], None]


@dataclass(frozen=True)
class ScanOptions:
    """All toggles affecting which paths are walked."""

    include_subdirectories: bool = False
    include_folders: bool = False
    ignored_paths: tuple[str, ...] = field(
        default=(".git", ".vscode", ".idea", "__pycache__", "venv", "node_modules"),
    )
    ignored_files: tuple[str, ...] = field(
        default=("README.md", "README.rst", "LICENSE", "config.ini", "requirements.txt"),
    )


class FileScanner:
    """Iterates a directory producing domain :class:`FileEntry` objects.

    The scanner is I/O-heavy; ``count`` and ``scan`` both walk the same
    directory tree because the original UI needs to know a total up front to
    size its progress bar.
    """

    def __init__(self, label_provider: LabelProvider) -> None:
        self._label_provider = label_provider

    @staticmethod
    def _has_hidden_attribute(path: Path) -> bool:
        if os.name != "nt":
            return False
        try:
            return bool(path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)  # type: ignore[attr-defined]
        except OSError:
            return False

    def _is_ignored_root(self, root: Path, options: ScanOptions) -> bool:
        root_str = str(root)
        return any(ignored in root_str for ignored in options.ignored_paths)

    def _visible_dirs(self, root: Path, dirs: list[str]) -> list[str]:
        return [
            directory
            for directory in dirs
            if not directory.startswith(".")
            and not self._has_hidden_attribute(root / directory)
        ]

    def _visible_files(self, root: Path, files: list[str], options: ScanOptions) -> list[str]:
        return [
            file
            for file in files
            if not file.startswith(".")
            and not self._has_hidden_attribute(root / file)
            and file not in options.ignored_files
        ]

    def count(self, base: Path, options: ScanOptions) -> int:
        """Return the number of entries ``scan`` would yield for the same inputs."""
        total = 0
        for raw_root, dirs, files in os.walk(base):
            root = Path(raw_root)
            if not options.include_subdirectories and root != base:
                continue
            if self._is_ignored_root(root, options):
                continue
            dirs[:] = self._visible_dirs(root, dirs)
            if options.include_folders:
                total += len(dirs)
            files[:] = self._visible_files(root, files, options)
            total += len(files)
        return total

    def scan(
        self,
        base: Path,
        options: ScanOptions,
        on_progress: ProgressCallback | None = None,
    ) -> Iterator[FileEntry]:
        """Yield :class:`FileEntry` objects for every visible entry under ``base``."""
        for raw_root, dirs, files in os.walk(base):
            root = Path(raw_root)
            if not options.include_subdirectories and root != base:
                continue
            if self._is_ignored_root(root, options):
                continue
            dirs[:] = self._visible_dirs(root, dirs)
            if options.include_folders:
                for directory in dirs:
                    yield self._build_entry(directory, root, is_folder=True)
                    if on_progress is not None:
                        on_progress()
            files[:] = self._visible_files(root, files, options)
            for file in files:
                yield self._build_entry(file, root, is_folder=False)
                if on_progress is not None:
                    on_progress()

    def _build_entry(self, name: str, root: Path, *, is_folder: bool) -> FileEntry:
        if is_folder:
            stem = name
            extension = ""
        else:
            stem, extension = os.path.splitext(name)
        label = self._label_provider(extension, is_folder)
        size: int | None
        if is_folder:
            size = None
        else:
            try:
                size = (root / name).stat().st_size
            except OSError:
                size = 0
        return FileEntry(
            name=name,
            stem=stem,
            extension=extension,
            extension_label=label,
            is_folder=is_folder,
            directory=root,
            size_bytes=size,
        )
