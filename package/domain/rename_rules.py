"""Rename rule strategies and their registry.

Each rule consumes a sequence of :class:`FileEntry` objects plus a
:class:`RenameContext` and emits a preview list of new names (empty string
means "no change"). Rules do not mutate the filesystem; they only compute
what the new names would be.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import ClassVar

from package.domain.file_entry import FileEntry
from package.domain.filters import AllFilter, FileTypeFilter


@dataclass(frozen=True)
class RenameContext:
    """All user-tunable parameters required to compute a rename preview."""

    find: str = ""
    replace: str = ""
    case_sensitive: bool = True
    regex: bool = False
    position_after: bool = False
    sequential_start: int = 1
    sequential_count: int = 1
    filter_: FileTypeFilter = field(default_factory=AllFilter)


@dataclass
class PreviewResult:
    """Outcome of computing a preview for a list of entries.

    ``new_names[i]`` corresponds to ``entries[i]``. An empty string indicates
    the entry is not renamed (filter rejected it, or the rule does not apply).
    """

    new_names: list[str]
    error_message: str | None = None


class RenameRule(ABC):
    """Strategy that transforms a list of entries into a list of new names."""

    rule_id: ClassVar[str]

    @abstractmethod
    def preview(
        self,
        entries: Sequence[FileEntry],
        context: RenameContext,
    ) -> PreviewResult:
        """Return the new name for each entry (``""`` when unchanged)."""

    @staticmethod
    def _extension_for_output(entry: FileEntry) -> str:
        """The extension suffix to append when rebuilding a file name.

        Folders and extension-less files contribute no suffix, matching the
        behaviour of the original implementation.
        """
        return entry.extension if entry.has_real_extension else ""


class AddTextRule(RenameRule):
    """Prefix (or suffix) every matching file name with a fixed string."""

    rule_id: ClassVar[str] = "add"

    def preview(
        self,
        entries: Sequence[FileEntry],
        context: RenameContext,
    ) -> PreviewResult:
        replace_value = context.replace
        names: list[str] = []
        for entry in entries:
            if not context.filter_.matches(entry):
                names.append("")
                continue
            ext = self._extension_for_output(entry)
            if context.position_after:
                names.append(f"{entry.stem}{replace_value}{ext}")
            else:
                names.append(f"{replace_value}{entry.stem}{ext}")
        return PreviewResult(new_names=names)


class ReplaceTextRule(RenameRule):
    """Replace a substring or regex match within matching file stems."""

    rule_id: ClassVar[str] = "replace"

    def preview(
        self,
        entries: Sequence[FileEntry],
        context: RenameContext,
    ) -> PreviewResult:
        find = context.find if context.case_sensitive else context.find.casefold()
        replace = context.replace
        if not find:
            return PreviewResult(new_names=["" for _ in entries])

        names: list[str] = [""] * len(entries)
        error_message: str | None = None
        if context.regex:
            for index, entry in enumerate(entries):
                if not context.filter_.matches(entry):
                    continue
                ext = self._extension_for_output(entry)
                try:
                    new_stem = re.sub(find, replace, entry.stem)
                except re.error:
                    error_message = "Invalid expression"
                    continue
                names[index] = f"{new_stem}{ext}"
        else:
            # Mirror the legacy behaviour: when case-insensitive is enabled
            # the FIND value is casefolded (but the stem is not), and that
            # casefolded value is used both for membership testing and for
            # ``str.replace``. This has the quirk that upper-case characters
            # in the stem never match — preserved verbatim for compatibility.
            for index, entry in enumerate(entries):
                if not context.filter_.matches(entry):
                    continue
                if find not in entry.stem:
                    continue
                ext = self._extension_for_output(entry)
                names[index] = f"{entry.stem.replace(find, replace)}{ext}"
        return PreviewResult(new_names=names, error_message=error_message)


class ReplaceExtensionRule(RenameRule):
    """Replace the file extension of matching files (folders are skipped)."""

    rule_id: ClassVar[str] = "replace_extension"

    def preview(
        self,
        entries: Sequence[FileEntry],
        context: RenameContext,
    ) -> PreviewResult:
        replace_value = context.replace
        if not replace_value:
            return PreviewResult(new_names=["" for _ in entries])
        names: list[str] = []
        for entry in entries:
            # Folders and extension-less entries are ignored: preserving the
            # original behaviour of "extension[0] != '.'" guard.
            if not entry.extension_label.startswith(".") or not context.filter_.matches(entry):
                names.append("")
                continue
            names.append(f"{entry.stem}.{replace_value}")
        return PreviewResult(new_names=names)


class SequentialRule(RenameRule):
    """Number matching files using an arithmetic progression."""

    rule_id: ClassVar[str] = "sequential"

    def preview(
        self,
        entries: Sequence[FileEntry],
        context: RenameContext,
    ) -> PreviewResult:
        replace_value = context.replace
        current = context.sequential_start
        step = context.sequential_count
        names: list[str] = []
        for entry in entries:
            if not context.filter_.matches(entry):
                names.append("")
                continue
            ext = self._extension_for_output(entry)
            if context.position_after:
                names.append(f"{entry.stem}{replace_value}({current}){ext}")
            else:
                names.append(f"({current}){replace_value}{entry.stem}{ext}")
            current += step
        return PreviewResult(new_names=names)


class RuleRegistry:
    """Factory returning a fresh rule instance by its string id.

    Using a class-level registry keeps the rule lookup a single source of
    truth and lets new rules be added without touching the view layer.
    """

    _rules: ClassVar[dict[str, type[RenameRule]]] = {
        AddTextRule.rule_id: AddTextRule,
        ReplaceTextRule.rule_id: ReplaceTextRule,
        ReplaceExtensionRule.rule_id: ReplaceExtensionRule,
        SequentialRule.rule_id: SequentialRule,
    }

    @classmethod
    def create(cls, rule_id: str) -> RenameRule:
        try:
            return cls._rules[rule_id]()
        except KeyError as exc:
            raise ValueError(f"Unknown rename rule: {rule_id!r}") from exc

    @classmethod
    def ids(cls) -> tuple[str, ...]:
        return tuple(cls._rules.keys())
