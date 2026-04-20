"""Translates the generated ``Ui_MainWindow`` widgets using the active language."""
from __future__ import annotations

from typing import TYPE_CHECKING

from package.lang.lang import Lang

if TYPE_CHECKING:
    from package.ui.ui_main import Ui_MainWindow


class UiTranslator:
    """Applies the user's language to every label, menu and action in the UI.

    This replaces the ``Lang.translate_ui`` monkey-patch from the legacy code
    by taking the UI object explicitly instead of mutating it from inside the
    language module.
    """

    def __init__(self, lang: Lang) -> None:
        self._lang = lang

    def translate(self, ui: Ui_MainWindow) -> None:
        t = self._lang.translate

        ui.menuFile.setTitle(t("File"))
        ui.menuOptions.setTitle(t("Options"))
        ui.menuHelp.setTitle(t("Help"))

        ui.actionOpen_Folder.setText(t("Open Folder"))
        ui.actionAlways_backup_before_renaming.setText(t("Always backup before renaming"))
        ui.actionExit.setText(t("Exit"))

        ui.actionProtect_Paths.setText(t("Protect Paths"))
        ui.actionOpen_settings.setText(t("Settings"))

        ui.actionDocumentation.setText(t("Documentation"))
        ui.actionAbout.setText(t("About"))

        ui.helpButton.setText(t("Welcome! If you need help, click me!"))
        ui.Step1.setTitle(t("Step 1: Select the folder where the files are located"))
        ui.includeFoldersCheckbox.setText(t("Include folders"))
        ui.includeSubdirCheckbox.setText(t("Include files in subdirectories"))

        ui.Step2.setTitle(t("Step 2: Select the types of files to rename"))
        ui.allFilesCheckbox.setText(t("All types of files"))
        ui.commonFilesCheckbox.setText(t("Common types of files"))
        ui.specificFilesCheckbox.setText(t("Specific types of files"))

        ui.Step3.setText(t("Step 3: Set the rules"))
        ui.rulesCombo.setItemText(0, t("Add Text or Date"))
        ui.rulesCombo.setItemText(1, t("Replace File Name"))
        ui.rulesCombo.setItemText(2, t("Replace File Extension"))
        ui.rulesCombo.setItemText(3, t("Make sequential"))
        ui.startLabel.setText(t("Start at"))
        ui.countLabel.setText(t("Count by"))

        ui.Step4.setTitle(t("Step 4: Choose some options"))
        ui.findLabel.setText(t("Find..."))
        ui.replaceLabel.setText(t("... and replace with"))
        ui.caseSentitiveCheckbox.setText(t("Case sensitive"))
        ui.regexCheckbox.setText(t("Regular Expression"))
        ui.inLabel.setText(t("In"))
        ui.inneCombo.setItemText(0, t("Before"))
        ui.inneCombo.setItemText(1, t("After"))

        ui.backupCheckbox.setText(t("Backup files before renaming"))
        ui.Step5.setText(t("Step 5: Rename them"))
        ui.renameButton.setText(t("Rename"))
        ui.exitButton.setText(t("Exit"))

        ui.filesList.setHorizontalHeaderLabels(
            [
                t("File Name"),
                t("New File Name"),
                t("File Extension"),
                t("Path"),
                t("Size"),
            ]
        )
