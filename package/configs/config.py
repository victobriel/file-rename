"""Thin wrapper around :mod:`configparser` with safe boolean handling.

Responsibilities are deliberately narrow: load the ini file from disk, expose
typed getters/setters, and re-create a default file if it goes missing. No
``eval``, no bare ``except``.
"""
from __future__ import annotations

import configparser
import os
from pathlib import Path

_WINDOWS_PROTECTED = (
    "C:/Windows,C:/Program Files,C:/ProgramData,AppData,System Volume Information"
)
_POSIX_PROTECTED = (
    "/etc,/bin,/usr,/var,/lib,/sbin,/dev,/proc,/boot,/sys,/run,/snap,/lib64,/lib32,"
    "/media,/mnt,/opt,/srv,/tmp,/root,/home,/lost+found,/cdrom,/usr/local,/usr/share,"
    "/usr/bin,/usr/sbin,/usr/lib,/usr/lib64,/usr/lib32,/usr/local/bin,/usr/local/sbin,"
    "/usr/local/lib,/usr/local/lib64,/usr/local/lib32,/usr/share/bin,/usr/share/sbin,"
    "/usr/share/lib,/usr/share/lib64,/usr/share/lib32,/usr/bin,/usr/sbin,/usr/lib,"
    "/usr/lib64,/usr/lib32,/bin,/sbin,/lib,/lib64,/lib32,/media,/mnt,/opt,/srv,/tmp,"
    "/root,/home,/lost+found,/cdrom,/usr/local,/usr/share,/usr/bin,/usr/sbin,/usr/lib,"
    "/usr/lib64,/usr/lib32,/usr/local/bin,/usr/local/sbin,/usr/local/lib,"
    "/usr/local/lib64,/usr/local/lib32,/usr/share/bin,/usr/share/sbin,/usr/share/lib,"
    "/usr/share/lib64,/usr/share/lib32"
)


class Config:
    """Manages the user's ``config.ini`` with safe defaults."""

    def __init__(self, file: str | Path = "config.ini", language: str = "en_US") -> None:
        self._parser: configparser.ConfigParser = configparser.ConfigParser()
        self._file: Path = Path(file)
        self._default_language = language
        if not self._file.exists():
            self._write_defaults()

    def __str__(self) -> str:
        return f"{type(self).__name__}(file={self._file!s})"

    @property
    def file(self) -> Path:
        return self._file

    def read(self) -> None:
        """Load the ini file from disk, replacing any cached state."""
        self._parser.read(self._file)

    def resetconfig(self) -> None:
        """Delete the ini file (if any) and rewrite the defaults."""
        if self._file.exists():
            try:
                os.remove(self._file)
            except OSError:
                pass
        self._parser = configparser.ConfigParser()
        self._write_defaults()

    def get(self, section: str, key: str) -> str:
        return self._parser[section][key]

    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Read a value as a boolean using configparser's native parsing."""
        return self._parser.getboolean(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str) -> None:
        self._parser[section][key] = value
        try:
            with open(self._file, "w", encoding="utf-8") as handle:
                self._parser.write(handle)
        except OSError:
            # If writing fails (e.g. file vanished or permissions changed),
            # rebuild a fresh defaults file instead of leaving state half-updated.
            self.resetconfig()

    def _write_defaults(self) -> None:
        self._parser.add_section("config")
        self._parser.set("config", "backup", "False")
        self._parser.set("config", "language", self._default_language)
        self._parser.set("config", "encoding", "utf-8")
        self._parser.add_section("paths")
        self._parser.set("paths", "protect_paths", "True")
        if os.name == "nt":
            self._parser.set("paths", "protected", _WINDOWS_PROTECTED)
        elif os.name == "posix":
            self._parser.set("paths", "protected", _POSIX_PROTECTED)
        else:
            self._parser.set("paths", "protected", "")

        with open(self._file, "w", encoding="utf-8") as handle:
            self._parser.write(handle)
