"""Date-token substitution and invalid-character sanitising for rename text."""
from __future__ import annotations

import datetime
import re


class TokenSubstitutor:
    """Replaces ``{%D}``, ``{%M}``, ``{%Y}``, ``{%H}``, ``{%I}`` tokens with the
    current date/time fragments and strips characters not allowed in file names.

    Tokens use zero-padded two-digit values for day/month/hour/minute and a
    four-digit year. Invalid filename characters (``/ \\ : * ? " < > |``) are
    removed from the final text.
    """

    _INVALID_FILENAME_CHARS = re.compile(r'[/\\:\*?\"<>\|]')

    def substitute(self, text: str, now: datetime.datetime | None = None) -> str:
        """Return ``text`` with date tokens expanded and invalid chars removed."""
        moment = now or datetime.datetime.now()
        day = f"{moment.day:02d}"
        month = f"{moment.month:02d}"
        year = str(moment.year)
        hour = f"{moment.hour:02d}"
        minute = f"{moment.minute:02d}"

        replaced = (
            text.replace("{%D}", day)
            .replace("{%M}", month)
            .replace("{%Y}", year)
            .replace("{%H}", hour)
            .replace("{%I}", minute)
        )
        return self.sanitize(replaced)

    def sanitize(self, text: str) -> str:
        """Strip characters illegal in file names."""
        return self._INVALID_FILENAME_CHARS.sub("", text)
