"""Slim ``QMainWindow`` that wires Qt signals to controllers and services."""
from __future__ import annotations

import sys
import webbrowser
from collections.abc import Callable
from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from package.configs.config import Config
from package.domain.filters import (
    AllFilter,
    CommonExtensionsFilter,
    FileTypeFilter,
    SpecificExtensionsFilter,
)
from package.domain.rename_rules import RenameContext, RuleRegistry
from package.domain.tokens import TokenSubstitutor
from package.lang.lang import Lang
from package.services.backup_service import BackupService
from package.services.common_files_repository import CommonFilesRepository
from package.services.file_scanner import FileScanner, ScanOptions
from package.services.rename_service import RenameService
from package.ui.ui_main import Ui_MainWindow
from package.views.controllers.rename_controller import RenameController
from package.views.file_table_presenter import FileTablePresenter
from package.views.message_boxes import SuccessBox, WarningBox
from package.views.progress_status import ProgressStatus
from package.views.ui_translator import UiTranslator

_RULE_IDS_BY_INDEX: tuple[str, ...] = (
    "add",
    "replace",
    "replace_extension",
    "sequential",
)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """Top-level window. Owns collaborators; delegates all logic to them."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("File Rename")
        self.setWindowIcon(QtGui.QIcon("icons/folder.png"))

        self._config = Config()
        self._load_config()

        self._lang = Lang(
            self._config.get("config", "language"),
            self._config.get("config", "encoding"),
        )
        self._translate: Callable[[str], str] = self._lang.translate

        UiTranslator(self._lang).translate(self)

        self._tokens = TokenSubstitutor()
        self._common_files = CommonFilesRepository()
        self._common_file_types: list[str] = []
        self._specific_file_types: list[str] = []

        self._progress = ProgressStatus(self.statusBar)
        self._warning_box = WarningBox(self, self._translate)
        self._success_box = SuccessBox(self, self._translate)
        self._table = FileTablePresenter(self.filesList, self._translate)

        scanner = FileScanner(label_provider=self._label_for_raw_entry)
        self._controller = RenameController(
            scanner=scanner,
            rename_service=RenameService(),
            backup_service=BackupService(),
            table=self._table,
            progress=self._progress,
            warning_box=self._warning_box,
            success_box=self._success_box,
            translate=self._translate,
        )

        self._apply_icons()
        self._wire_menu()
        self._wire_buttons()
        self._wire_filters()
        self._wire_rule_inputs()

        self._populate_common_files_widget()
        self._progress.reset(self._translate("Nothing to load"))

    # -- configuration -----------------------------------------------------

    def _load_config(self) -> None:
        try:
            self._config.read()
            backup = self._config.getboolean("config", "backup", fallback=False)
            if backup:
                self.actionAlways_backup_before_renaming.setChecked(True)
                self.backupCheckbox.setChecked(True)
                self.backupCheckbox.setEnabled(False)
            self.actionProtect_Paths.setChecked(
                self._config.getboolean("paths", "protect_paths", fallback=True)
            )
        except (OSError, KeyError, ValueError):
            self._config.resetconfig()

    # -- UI wiring ---------------------------------------------------------

    def _apply_icons(self) -> None:
        self.openFolderButton.setIcon(QtGui.QIcon("icons/folder.png"))
        self.specificFilesAddButton.setIcon(QtGui.QIcon("icons/add.png"))
        self.specificFilesClearButton.setIcon(QtGui.QIcon("icons/remove.png"))

    def _wire_menu(self) -> None:
        self.actionOpen_Folder.triggered.connect(self._on_path_change)
        self.actionAlways_backup_before_renaming.triggered.connect(self._on_always_backup_click)
        self.actionExit.triggered.connect(lambda: sys.exit())
        self.actionProtect_Paths.triggered.connect(
            lambda: self._config.set(
                "paths", "protect_paths", str(self.actionProtect_Paths.isChecked())
            )
        )
        self.actionOpen_settings.triggered.connect(self._on_open_settings)
        self.actionDocumentation.triggered.connect(
            lambda: webbrowser.open("https://github.com/victobriel/file-rename")
        )
        self.actionAbout.triggered.connect(
            lambda: self._warning_box.show(
                "File Rename Lite\nVersion: 1.0.0\nhttps://github.com/victobriel/file-rename/",
                default_button=True,
            )
        )

    def _wire_buttons(self) -> None:
        self.helpButton.clicked.connect(
            lambda: webbrowser.open("https://github.com/victobriel/file-rename")
        )
        self.openFolderButton.clicked.connect(self._on_path_change)
        self.renameButton.clicked.connect(self._on_rename_clicked)
        self.exitButton.clicked.connect(lambda: sys.exit())

    def _wire_filters(self) -> None:
        self.includeSubdirCheckbox.clicked.connect(self._reload_current_directory)
        self.includeFoldersCheckbox.clicked.connect(self._reload_current_directory)
        self.allFilesCheckbox.clicked.connect(lambda: self._on_file_type_option(0))
        self.commonFilesCheckbox.clicked.connect(lambda: self._on_file_type_option(1))
        self.specificFilesCheckbox.clicked.connect(lambda: self._on_file_type_option(2))
        self.commonFilesList.itemClicked.connect(self._on_common_types_click)
        self.specificFilesLine.textChanged.connect(self._on_specific_line_change)
        self.specificFilesAddButton.clicked.connect(self._on_add_specific_click)
        self.specificFilesClearButton.clicked.connect(self._on_clear_specific_click)

    def _wire_rule_inputs(self) -> None:
        self.rulesCombo.currentIndexChanged.connect(self._on_rule_combo_change)
        self.findLine.textChanged.connect(self._refresh_preview)
        self.replaceLine.textChanged.connect(self._refresh_preview)
        self.caseSentitiveCheckbox.clicked.connect(self._refresh_preview)
        self.regexCheckbox.clicked.connect(self._refresh_preview)
        self.inneCombo.currentIndexChanged.connect(self._refresh_preview)
        self.startSpin.valueChanged.connect(self._refresh_preview)
        self.countSpin.valueChanged.connect(self._refresh_preview)

    # -- common files list -------------------------------------------------

    def _populate_common_files_widget(self) -> None:
        for index, group in enumerate(self._common_files.groups()):
            # The first row is the "Folder" group — its display name is
            # translated so users see the word in their language.
            display_name = self._translate(group.name) if index == 0 else group.name
            self.commonFilesList.addItem(f"{display_name} (*{group.display_pattern()})")

    def _label_for_raw_entry(self, extension: str, is_folder: bool) -> str:
        if is_folder:
            return self._translate("Folder")
        if not extension:
            return "Undefined"
        return extension

    # -- events: menu & app ------------------------------------------------

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return:
            if self.specificFilesLine.hasFocus():
                self._on_add_specific_click()

    def _on_open_settings(self) -> None:
        self._warning_box.show(
            self._translate("The configuration file will be opened in the default text editor."),
            self._translate(
                "If you change the file contents, the application will need to be "
                "restarted to apply the changes."
            ),
            True,
        )
        if not self._config.file.exists():
            self._load_config()
        webbrowser.open(str(self._config.file))

    def _on_always_backup_click(self) -> None:
        backup_on = self.actionAlways_backup_before_renaming.isChecked()
        self.backupCheckbox.setEnabled(not backup_on)
        self.backupCheckbox.setChecked(backup_on)
        self._config.set("config", "backup", str(backup_on))

    # -- events: path change ----------------------------------------------

    def _on_path_change(self) -> None:
        chosen = QtWidgets.QFileDialog.getExistingDirectory()
        if not chosen:
            return
        if self.actionProtect_Paths.isChecked():
            protected = self._config.get("paths", "protected").split(",")
            if any(path in chosen for path in protected):
                if not self._handle_protected_path():
                    return

        self.pathLine.setText(chosen)
        self._reload_current_directory()

    def _handle_protected_path(self) -> bool:
        """Interact with the warning dialog; returns False when the user cancels."""
        warning = self._warning_box.box
        btn_disable = warning.addButton(
            self._translate("Disable Protection"),
            QtWidgets.QMessageBox.ButtonRole.ActionRole,
        )
        btn_ignore = warning.addButton(
            self._translate("Ignore Warning"),
            QtWidgets.QMessageBox.ButtonRole.ActionRole,
        )
        btn_cancel = warning.addButton(QtWidgets.QMessageBox.StandardButton.Cancel)
        warning.setDefaultButton(btn_cancel)
        self._warning_box.show(
            "This path contains protected files. It is not recommended to use this "
            "path as it may cause system problems. To unprotect paths, uncheck "
            "Protect Paths in Options, in the Menu bar.",
            "If you ignore the path, this path will not be listed.",
            False,
        )
        clicked = warning.clickedButton()
        warning.removeButton(btn_disable)
        warning.removeButton(btn_ignore)
        warning.removeButton(btn_cancel)
        if clicked == btn_disable:
            self.actionProtect_Paths.setChecked(False)
            self._config.set("paths", "protect_paths", "False")
            return True
        if clicked == btn_cancel:
            self._on_path_change()
            return False
        return True

    def _reload_current_directory(self) -> None:
        path_text = self.pathLine.text()
        if not path_text:
            return
        self._controller.load_directory(Path(path_text), self._scan_options())
        self._refresh_preview()

    def _scan_options(self) -> ScanOptions:
        return ScanOptions(
            include_subdirectories=self.includeSubdirCheckbox.isChecked(),
            include_folders=self.includeFoldersCheckbox.isChecked(),
        )

    # -- events: file type filters ----------------------------------------

    def _on_file_type_option(self, option: int) -> None:
        self.allFilesCheckbox.setChecked(False)
        self.commonFilesCheckbox.setChecked(False)
        self.specificFilesCheckbox.setChecked(False)
        self.commonFilesList.setEnabled(False)
        self.specificFilesList.setEnabled(False)
        self.specificFilesLine.setEnabled(False)
        self.specificFilesAddButton.setEnabled(False)
        self.specificFilesClearButton.setEnabled(False)

        match option:
            case 1:
                self.commonFilesCheckbox.setChecked(True)
                self.commonFilesList.setEnabled(True)
            case 2:
                self.specificFilesCheckbox.setChecked(True)
                self.specificFilesList.setEnabled(True)
                self.specificFilesLine.setEnabled(True)
                self.specificFilesAddButton.setEnabled(True)
                self.specificFilesClearButton.setEnabled(True)
                self.specificFilesLine.setFocus()
            case _:
                self.allFilesCheckbox.setChecked(True)
        self._refresh_after_filter_change()

    def _on_common_types_click(self) -> None:
        groups = self._common_files.groups()
        self._common_file_types.clear()
        for selection in self.commonFilesList.selectedIndexes():
            row = selection.row()
            if row == 0:
                # The folder row contributes the translated "Folder" label.
                self._common_file_types += self._translate("Folder").split(" ")
                continue
            self._common_file_types += groups[row].extension_tokens()
        self._refresh_after_filter_change()

    def _on_specific_line_change(self) -> None:
        # Forbid everything except letters, digits, dot, slash, and space.
        import re

        cleaned_pattern = re.compile(r"[^A-Za-z0-9./ ]*$")
        text = self.specificFilesLine.text()
        for match in cleaned_pattern.finditer(text):
            text = text.replace(match.group(0), "")
        self.specificFilesLine.setText(text)

    def _on_add_specific_click(self) -> None:
        raw = self.specificFilesLine.text()
        if not raw:
            return
        for token in raw.split(" "):
            if not token:
                continue
            if "/" in token:
                extension = self._translate("Folder")
            elif not token.startswith("."):
                extension = f".{token}"
            else:
                extension = token
            if extension in self._specific_file_types:
                continue
            self.specificFilesList.addItem(extension)
            self._specific_file_types.append(extension)
        self.specificFilesLine.setText("")
        self.specificFilesLine.setFocus()
        self._refresh_after_filter_change()

    def _on_clear_specific_click(self) -> None:
        self.specificFilesList.clear()
        self._specific_file_types.clear()
        self.specificFilesLine.setFocus()
        self._refresh_after_filter_change()

    # -- events: rule combo -----------------------------------------------

    def _on_rule_combo_change(self) -> None:
        self.startSpin.setEnabled(False)
        self.countSpin.setEnabled(False)
        self.inneCombo.setEnabled(False)
        self.findLine.setEnabled(False)
        self.replaceLine.setEnabled(True)
        self.regexCheckbox.setEnabled(False)
        self.caseSentitiveCheckbox.setEnabled(False)
        self.replaceLabel.setText(self._translate("... and replace with"))

        match self.rulesCombo.currentIndex():
            case 0:
                self.replaceLabel.setText(self._translate("Add"))
                self.inneCombo.setEnabled(True)
            case 1:
                self.findLine.setEnabled(True)
                self.regexCheckbox.setEnabled(True)
                self.caseSentitiveCheckbox.setEnabled(True)
            case 2:
                self.findLine.setText("")
                self.findLine.setPlaceholderText("")
                if self.allFilesCheckbox.isChecked():
                    self.findLine.setPlaceholderText(".*")
                    return
                if self.commonFilesCheckbox.isChecked():
                    self.findLine.setPlaceholderText(self._csv_tokens(self._common_file_types))
                    return
                if self.specificFilesCheckbox.isChecked():
                    self.findLine.setPlaceholderText(self._csv_tokens(self._specific_file_types))
                    return
            case 3:
                self.startSpin.setEnabled(True)
                self.countSpin.setEnabled(True)
                self.inneCombo.setEnabled(True)
                self._refresh_preview()
        self.findLine.setPlaceholderText("")
        self._recolor_table()
        self._refresh_preview()

    @staticmethod
    def _csv_tokens(tokens: list[str]) -> str:
        return ", ".join(tokens)

    # -- preview & recolor -------------------------------------------------

    def _refresh_after_filter_change(self) -> None:
        self._on_rule_combo_change()
        self._recolor_table()
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        # Expand date tokens and sanitise the replace input before using it.
        replace_value = self._tokens.substitute(self.replaceLine.text())
        if replace_value != self.replaceLine.text():
            self.replaceLine.setText(replace_value)

        self.invalidLabel.setText("")
        self._table.clear_new_names()
        self._recolor_table()

        rule_index = self.rulesCombo.currentIndex()
        find_value = self.findLine.text()
        if rule_index == 1 and not find_value:
            return
        if rule_index == 2 and not replace_value:
            return

        context = RenameContext(
            find=find_value,
            replace=replace_value,
            case_sensitive=self.caseSentitiveCheckbox.isChecked(),
            regex=self.regexCheckbox.isChecked(),
            position_after=bool(self.inneCombo.currentIndex()),
            sequential_start=self.startSpin.value(),
            sequential_count=self.countSpin.value(),
            filter_=self._current_filter(),
        )
        result = self._controller.compute_preview(_RULE_IDS_BY_INDEX[rule_index], context)
        if result.error_message is not None:
            self.invalidLabel.setText("* " + self._translate(result.error_message))

    def _recolor_table(self) -> None:
        if self._table.row_count() <= 0:
            return
        if self.allFilesCheckbox.isChecked():
            self._table.recolour(accept=None)
            return
        if self.commonFilesCheckbox.isChecked() and self._common_file_types:
            filter_ = CommonExtensionsFilter(self._common_file_types)
            self._table.recolour(accept=filter_.matches)
            return
        if self.specificFilesCheckbox.isChecked() and self._specific_file_types:
            filter_ = SpecificExtensionsFilter(self._specific_file_types)
            self._table.recolour(accept=filter_.matches)
            return
        self._table.clear_all_row_colors()

    def _current_filter(self) -> FileTypeFilter:
        if self.commonFilesCheckbox.isChecked():
            return CommonExtensionsFilter(self._common_file_types)
        if self.specificFilesCheckbox.isChecked():
            return SpecificExtensionsFilter(self._specific_file_types)
        return AllFilter()

    # -- rename ------------------------------------------------------------

    def _on_rename_clicked(self) -> None:
        if self.backupCheckbox.isChecked():
            path_text = self.pathLine.text()
            if not path_text:
                return
            if not self._controller.run_backup(Path(path_text), self._scan_options()):
                return
        if self._controller.execute_rename():
            self._reload_current_directory()
