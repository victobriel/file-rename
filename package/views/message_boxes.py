"""Reusable message-box helpers with sensible defaults."""
from __future__ import annotations

from collections.abc import Callable

from PySide6 import QtCore, QtWidgets

Translator = Callable[[str], str]


class _BaseBox:
    """Shared configuration between warning and success dialogs."""

    _ICON: QtWidgets.QMessageBox.Icon = QtWidgets.QMessageBox.Icon.NoIcon
    _TITLE_KEY: str = ""

    def __init__(self, parent: QtWidgets.QWidget, translate: Translator) -> None:
        self._box = QtWidgets.QMessageBox(parent)
        self._translate = translate

    @property
    def box(self) -> QtWidgets.QMessageBox:
        """The underlying ``QMessageBox`` for callers that need to customise it."""
        return self._box

    def _prepare(self, text: str, informative_text: str) -> None:
        self._box.setMinimumSize(QtCore.QSize(800, 600))
        self._box.setWindowTitle(self._translate(self._TITLE_KEY))
        self._box.setIcon(self._ICON)
        self._box.setText(text)
        self._box.setInformativeText(informative_text)


class WarningBox(_BaseBox):
    """Warning dialog. Use ``default_button=True`` to render a single OK button."""

    _ICON = QtWidgets.QMessageBox.Icon.Warning
    _TITLE_KEY = "Warning"

    def show(
        self,
        text: str,
        informative_text: str = "",
        default_button: bool = False,
    ) -> None:
        self._prepare(text, informative_text)
        if default_button:
            self._box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            self._box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        self._box.exec()


class SuccessBox(_BaseBox):
    """Informational dialog shown after a successful rename batch."""

    _ICON = QtWidgets.QMessageBox.Icon.Information
    _TITLE_KEY = "Success"

    def show(self, text: str, informative_text: str = "") -> None:
        self._prepare(text, informative_text)
        self._box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        self._box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        self._box.exec()
