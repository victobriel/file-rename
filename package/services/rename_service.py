"""Executes planned rename operations against the filesystem."""
from __future__ import annotations

import os
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

ProgressCallback = Callable[[], None]


@dataclass(frozen=True)
class RenamePlan:
    """Single rename operation: move ``directory/old_name`` to ``directory/new_name``."""

    directory: Path
    old_name: str
    new_name: str

    @property
    def source(self) -> Path:
        return self.directory / self.old_name

    @property
    def target(self) -> Path:
        return self.directory / self.new_name


@dataclass
class RenameOutcome:
    """Result of attempting a batch of renames."""

    renamed_count: int
    error: str | None = None


class RenameService:
    """Runs a list of :class:`RenamePlan` operations, reporting progress.

    Aborts on the first OS error so the caller can surface a warning — this
    preserves the behaviour of the original ``rename_run`` method which
    stopped the loop as soon as ``os.rename`` raised.
    """

    def execute(
        self,
        plans: Iterable[RenamePlan],
        on_progress: ProgressCallback | None = None,
    ) -> RenameOutcome:
        renamed = 0
        for plan in plans:
            if not plan.new_name:
                if on_progress is not None:
                    on_progress()
                continue
            try:
                os.rename(plan.source, plan.target)
            except OSError as exc:
                return RenameOutcome(renamed_count=renamed, error=str(exc))
            renamed += 1
            if on_progress is not None:
                on_progress()
        return RenameOutcome(renamed_count=renamed)
