#--coding: utf-8 --
# mypy: ignore-errors
import json
class Lang:
    def __init__(self, user_language: str, encode="utf-8") -> None:
        super().__init__()
        self.user_language: str = user_language
        self.encode: str = encode
        self.messages: dict = {}
        self.load()

    def load(self) -> None:
        self.DEFAULT_LANGUAGE: str = "en"
        if self.user_language != self.DEFAULT_LANGUAGE:
            with open('package/lang/bases/{}.json'.format(self.user_language), 'r', encoding=self.encode) as json_file:
                self.messages = json.load(json_file)

    def get(self, element: str) -> str:
        return self.messages[element] if element in self.messages else None

    def translate(self, message: str) -> str:
        if len(self.messages["messages"]) > 0 and (message in self.messages["messages"]):
            return self.messages["messages"][message]
        return message
    
    def _m():
        pass

    def translate_ui(self, MainWindow) -> None:
        self = MainWindow
        self.menuFile.setTitle(self._m("File"))
        self.menuOptions.setTitle(self._m("Options"))
        self.menuHelp.setTitle(self._m("Help"))

        self.actionOpen_Folder.setText(self._m("Open Folder"))
        self.actionAlways_backup_before_renaming.setText(self._m("Always backup before renaming"))
        self.actionExit.setText(self._m("Exit"))
        
        self.actionProtect_Paths.setText(self._m("Protect Paths"))
        self.actionOpen_settings.setText(self._m("Settings"))

        self.actionDocumentation.setText(self._m("Documentation"))
        self.actionAbout.setText(self._m("About"))

        self.helpButton.setText(self._m("Welcome! If you need help, click me!"))
        self.Step1.setTitle(self._m("Step 1: Select the folder where the files are located"))
        self.includeFoldersCheckbox.setText(self._m("Include folders"))
        self.includeSubdirCheckbox.setText(self._m("Include files in subdirectories"))

        self.Step2.setTitle(self._m("Step 2: Select the types of files to rename"))
        self.allFilesCheckbox.setText(self._m("All types of files"))
        self.commonFilesCheckbox.setText(self._m("Common types of files"))
        self.specificFilesCheckbox.setText(self._m("Specific types of files"))

        self.Step3.setText(self._m("Step 3: Set the rules"))
        self.rulesCombo.setItemText(0, self._m("Add Text or Date"))
        self.rulesCombo.setItemText(1, self._m("Replace File Name"))
        self.rulesCombo.setItemText(2, self._m("Replace File Extension"))
        self.rulesCombo.setItemText(3, self._m("Make sequential"))
        self.startLabel.setText(self._m("Start at"))
        self.countLabel.setText(self._m("Count by"))

        self.Step4.setTitle(self._m("Step 4: Choose some options"))
        self.findLabel.setText(self._m("Find..."))
        self.replaceLabel.setText(self._m("... and replace with"))
        self.caseSentitiveCheckbox.setText(self._m("Case sensitive"))
        self.regexCheckbox.setText(self._m("Regular Expression"))
        self.inLabel.setText(self._m("In"))
        self.inneCombo.setItemText(0, self._m("Before"))
        self.inneCombo.setItemText(1, self._m("After"))

        self.backupCheckbox.setText(self._m("Backup files before renaming"))
        self.Step5.setText(self._m("Step 5: Rename them"))
        self.renameButton.setText(self._m("Rename"))
        self.exitButton.setText(self._m("Exit"))

        self.filesList.setHorizontalHeaderLabels([self._m("File Name"), self._m("New File Name"), self._m("File Extension"), self._m("Path"), self._m("Size")])
