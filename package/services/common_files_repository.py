"""Loads the curated "common file types" table from CSV using pandas."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class CommonFileGroup:
    """A row from ``common_file_types.csv``.

    ``extensions`` is the raw space-separated string as stored in the CSV
    (e.g. ``".mp3 .ogg .wav"``). Splitting on space mirrors the original app.
    """

    name: str
    extensions: str

    def extension_tokens(self) -> list[str]:
        """Return individual extension tokens (``.mp3``, ``.ogg``…)."""
        return self.extensions.split(" ")

    def display_pattern(self) -> str:
        """Filter pattern for the UI list (``*.mp3;*.ogg;*.wav``)."""
        return self.extensions.replace(" ", ";*")


class CommonFilesRepository:
    """Caches the parsed CSV so pandas only reads it once per session."""

    DEFAULT_CSV_PATH: Path = Path("db/common_file_types.csv")

    def __init__(self, csv_path: Path | str | None = None) -> None:
        self._csv_path: Path = Path(csv_path) if csv_path is not None else self.DEFAULT_CSV_PATH
        self._groups: list[CommonFileGroup] | None = None

    def groups(self) -> list[CommonFileGroup]:
        """Return the list of groups, loading lazily on first access."""
        if self._groups is None:
            data = pd.read_csv(self._csv_path)
            names: list[str] = data["File_Name"].tolist()
            extensions: list[str] = data["File_Extensions"].tolist()
            self._groups = [
                CommonFileGroup(name=name, extensions=exts)
                for name, exts in zip(names, extensions, strict=True)
            ]
        return self._groups
