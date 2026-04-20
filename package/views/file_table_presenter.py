"""Adapter between domain entries and the Qt ``QTableWidget`` showing them.

All reads and writes of the five-column file table go through this class so
the rest of the presentation code never has to call ``item(row, col).text()``
directly.
"""
from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

from PySide6 import QtGui, QtWidgets

from package.domain.file_entry import FileEntry

Translator = Callable[[str], str]

COL_NAME = 0
COL_NEW_NAME = 1
COL_EXTENSION = 2
COL_PATH = 3
COL_SIZE = 4


class FileTablePresenter:
    """Wraps the ``filesList`` :class:`QTableWidget` used on the main window."""

    _HIGHLIGHT_COLOR = QtGui.QColor(174, 214, 241)
    _CLEAR_COLOR = QtGui.QColor(255, 255, 255)

    def __init__(self, table: QtWidgets.QTableWidget, translate: Translator) -> None:
        self._table = table
        self._translate = translate
        self._entries: list[FileEntry] = []

    def clear(self) -> None:
        self._table.setRowCount(0)
        self._entries.clear()

    def load(self, entries: Iterable[FileEntry]) -> None:
        """Replace the table contents with the given entries."""
        self.clear()
        for entry in entries:
            self._append_row(entry)

    def _append_row(self, entry: FileEntry) -> None:
        row = self._table.rowCount()
        self._table.insertRow(row)
        self._entries.append(entry)

        self._set_cell(row, COL_NAME, entry.name)
        self._set_cell(row, COL_NEW_NAME, "")
        self._set_cell(row, COL_EXTENSION, entry.extension_label)
        # Trailing slash preserves the contract with ``os.rename`` callers.
        self._set_cell(row, COL_PATH, f"{entry.directory}/")
        self._set_cell(row, COL_SIZE, self._size_label(entry))

    def _set_cell(self, row: int, column: int, text: str) -> None:
        self._table.setItem(row, column, QtWidgets.QTableWidgetItem(text))

    @staticmethod
    def _size_label(entry: FileEntry) -> str:
        if entry.is_folder:
            return "-"
        size_bytes = entry.size_bytes or 0
        return f"{round(size_bytes / 1024, 2)} KB"

    def row_count(self) -> int:
        return self._table.rowCount()

    def entries(self) -> Sequence[FileEntry]:
        """Domain entries currently displayed, in table row order."""
        return tuple(self._entries)

    def read_new_name(self, row: int) -> str:
        item = self._table.item(row, COL_NEW_NAME)
        return item.text() if item is not None else ""

    def set_new_names(self, new_names: Sequence[str]) -> None:
        """Write the "new name" column (painting highlighted rows)."""
        for row, new_name in enumerate(new_names):
            self._set_cell(row, COL_NEW_NAME, new_name)
            if new_name:
                self._table.item(row, COL_NEW_NAME).setBackground(self._HIGHLIGHT_COLOR)

    def clear_new_names(self) -> None:
        for row in range(self._table.rowCount()):
            self._set_cell(row, COL_NEW_NAME, "")

    def recolour(self, accept: Callable[[FileEntry], bool] | None) -> None:
        """Highlight rows whose entry satisfies ``accept`` (or all when ``None``)."""
        columns = self._table.columnCount()
        for row, entry in enumerate(self._entries):
            color = (
                self._HIGHLIGHT_COLOR
                if accept is None or accept(entry)
                else self._CLEAR_COLOR
            )
            for column in range(columns):
                item = self._table.item(row, column)
                if item is not None:
                    item.setBackground(color)

    def clear_all_row_colors(self) -> None:
        self.recolour(accept=lambda _entry: False)
