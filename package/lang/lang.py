"""Simple JSON-backed i18n loader.

The ``Lang`` class is intentionally tiny — it only knows how to read a
language file and translate message keys. UI-widget translation lives in
``package.views.ui_translator`` so the language module stays Qt-free.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Lang:
    """Loads ``package/lang/bases/<code>.json`` and looks up message strings."""

    DEFAULT_LANGUAGE: str = "en"
    BASES_DIR: Path = Path("package/lang/bases")

    def __init__(self, user_language: str, encode: str = "utf-8") -> None:
        self.user_language: str = user_language
        self.encode: str = encode
        self.messages: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load the language JSON file for ``user_language``.

        The English base ships with an empty ``messages`` dict, so we skip
        reading it entirely when the user's language equals
        :data:`DEFAULT_LANGUAGE`, matching the original behaviour.
        """
        if self.user_language == self.DEFAULT_LANGUAGE:
            return
        path = self.BASES_DIR / f"{self.user_language}.json"
        with open(path, encoding=self.encode) as handle:
            self.messages = json.load(handle)

    def get(self, element: str) -> str | None:
        """Return a top-level metadata entry (``encoding``, ``name``…)."""
        return self.messages.get(element)

    def translate(self, message: str) -> str:
        """Translate ``message`` using the loaded catalogue.

        Falls back to ``message`` itself when no translation is available.
        """
        catalogue = self.messages.get("messages") if self.messages else None
        if catalogue and message in catalogue:
            return catalogue[message]
        return message
