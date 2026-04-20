"""Coordinates the scanner, rule preview, backup and rename services.

The controller owns no Qt widgets itself but talks to the main window through
collaborators (``FileTablePresenter``, ``ProgressStatus``, ``WarningBox``) and
through small callbacks for translations. This keeps view code thin and the
business flow testable in isolation from Qt.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from package.domain.rename_rules import PreviewResult, RenameContext, RuleRegistry
from package.services.backup_service import BackupService
from package.services.file_scanner import FileScanner, ScanOptions
from package.services.rename_service import RenamePlan, RenameService
from package.views.file_table_presenter import FileTablePresenter
from package.views.message_boxes import WarningBox, SuccessBox
from package.views.progress_status import ProgressStatus

Translator = Callable[[str], str]


@dataclass(frozen=True)
class LoadOutcome:
    """How many files/folders were discovered during the last scan."""

    files: int
    folders: int


class RenameController:
    """Orchestrates the scan → preview → (backup →) rename pipeline."""

    def __init__(
        self,
        scanner: FileScanner,
        rename_service: RenameService,
        backup_service: BackupService,
        table: FileTablePresenter,
        progress: ProgressStatus,
        warning_box: WarningBox,
        success_box: SuccessBox,
        translate: Translator,
    ) -> None:
        self._scanner = scanner
        self._rename_service = rename_service
        self._backup_service = backup_service
        self._table = table
        self._progress = progress
        self._warning = warning_box
        self._success = success_box
        self._translate = translate

    def load_directory(self, path: Path, options: ScanOptions) -> LoadOutcome | None:
        """Scan ``path`` and populate the table. ``None`` on I/O error."""
        self._table.clear()
        self._progress.reset(self._translate("Nothing to load"))

        self._progress.set_message(self._translate("Wait, checking files..."))
        try:
            total = self._scanner.count(path, options)
        except OSError as exc:
            self._warning.show(f"ERROR 0x0001: {exc}", default_button=True)
            return None

        if total <= 0:
            self._progress.set_message(self._translate("Nothing to load"))
            return LoadOutcome(files=0, folders=0)

        self._progress.set_maximum(total)
        self._progress.set_message(self._translate("Loading files..."))

        files = 0
        folders = 0
        try:
            entries = []
            for entry in self._scanner.scan(
                path, options, on_progress=lambda: self._progress.advance()
            ):
                entries.append(entry)
                if entry.is_folder:
                    folders += 1
                else:
                    files += 1
            self._table.load(entries)
        except OSError as exc:
            self._warning.show(f"ERROR 0x0002: {exc}", default_button=True)
            return None

        self._progress.set_message(
            self._translate("Total Files: {}, Total Folders: {}").format(files, folders)
        )
        return LoadOutcome(files=files, folders=folders)

    def compute_preview(self, rule_id: str, context: RenameContext) -> PreviewResult:
        """Run the selected rule and write the new-name column."""
        rule = RuleRegistry.create(rule_id)
        entries = self._table.entries()
        result = rule.preview(entries, context)
        self._table.set_new_names(result.new_names)
        return result

    def run_backup(self, source: Path, options: ScanOptions) -> bool:
        """Zip ``source`` before renaming. Returns False if the archive failed."""
        self._progress.reset()
        self._progress.set_message(self._translate("Creating backup..."))
        backup_path = self._backup_service.create_backup(
            source=source,
            options=options,
            on_progress=lambda: self._progress.advance(),
        )
        if backup_path is None:
            self._progress.set_label(self._translate("Error creating backup"))
            return False
        self._progress.set_label(self._translate("Backup created"))
        return True

    def execute_rename(self) -> bool:
        """Apply previewed renames; returns True if anything ran to completion."""
        entries = self._table.entries()
        row_count = self._table.row_count()
        if row_count <= 0:
            self._progress.set_message(self._translate("No files to rename"))
            return False

        self._progress.reset()
        self._progress.set_label(self._translate("Renaming files..."))
        self._progress.set_maximum(row_count)

        plans = [
            RenamePlan(
                directory=entry.directory,
                old_name=entry.name,
                new_name=self._table.read_new_name(row),
            )
            for row, entry in enumerate(entries)
        ]
        outcome = self._rename_service.execute(
            plans,
            on_progress=lambda: self._progress.advance(),
        )
        if outcome.error is not None:
            self._warning.show(f"ERROR 0x0003: {outcome.error}", default_button=True)
            return False

        self._success.show(
            self._translate("Files renamed successfully"),
            self._translate("{} files renamed").format(outcome.renamed_count),
        )
        return True
