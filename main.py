import sys,os,webbrowser
import pandas as pd
from PySide6 import QtWidgets, QtGui, QtCore
from package.ui.ui_main import Ui_MainWindow
import re,datetime,zipfile,stat
from package.configs.config import Config
from package.lang.lang import Lang
from typing import Callable

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("File Rename")
        self.load_config() #load config
        appIcon = QtGui.QIcon("icons/folder.png") #set icon
        self.setWindowIcon(appIcon)
        #menu bar
        self.actionOpen_Folder.triggered.connect(self.path_change)
        self.actionAlways_backup_before_renaming.triggered.connect(self.always_backup_click)
        self.actionExit.triggered.connect(lambda: sys.exit())
        self.actionProtect_Paths.triggered.connect(lambda: self.CONFIG.set("paths", "protect_paths", str(self.actionProtect_Paths.isChecked())))
        self.actionOpen_settings.triggered.connect(self.open_config)
        self.actionDocumentation.triggered.connect(lambda: webbrowser.open("https://github.com/victobriel/file-rename"))
        self.actionAbout.triggered.connect(lambda: self.run_warning_box("File Rename Lite\nVersion: 1.0.0\nhttps://github.com/victobriel/file-rename/", default_button=True))
        #icons
        self.openFolderButton.setIcon(QtGui.QIcon("icons/folder.png"))
        self.specificFilesAddButton.setIcon(QtGui.QIcon("icons/add.png"))
        self.specificFilesClearButton.setIcon(QtGui.QIcon("icons/remove.png"))

        self.helpButton.clicked.connect(lambda: webbrowser.open("https://github.com/victobriel/file-rename"))
        self.openFolderButton.clicked.connect(self.path_change)
        self.includeSubdirCheckbox.clicked.connect(self.update_table_files)
        self.includeFoldersCheckbox.clicked.connect(self.update_table_files)
        self.allFilesCheckbox.clicked.connect(lambda: self.update_file_types_list(0))
        self.commonFilesCheckbox.clicked.connect(lambda: self.update_file_types_list(1))
        self.specificFilesCheckbox.clicked.connect(lambda: self.update_file_types_list(2))
        self.commonFilesList.itemClicked.connect(self.common_types_list_click)
        self.specificFilesLine.textChanged.connect(self.specific_types_line_change)
        self.specificFilesAddButton.clicked.connect(self.add_specific_types_click)
        self.specificFilesClearButton.clicked.connect(self.clear_specific_types_click)
        self.rulesCombo.currentIndexChanged.connect(self.rename_type_combo_change)
        self.findLine.textChanged.connect(self.replaceby_line_text_change)
        self.replaceLine.textChanged.connect(self.replaceby_line_text_change)
        self.caseSentitiveCheckbox.clicked.connect(self.replaceby_line_text_change)
        self.regexCheckbox.clicked.connect(self.replaceby_line_text_change)
        self.inneCombo.currentIndexChanged.connect(self.replaceby_line_text_change)
        self.startSpin.valueChanged.connect(self.replaceby_line_text_change)
        self.countSpin.valueChanged.connect(self.replaceby_line_text_change)
        self.renameButton.clicked.connect(self.rename_run)
        self.exitButton.clicked.connect(lambda: sys.exit())

        self.progressBar: QtWidgets.QProgressBar = QtWidgets.QProgressBar(self.statusBar)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar.setFixedWidth(200)
        self.progressBar.setFixedHeight(20)
        self.progressBar.setTextVisible(False)
        self.progressBar.setAlignment(QtCore.Qt.AlignRight)
        self.progressBar.setStyleSheet("QProgressBar {border: 1px solid #ccc;background-color: #fff; color: #000; font-weight: bold; font-size: 12px;} QProgressBar::chunk {background-color: #aed6f1;}")

        self.progressLabel: QtWidgets.QLabel = QtWidgets.QLabel(self.statusBar)
        self.progressLabel.setFixedWidth(80)
        self.progressLabel.setFixedHeight(20)
        self.progressLabel.setText("0/0")
        self.progressLabel.setAlignment(QtCore.Qt.AlignRight)
        self.progressLabel.setStyleSheet("QLabel {color: #000; font-size: 12px; margin-right: 5px; }")

        self.statusBar.addPermanentWidget(self.progressLabel)
        self.statusBar.addPermanentWidget(self.progressBar)
        #load language
        self.lang: Lang = Lang(self.CONFIG.get("config", "language"), self.CONFIG.get("config", "encoding"))
        self._m: Callable  = self.lang.translate
        self.lang.translate_ui(self)
        #load application
        self.load_common_files()
        #reset progress bar
        self.reset_progress_bar()
        #set colors
        self.WHITE_COLOR: QtGui.QColor = QtGui.QColor(255,255,255)
        self.DEFAULT_COLOR: QtGui.QColor = QtGui.QColor(174,214,241)

        self.common_files_list: list[str] = [] ; self.specific_files_list: list[str] = []
        #boxes
        self.warningbox: QtWidgets.QMessageBox = QtWidgets.QMessageBox()
        self.successbox: QtWidgets.QMessageBox = QtWidgets.QMessageBox()

        self.IGNORED_PATHS: list[str] = ['.git', '.vscode', '.idea', '__pycache__', 'venv', 'node_modules']
        self.IGNORED_FILES: list[str] = ['README.md', 'README.rst', 'LICENSE', 'config.ini', 'requirements.txt']

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return: # type: ignore # noqa: F401
            if self.specificFilesLine.hasFocus():
                self.add_specific_types_click()

    def load_config(self) -> None:
        self.CONFIG: Config = Config()
        try:
            self.CONFIG.read()
            BACKUP_STATUS: bool = eval(self.CONFIG.get("config", "backup"))
            if BACKUP_STATUS:
                self.actionAlways_backup_before_renaming.setChecked(BACKUP_STATUS)
                self.backupCheckbox.setChecked(BACKUP_STATUS)
                self.backupCheckbox.setEnabled(not BACKUP_STATUS)
            self.actionProtect_Paths.setChecked(eval(self.CONFIG.get("paths", "protect_paths")))
        except:
            self.CONFIG.resetconfig()

    def open_config(self) -> None:
        self.run_warning_box(self._m("The configuration file will be opened in the default text editor."), self._m("If you change the file contents, the application will need to be restarted to apply the changes."), True) #type: ignore # noqa: F821
        if not os.path.exists("config.ini"):
            self.load_config()
        webbrowser.open("config.ini")

    def load_common_files(self) -> None: #load common files from csv
        COMMON_FILES_DATA = pd.read_csv("db/common_file_types.csv")
        COMMON_FILES_NAME: list = COMMON_FILES_DATA['File_Name'].tolist()
        common_files_extensions: list = COMMON_FILES_DATA['File_Extensions'].tolist()
        for i in range(len(common_files_extensions)):
            common_files_extensions[i] = common_files_extensions[i].replace(" ", ";*")
        for i in range(len(COMMON_FILES_NAME)):
            if i == 0:
                self.commonFilesList.addItem('%s (*%s)' % (self._m(COMMON_FILES_NAME[i]), common_files_extensions[i]))
                continue
            self.commonFilesList.addItem('%s (*%s)' % (COMMON_FILES_NAME[i], common_files_extensions[i]))

    def run_warning_box(self, text: str, informative_text: str = "", default_button: bool = False) -> None:
        self.warningbox.setMinimumSize(QtCore.QSize(800, 600))
        self.warningbox.setWindowTitle(self._m("Warning"))
        self.warningbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        if default_button:
            self.warningbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            self.warningbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        self.warningbox.setText(text)
        self.warningbox.setInformativeText(informative_text)
        self.warningbox.exec()

    def run_success_box(self, text: str, informative_text: str = "") -> None:
        self.successbox.setMinimumSize(QtCore.QSize(800, 600))
        self.successbox.setWindowTitle(self._m("Success"))
        self.successbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        self.successbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        self.successbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        self.successbox.setText(text)
        self.successbox.setInformativeText(informative_text)
        self.successbox.exec()

    def reset_progress_bar(self) -> None:
        self.progressBar.setValue(0)
        self.statusBar.showMessage(self._m("Nothing to load")) #type: ignore # noqa: F821
        self.progressLabel.setText("0/0")

    def update_progress_bar(self, value: int) -> None:
        PROGRESS_BAR: QtWidgets.QProgressBar = self.progressBar
        PROGRESS_LABEL: QtWidgets.QLabel = self.progressLabel
        PROGRESS_BAR.setValue(value)
        PROGRESS_LABEL.setText(f'{str(PROGRESS_BAR.value())}/{str(PROGRESS_BAR.maximum())}')

    def always_backup_click(self) -> None:
        BACKUP_STATUS: bool = self.actionAlways_backup_before_renaming.isChecked()
        self.backupCheckbox.setEnabled(not BACKUP_STATUS)
        self.backupCheckbox.setChecked(BACKUP_STATUS)
        self.CONFIG.set("config", "backup", str(BACKUP_STATUS)) #update config

    def update_file_types_list(self, option: int) -> None: #0 = all files, 1 = common files, 2 = specific files
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
        self.updateframe()

    def common_types_list_click(self) -> None:
        COMMON_FILES_DATA = pd.read_csv("db/common_file_types.csv")
        COMMON_FILES_EXTENSIONS: list[str] = COMMON_FILES_DATA['File_Extensions'].tolist()
        self.common_files_list.clear()
        for i in self.commonFilesList.selectedIndexes():
            if i.row() == 0:
                self.common_files_list += self._m('Folder').split(" ")
                continue
            self.common_files_list += COMMON_FILES_EXTENSIONS[i.row()].split(" ")
        self.updateframe()

    def rename_type_combo_change(self) -> None:
        self.startSpin.setEnabled(False)
        self.countSpin.setEnabled(False)
        self.inneCombo.setEnabled(False)
        self.findLine.setEnabled(False)
        self.replaceLine.setEnabled(True)
        self.regexCheckbox.setEnabled(False)
        self.caseSentitiveCheckbox.setEnabled(False)
        self.replaceLabel.setText(self._m("... and replace with"))
        match self.rulesCombo.currentIndex():
            case 0:
                self.replaceLabel.setText(self._m("Add"))
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
                    self.findLine.setPlaceholderText(str(self.common_files_list).replace("[", "").replace("]", "").replace("'", ""))
                    return
                if self.specificFilesCheckbox.isChecked():
                    self.findLine.setPlaceholderText(str(self.specific_files_list).replace("[", "").replace("]", "").replace("'", ""))
                    return
            case 3:
                self.startSpin.setEnabled(True)
                self.countSpin.setEnabled(True)
                self.inneCombo.setEnabled(True)
                self.replaceby_line_text_change()
        self.findLine.setPlaceholderText("")
        self.update_table_list_color()
        self.replaceby_line_text_change()

    def convert(self, text) -> str:
        TODAY: datetime.datetime = datetime.datetime.now()
        DAY: str = str(TODAY.day) if len(str(TODAY.day)) > 1 else f'0{str(TODAY.day)}'
        MONTH: str = str(TODAY.month) if len(str(TODAY.month)) > 1 else f'0{str(TODAY.month)}'
        YEAR: str = str(TODAY.year)
        HOUR: str = str(TODAY.hour) if len(str(TODAY.hour)) > 1 else f'0{str(TODAY.hour)}'
        MINUTE: str = str(TODAY.minute) if len(str(TODAY.minute)) > 1 else f'0{str(TODAY.minute)}'

        text = text.replace("{%D}", DAY)
        text = text.replace("{%M}", MONTH)
        text = text.replace("{%Y}", YEAR)
        text = text.replace("{%H}", HOUR)
        text = text.replace("{%I}", MINUTE)

        REGEX: re.Pattern[str] = re.compile(r'[/\\:\*?\"<>\|]')
        for match in REGEX.finditer(text):
            text = text.replace(match.group(), "")
        return text

    def replaceby_line_text_change(self) -> None:
        REPLACELINE_VALUE: str = self.replaceLine.text()
        FINDLINE_VALUE: str = self.findLine.text()
        if not self.caseSentitiveCheckbox.isChecked():
            FINDLINE_VALUE = FINDLINE_VALUE.casefold()

        REPLACELINE_VALUE = self.convert(REPLACELINE_VALUE)
        self.replaceLine.setText(REPLACELINE_VALUE)

        FILESLIST_ROWS: int = self.filesList.rowCount()

        self.invalidLabel.setText("")

        #clear table
        for i in range(FILESLIST_ROWS):
            self.filesList.setItem(i, 1, QtWidgets.QTableWidgetItem(""))
        self.update_table_list_color()

        if ((self.rulesCombo.currentIndex() == 1 and len(FINDLINE_VALUE) <= 0)
            or ((self.rulesCombo.currentIndex() == 2) and len(REPLACELINE_VALUE) <= 0)):
            return

        NEW_VALUE: str = "" ; file_name: str ; file_extension: str
        match self.rulesCombo.currentIndex():
            case 0:
                for file in range(FILESLIST_ROWS):
                    file_name = os.path.splitext(self.filesList.item(file, 0).text())[0]
                    file_extension = self.filesList.item(file, 2).text()
                    if (self.allFilesCheckbox.isChecked()
                        or (self.commonFilesCheckbox.isChecked()
                            and (file_extension in self.common_files_list))
                        or (self.specificFilesCheckbox.isChecked()
                            and (file_extension in self.specific_files_list))):
                        file_extension = "" if file_extension[0] != "." else file_extension
                        if self.inneCombo.currentIndex():
                            NEW_VALUE = file_name + REPLACELINE_VALUE + file_extension
                        else:
                            NEW_VALUE = REPLACELINE_VALUE + file_name + file_extension
                        self.filesList.setItem(file, 1, QtWidgets.QTableWidgetItem(NEW_VALUE))
                        self.filesList.item(file, 1).setBackground(self.DEFAULT_COLOR)
            case 1:
                if self.regexCheckbox.isChecked():
                    for file in range(FILESLIST_ROWS):
                        file_name = os.path.splitext(self.filesList.item(file, 0).text())[0]
                        file_extension = self.filesList.item(file, 2).text()
                        if (self.allFilesCheckbox.isChecked()
                            or (self.commonFilesCheckbox.isChecked()
                                and (file_extension in self.common_files_list))
                            or (self.specificFilesCheckbox.isChecked()
                                and (file_extension in self.specific_files_list))):
                            file_extension = "" if file_extension[0] != "." else file_extension
                            try:
                                NEW_VALUE = re.sub(FINDLINE_VALUE, REPLACELINE_VALUE, file_name) + file_extension
                            except:
                                self.invalidLabel.setText("* " + self._m("Invalid expression"))
                                continue
                            self.filesList.setItem(file, 1, QtWidgets.QTableWidgetItem(NEW_VALUE))
                            self.filesList.item(file, 1).setBackground(self.DEFAULT_COLOR)
                else:
                    for file in range(FILESLIST_ROWS):
                        file_name = os.path.splitext(self.filesList.item(file, 0).text())[0]
                        file_extension = self.filesList.item(file, 2).text()
                        if (self.allFilesCheckbox.isChecked()
                                and (FINDLINE_VALUE in file_name)
                            or (self.commonFilesCheckbox.isChecked()
                                and (FINDLINE_VALUE in file_name)
                                    and (file_extension in self.common_files_list))
                            or (self.specificFilesCheckbox.isChecked()
                                and (FINDLINE_VALUE in file_name)
                                    and (file_extension in self.specific_files_list))):
                            file_extension = "" if file_extension[0] != "." else file_extension
                            NEW_VALUE = file_name.replace(FINDLINE_VALUE, REPLACELINE_VALUE) + file_extension
                            self.filesList.setItem(file, 1, QtWidgets.QTableWidgetItem(NEW_VALUE))
                            self.filesList.item(file, 1).setBackground(self.DEFAULT_COLOR)
            case 2:
                for file in range(FILESLIST_ROWS):
                    file_name = os.path.splitext(self.filesList.item(file, 0).text())[0]
                    file_extension = self.filesList.item(file, 2).text()
                    if file_extension[0] != ".":
                        continue #ignore folders
                    if (self.allFilesCheckbox.isChecked()
                        or (self.commonFilesCheckbox.isChecked()
                            and (file_extension in self.common_files_list))
                        or (self.specificFilesCheckbox.isChecked()
                            and (file_extension in self.specific_files_list))):
                        NEW_VALUE = f'{file_name}.{REPLACELINE_VALUE}'
                        self.filesList.setItem(file, 1, QtWidgets.QTableWidgetItem(NEW_VALUE))
                        self.filesList.item(file, 1).setBackground(self.DEFAULT_COLOR)
            case 3:
                COUNT_SPIN: int = self.countSpin.value()
                current_spin: int = self.startSpin.value()
                for file in range(FILESLIST_ROWS):
                    file_name = os.path.splitext(self.filesList.item(file, 0).text())[0]
                    file_extension = self.filesList.item(file, 2).text()
                    if (self.allFilesCheckbox.isChecked()
                        or (self.commonFilesCheckbox.isChecked()
                            and (file_extension in self.common_files_list))
                        or (self.specificFilesCheckbox.isChecked()
                            and (file_extension in self.specific_files_list))):
                        file_extension = "" if file_extension[0] != "." else file_extension
                        if self.inneCombo.currentIndex():
                            NEW_VALUE = f'{file_name}{REPLACELINE_VALUE}({str(current_spin)}){file_extension}'
                        else:
                            NEW_VALUE = f'({str(current_spin)}){REPLACELINE_VALUE}{file_name}{file_extension}'
                        self.filesList.setItem(file, 1, QtWidgets.QTableWidgetItem(NEW_VALUE))
                        self.filesList.item(file, 1).setBackground(self.DEFAULT_COLOR)
                        current_spin += COUNT_SPIN

    def rename_run(self) -> None:
        if self.backupCheckbox.isChecked() and not self.backup_run():
            return
        FILES_LIST: QtWidgets.QTableWidget = self.filesList
        TABLE_ROWS: int = self.filesList.rowCount()
        TABLE_LIST_ITEMS: list = []
        for i in range(TABLE_ROWS):
            TABLE_LIST_ITEMS.append([
                FILES_LIST.item(i, 0).text(),FILES_LIST.item(i, 1).text(),FILES_LIST.item(i, 3).text()
            ])
        if len(TABLE_LIST_ITEMS) <= 0:
            self.statusBar.showMessage(self._m("No files to rename")) #type: ignore # noqa: F821
            return
        self.reset_progress_bar()
        self.progressLabel.setText(self._m("Renaming files..."))
        self.progressBar.setMaximum(TABLE_ROWS)
        itens_renamed: int = 0
        for i in range(TABLE_ROWS):
            if len(TABLE_LIST_ITEMS[i][1]) <= 0:
                self.update_progress_bar(self.progressBar.value() + 1)
                continue
            try:
                os.rename(TABLE_LIST_ITEMS[i][2] + TABLE_LIST_ITEMS[i][0], TABLE_LIST_ITEMS[i][2] + TABLE_LIST_ITEMS[i][1])
            except Exception as e:
                self.run_warning_box(f'ERROR 0x0003: {e}', default_button=True)
                return
            itens_renamed += 1
            self.update_progress_bar(self.progressBar.value() + 1)
        self.update_table_files()
        self.run_success_box(self._m("Files renamed successfully"), self._m("{} files renamed".format(str(itens_renamed))))

    def backup_run(self) -> bool:
        self.reset_progress_bar()
        self.statusBar.showMessage(self._m("Creating backup...")) #type: ignore # noqa: F821
        DIR_PATH: str = self.pathLine.text()
        TODAY: datetime.datetime = datetime.datetime.now()
        DATE_FORMAT: str = TODAY.strftime("%Y-%d-%m-%H-%M")
        BACKUP_FORMAT: str = f'Backup_{DATE_FORMAT}.zip'
        BACKUP_PATH: str = f'{os.getcwd()}/{BACKUP_FORMAT}.zip'
        BACKUP_ZIPFILE: zipfile.ZipFile = zipfile.ZipFile(BACKUP_PATH, "a")
        for root, dirs, files in os.walk(DIR_PATH):
            if not self.includeSubdirCheckbox.isChecked() and (root != DIR_PATH):
                continue
            if any(path in root for path in self.IGNORED_PATHS):
                continue
            dirs[:] = [dir for dir in dirs if not dir.startswith(".") and not self.has_hidden_attribute(f'{root}/{dir}')]
            for file in files:
                if file in self.IGNORED_FILES:
                    continue
                BACKUP_ZIPFILE.write(f'{root}/{file}')
                self.update_progress_bar(self.progressBar.value() + 1)
        BACKUP_ZIPFILE.close()
        if not os.path.exists(BACKUP_PATH):
            self.progressLabel.setText(self._m("Error creating backup"))
            return False
        self.progressLabel.setText(self._m("Backup created"))
        return True

    def get_number_of_files(self, dir_path: str) -> int:
        self.statusBar.showMessage(self._m("Wait, checking files...")) #type: ignore # noqa: F821
        len_folders: int = 0 ; len_files: int = 0
        try:
            for root, dirs, files in os.walk(dir_path):
                if not self.includeSubdirCheckbox.isChecked() and (root != dir_path):
                    continue #ignore subdirectories
                if any(path in root for path in self.IGNORED_PATHS):
                    continue #ignore protected paths
                dirs[:] = [dir for dir in dirs if not dir.startswith(".") and not self.has_hidden_attribute(f'{root}/{dir}')] #ignore hidden folders
                len_folders += len(dirs) if self.includeFoldersCheckbox.isChecked() else 0
                files[:] = [file for file in files if not file.startswith(".") and not self.has_hidden_attribute(f'{root}/{file}') and not file in self.IGNORED_FILES] #ignore hidden files
                len_files += len(files)
        except Exception as e:
            self.run_warning_box(f'ERROR 0x0001: {e}', default_button=True)
            return 0
        return len_files + len_folders

    def path_change(self) -> None: #change path to load files
        DIR_PATH: str = QtWidgets.QFileDialog.getExistingDirectory()
        if not DIR_PATH:
            return
        if self.actionProtect_Paths.isChecked():
            PROTECTED_PATHS: list[str] = self.CONFIG.get("paths", "protected").split(",")
            if any(path in DIR_PATH for path in PROTECTED_PATHS):
                BUTTON_DISABL: QtWidgets.QPushButton = self.warningbox.addButton(self._m("Disable Protection"), QtWidgets.QMessageBox.ButtonRole.ActionRole)
                BUTTON_IGNORE: QtWidgets.QPushButton = self.warningbox.addButton(self._m("Ignore Warning"), QtWidgets.QMessageBox.ButtonRole.ActionRole)
                BUTTON_CANCEL: QtWidgets.QPushButton = self.warningbox.addButton(QtWidgets.QMessageBox.StandardButton.Cancel)
                self.warningbox.setDefaultButton(BUTTON_CANCEL)
                self.run_warning_box(
                    "This path contains protected files. It is not recommended to use this path as it may cause system problems. To unprotect paths, uncheck Protect Paths in Options, in the Menu bar.",
                    "If you ignore the path, this path will not be listed.", False)
                self.warningbox.removeButton(BUTTON_DISABL)
                self.warningbox.removeButton(BUTTON_IGNORE)
                self.warningbox.removeButton(BUTTON_CANCEL)
                if self.warningbox.clickedButton() == BUTTON_DISABL:
                    self.actionProtect_Paths.setChecked(False)
                    self.CONFIG.set("paths", "protect_paths", "False") #update config
                elif self.warningbox.clickedButton() == BUTTON_CANCEL:
                    return self.path_change()

        self.pathLine.setText(DIR_PATH)
        self.update_table_files()

    def update_table_files(self) -> None:
        self.filesList.setRowCount(0) #clear table
        self.reset_progress_bar()

        DIR_PATH: str = self.pathLine.text()
        counted_files: int = 0 ; counted_folders: int = 0 ; table_rows: int = 0
        NUMBER_OF_FILES: int = self.get_number_of_files(DIR_PATH)
        if NUMBER_OF_FILES <= 0:
            self.statusBar.showMessage(self._m("Nothing to load")) #type: ignore # noqa: F821
            return
        self.progressBar.setMaximum(NUMBER_OF_FILES)
        self.statusBar.showMessage(self._m("Loading files...")) #type: ignore # noqa: F821
        try:
            for root, dirs, files in os.walk(DIR_PATH):
                if not self.includeSubdirCheckbox.isChecked() and (root != DIR_PATH):
                    continue #ignore subdirectories
                if any(path in root for path in self.IGNORED_PATHS):
                    continue #ignore protected paths
                dirs[:] = [dir for dir in dirs if not dir.startswith(".") and not self.has_hidden_attribute(f'{root}/{dir}')] #ignore hidden folders
                if self.includeFoldersCheckbox.isChecked():
                    for dir in dirs:
                        self.filesList.insertRow(table_rows)
                        self.filesList.setItem(table_rows, 0, QtWidgets.QTableWidgetItem(dir))
                        self.filesList.setItem(table_rows, 1, QtWidgets.QTableWidgetItem(""))
                        self.filesList.setItem(table_rows, 2, QtWidgets.QTableWidgetItem(self._m("Folder")))
                        self.filesList.setItem(table_rows, 3, QtWidgets.QTableWidgetItem(f'{root}/'))
                        self.filesList.setItem(table_rows, 4, QtWidgets.QTableWidgetItem("-"))
                        counted_folders += 1
                        table_rows += 1
                        self.update_progress_bar(self.progressBar.value() + 1)
                files[:] = [file for file in files if not file.startswith(".") and not self.has_hidden_attribute(f'{root}/{file}') and not file in self.IGNORED_FILES] #ignore hidden files
                for file in files:
                    self.filesList.insertRow(table_rows)
                    self.filesList.setItem(table_rows, 0, QtWidgets.QTableWidgetItem(file))
                    self.filesList.setItem(table_rows, 1, QtWidgets.QTableWidgetItem(""))
                    file_extension: str = os.path.splitext(file)[1]
                    if file_extension == "":
                        file_extension = "Undefined"
                    self.filesList.setItem(table_rows, 2, QtWidgets.QTableWidgetItem(file_extension)) #get file extension
                    self.filesList.setItem(table_rows, 3, QtWidgets.QTableWidgetItem(f'{root}/'))
                    try:
                        file_size: float = os.path.getsize(f'{root}/{file}')
                    except:
                        file_size = 0
                    self.filesList.setItem(table_rows, 4, QtWidgets.QTableWidgetItem(f'{str(round(file_size / 1024, 2))} KB'))
                    counted_files += 1
                    table_rows += 1
                    self.update_progress_bar(self.progressBar.value() + 1)
        except Exception as e:
            self.run_warning_box(f'ERROR 0x0002: {e}', default_button=True)
            return

        self.statusBar.showMessage(self._m("Total Files: {}, Total Folders: {}").format(str(counted_files), str(counted_folders))) #type: ignore # noqa: F821
        self.update_table_list_color()
        self.replaceby_line_text_change()

    def update_table_list_color(self) -> None:
        TABLE_ROWS: int = self.filesList.rowCount()
        if TABLE_ROWS <= 0:
            return
        if self.allFilesCheckbox.isChecked():
            for i in range(TABLE_ROWS):
                self._paint_table_list_row(i)
            return
        if self.commonFilesCheckbox.isChecked() and len(self.common_files_list):
            for i in range(TABLE_ROWS):
                #paint row if file extension is in common files list
                self._paint_table_list_row(i) if self.filesList.item(i, 2).text() in self.common_files_list else self._clear_table_list_row(i)
            return
        if self.specificFilesCheckbox.isChecked() and len(self.specific_files_list):
            for i in range(TABLE_ROWS):
                #paint row if file extension is in specific files list
                self._paint_table_list_row(i) if self.filesList.item(i, 2).text() in self.specific_files_list else self._clear_table_list_row(i)
            return
        self._clear_all_table_list()

    def _paint_table_list_row(self, row) -> None:
        TABLE_COLUMNS: int = self.filesList.columnCount()
        for i in range(TABLE_COLUMNS):
            self.filesList.item(row, i).setBackground(self.DEFAULT_COLOR)

    def _clear_table_list_row(self, row) -> None:
        TABLE_COLUMNS: int = self.filesList.columnCount()
        for i in range(TABLE_COLUMNS):
            self.filesList.item(row, i).setBackground(self.WHITE_COLOR)

    def _clear_all_table_list(self) -> None:
        TABLE_ROWS = self.filesList.rowCount()
        TABLE_COLUMNS = self.filesList.columnCount()
        for i in range(TABLE_ROWS):
            for j in range(TABLE_COLUMNS):
                self.filesList.item(i, j).setBackground(self.WHITE_COLOR)

    def specific_types_line_change(self) -> None:
        #remove invalid caracters
        REGEX: re.Pattern[str] = re.compile(r'[^A-Za-z0-9./ ]*$')
        for match in REGEX.finditer(self.specificFilesLine.text()):
            self.specificFilesLine.setText(self.specificFilesLine.text().replace(match.group(0), ""))

    def add_specific_types_click(self) -> None:
        SPECIFIC_FILES_LINE_VALUE: str = self.specificFilesLine.text()
        if len(SPECIFIC_FILES_LINE_VALUE) <= 0:
            return
        EXTENSIONS: list[str] = SPECIFIC_FILES_LINE_VALUE.split(" ")
        for extension in EXTENSIONS:
            if "/" in extension:
                extension = self._m("Folder")
            elif extension[0] != ".":
                extension = f'.{extension}'
            if extension in self.specific_files_list:
                continue
            self.specificFilesList.addItem(extension)
            self.specific_files_list.append(extension)
        self.specificFilesLine.setText("")
        self.specificFilesLine.setFocus()
        self.updateframe()

    def clear_specific_types_click(self) -> None:
        self.specificFilesList.clear()
        self.specific_files_list.clear()
        self.specificFilesLine.setFocus()
        self.updateframe()

    def updateframe(self) -> None:
        self.rename_type_combo_change()
        self.update_table_list_color()
        self.replaceby_line_text_change()

    def has_hidden_attribute(self, path: str) -> bool:
        if os.name == 'nt':
            return bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        return False

if __name__ == "__main__":
    app: QtWidgets.QApplication = QtWidgets.QApplication(sys.argv)
    main: MainWindow = MainWindow()
    main.show()
    app.exec()
