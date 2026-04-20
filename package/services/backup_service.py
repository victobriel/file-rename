"""Creates ZIP backups of a directory tree before renames are executed."""
from __future__ import annotations

import datetime
import os
import zipfile
from collections.abc import Callable
from pathlib import Path

from package.services.file_scanner import ScanOptions

ProgressCallback = Callable[[], None]


class BackupService:
    """Zips a directory tree into ``Backup_<timestamp>.zip`` in the cwd.

    The archive honours the same ``include_subdirectories``/ignored-paths
    rules as the scanner so that "what was listed" and "what was backed up"
    stay in sync.
    """

    def create_backup(
        self,
        source: Path,
        options: ScanOptions,
        on_progress: ProgressCallback | None = None,
        output_directory: Path | None = None,
        now: datetime.datetime | None = None,
    ) -> Path | None:
        """Build the backup archive.

        Returns the archive path on success, ``None`` if the zip did not
        materialise (e.g. an I/O error silently prevented writes).
        """
        moment = now or datetime.datetime.now()
        date_format = moment.strftime("%Y-%d-%m-%H-%M")
        # Preserves the original output file name, including the duplicated
        # ".zip" suffix used by the legacy code — callers relying on globbing
        # for "Backup_*.zip" will still find it.
        backup_name = f"Backup_{date_format}.zip.zip"
        base_dir = output_directory or Path.cwd()
        backup_path = base_dir / backup_name

        with zipfile.ZipFile(backup_path, "a") as archive:
            for raw_root, dirs, files in os.walk(source):
                root = Path(raw_root)
                if not options.include_subdirectories and root != source:
                    continue
                if any(ignored in str(root) for ignored in options.ignored_paths):
                    continue
                dirs[:] = [
                    directory
                    for directory in dirs
                    if not directory.startswith(".")
                    and not self._is_hidden(root / directory)
                ]
                for file in files:
                    if file in options.ignored_files:
                        continue
                    if file.startswith(".") or self._is_hidden(root / file):
                        continue
                    archive.write(root / file)
                    if on_progress is not None:
                        on_progress()

        if not backup_path.exists():
            return None
        return backup_path

    @staticmethod
    def _is_hidden(path: Path) -> bool:
        if os.name != "nt":
            return False
        import stat

        try:
            return bool(path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)  # type: ignore[attr-defined]
        except OSError:
            return False
