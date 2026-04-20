"""Status-bar widget combining a progress bar and a short text label."""
from __future__ import annotations

from PySide6 import QtCore, QtWidgets


class ProgressStatus:
    """Encapsulates the progress bar and label attached to the status bar.

    Owning the two widgets together lets the rest of the app drive progress
    with just ``reset``, ``set_maximum``, ``advance`` and ``set_message``.
    """

    _BAR_STYLE = (
        "QProgressBar {border: 1px solid #ccc;background-color: #fff;"
        " color: #000; font-weight: bold; font-size: 12px;}"
        " QProgressBar::chunk {background-color: #aed6f1;}"
    )
    _LABEL_STYLE = "QLabel {color: #000; font-size: 12px; margin-right: 5px; }"

    def __init__(self, status_bar: QtWidgets.QStatusBar) -> None:
        self._status_bar = status_bar

        self._bar = QtWidgets.QProgressBar(status_bar)
        self._bar.setMaximum(100)
        self._bar.setMinimum(0)
        self._bar.setValue(0)
        self._bar.setFixedWidth(200)
        self._bar.setFixedHeight(20)
        self._bar.setTextVisible(False)
        self._bar.setAlignment(QtCore.Qt.AlignRight)
        self._bar.setStyleSheet(self._BAR_STYLE)

        self._label = QtWidgets.QLabel(status_bar)
        self._label.setFixedWidth(80)
        self._label.setFixedHeight(20)
        self._label.setText("0/0")
        self._label.setAlignment(QtCore.Qt.AlignRight)
        self._label.setStyleSheet(self._LABEL_STYLE)

        status_bar.addPermanentWidget(self._label)
        status_bar.addPermanentWidget(self._bar)

    def reset(self, idle_message: str = "") -> None:
        """Zero the bar and clear the label back to ``0/0``."""
        self._bar.setValue(0)
        if idle_message:
            self._status_bar.showMessage(idle_message)
        self._label.setText("0/0")

    def set_maximum(self, maximum: int) -> None:
        self._bar.setMaximum(maximum)

    def set_message(self, message: str) -> None:
        """Show a transient status message in the bar."""
        self._status_bar.showMessage(message)

    def set_label(self, text: str) -> None:
        """Overwrite the small right-hand label (e.g. ``"Renaming files..."``)."""
        self._label.setText(text)

    def advance(self, step: int = 1) -> None:
        """Increment the bar by ``step`` and refresh the ``value/max`` label."""
        self._bar.setValue(self._bar.value() + step)
        self._label.setText(f"{self._bar.value()}/{self._bar.maximum()}")
