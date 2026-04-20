"""Predicates that decide whether a :class:`FileEntry` participates in renaming."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from package.domain.file_entry import FileEntry


class FileTypeFilter(ABC):
    """Strategy that accepts or rejects a file entry based on its type."""

    @abstractmethod
    def matches(self, entry: FileEntry) -> bool:
        """Return True when the entry should be considered for renaming."""


class AllFilter(FileTypeFilter):
    """Accepts every file and folder."""

    def matches(self, entry: FileEntry) -> bool:
        return True


class _ExtensionLabelFilter(FileTypeFilter):
    """Accepts entries whose ``extension_label`` is in the allowed set."""

    def __init__(self, allowed_labels: Iterable[str]) -> None:
        self._allowed: frozenset[str] = frozenset(allowed_labels)

    def matches(self, entry: FileEntry) -> bool:
        return entry.extension_label in self._allowed


class CommonExtensionsFilter(_ExtensionLabelFilter):
    """Accepts entries matching the curated "common file types" list."""


class SpecificExtensionsFilter(_ExtensionLabelFilter):
    """Accepts entries matching the user-provided specific extensions list."""
