# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainPsMWYc.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QCommandLinkButton, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1111, 705)
        MainWindow.setStyleSheet(u"QLineEdit:disabled {\n"
"	background-color: #eee\n"
"}")
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionEnglish = QAction(MainWindow)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.actionEnglish.setCheckable(True)
        self.actionEnglish.setChecked(False)
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionPortugues_BR = QAction(MainWindow)
        self.actionPortugues_BR.setObjectName(u"actionPortugues_BR")
        self.actionPortugues_BR.setCheckable(True)
        self.actionAlways_backup_before_renaming = QAction(MainWindow)
        self.actionAlways_backup_before_renaming.setObjectName(u"actionAlways_backup_before_renaming")
        self.actionAlways_backup_before_renaming.setCheckable(True)
        self.actionProtect_Paths = QAction(MainWindow)
        self.actionProtect_Paths.setObjectName(u"actionProtect_Paths")
        self.actionProtect_Paths.setCheckable(True)
        self.actionProtect_Paths.setChecked(True)
        self.actionOpen_Folder = QAction(MainWindow)
        self.actionOpen_Folder.setObjectName(u"actionOpen_Folder")
        self.actionOpen_settings = QAction(MainWindow)
        self.actionOpen_settings.setObjectName(u"actionOpen_settings")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actiontest = QAction(MainWindow)
        self.actiontest.setObjectName(u"actiontest")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.Step4 = QGroupBox(self.centralwidget)
        self.Step4.setObjectName(u"Step4")
        self.gridLayout_5 = QGridLayout(self.Step4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMaximumSize)
        self.replaceLabel = QLabel(self.Step4)
        self.replaceLabel.setObjectName(u"replaceLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.replaceLabel.sizePolicy().hasHeightForWidth())
        self.replaceLabel.setSizePolicy(sizePolicy1)
        self.replaceLabel.setMinimumSize(QSize(110, 0))
        self.replaceLabel.setMaximumSize(QSize(105, 16777215))
        self.replaceLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.replaceLabel)

        self.replaceLine = QLineEdit(self.Step4)
        self.replaceLine.setObjectName(u"replaceLine")
        self.replaceLine.setMinimumSize(QSize(0, 24))
        font = QFont()
        font.setPointSize(9)
        self.replaceLine.setFont(font)
        self.replaceLine.setFocusPolicy(Qt.ClickFocus)
        self.replaceLine.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.replaceLine)


        self.gridLayout_5.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.inLabel = QLabel(self.Step4)
        self.inLabel.setObjectName(u"inLabel")
        sizePolicy1.setHeightForWidth(self.inLabel.sizePolicy().hasHeightForWidth())
        self.inLabel.setSizePolicy(sizePolicy1)
        self.inLabel.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_8.addWidget(self.inLabel)

        self.inneCombo = QComboBox(self.Step4)
        self.inneCombo.addItem("")
        self.inneCombo.addItem("")
        self.inneCombo.setObjectName(u"inneCombo")
        self.inneCombo.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.inneCombo)


        self.gridLayout_5.addLayout(self.horizontalLayout_8, 3, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setSizeConstraint(QLayout.SetMaximumSize)
        self.findLabel = QLabel(self.Step4)
        self.findLabel.setObjectName(u"findLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.findLabel.sizePolicy().hasHeightForWidth())
        self.findLabel.setSizePolicy(sizePolicy2)
        self.findLabel.setMinimumSize(QSize(110, 0))
        self.findLabel.setMaximumSize(QSize(105, 10))
        self.findLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.findLabel)

        self.findLine = QLineEdit(self.Step4)
        self.findLine.setObjectName(u"findLine")
        self.findLine.setMinimumSize(QSize(0, 24))
        self.findLine.setFont(font)
        self.findLine.setFocusPolicy(Qt.ClickFocus)
        self.findLine.setLayoutDirection(Qt.LeftToRight)
        self.findLine.setClearButtonEnabled(True)

        self.horizontalLayout_6.addWidget(self.findLine)


        self.gridLayout_5.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)

        self.caseSentitiveCheckbox = QCheckBox(self.Step4)
        self.caseSentitiveCheckbox.setObjectName(u"caseSentitiveCheckbox")
        self.caseSentitiveCheckbox.setChecked(True)

        self.gridLayout_5.addWidget(self.caseSentitiveCheckbox, 0, 1, 1, 1)

        self.regexCheckbox = QCheckBox(self.Step4)
        self.regexCheckbox.setObjectName(u"regexCheckbox")

        self.gridLayout_5.addWidget(self.regexCheckbox, 1, 1, 1, 1)

        self.invalidLabel = QLabel(self.Step4)
        self.invalidLabel.setObjectName(u"invalidLabel")
        self.invalidLabel.setStyleSheet(u"color: red;")

        self.gridLayout_5.addWidget(self.invalidLabel, 1, 0, 1, 1, Qt.AlignHCenter)


        self.gridLayout_2.addWidget(self.Step4, 7, 1, 1, 1)

        self.helpButton = QCommandLinkButton(self.centralwidget)
        self.helpButton.setObjectName(u"helpButton")
        self.helpButton.setStyleSheet(u"border: 1px solid rgb(220, 220, 220);")

        self.gridLayout_2.addWidget(self.helpButton, 1, 1, 1, 1)

        self.Step30 = QGroupBox(self.centralwidget)
        self.Step30.setObjectName(u"Step30")
        self.horizontalLayout_11 = QHBoxLayout(self.Step30)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.Step3 = QLabel(self.Step30)
        self.Step3.setObjectName(u"Step3")
        sizePolicy1.setHeightForWidth(self.Step3.sizePolicy().hasHeightForWidth())
        self.Step3.setSizePolicy(sizePolicy1)
        self.Step3.setMinimumSize(QSize(0, 0))
        self.Step3.setMaximumSize(QSize(16777215, 16777215))
        self.Step3.setLayoutDirection(Qt.LeftToRight)
        self.Step3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.Step3)

        self.rulesCombo = QComboBox(self.Step30)
        self.rulesCombo.addItem("")
        self.rulesCombo.addItem("")
        self.rulesCombo.addItem("")
        self.rulesCombo.addItem("")
        self.rulesCombo.setObjectName(u"rulesCombo")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.rulesCombo.sizePolicy().hasHeightForWidth())
        self.rulesCombo.setSizePolicy(sizePolicy3)
        self.rulesCombo.setMinimumSize(QSize(0, 24))
        self.rulesCombo.setFont(font)
        self.rulesCombo.setModelColumn(0)

        self.horizontalLayout_11.addWidget(self.rulesCombo)

        self.startLabel = QLabel(self.Step30)
        self.startLabel.setObjectName(u"startLabel")

        self.horizontalLayout_11.addWidget(self.startLabel)

        self.startSpin = QSpinBox(self.Step30)
        self.startSpin.setObjectName(u"startSpin")
        self.startSpin.setEnabled(False)

        self.horizontalLayout_11.addWidget(self.startSpin)

        self.countLabel = QLabel(self.Step30)
        self.countLabel.setObjectName(u"countLabel")

        self.horizontalLayout_11.addWidget(self.countLabel)

        self.countSpin = QSpinBox(self.Step30)
        self.countSpin.setObjectName(u"countSpin")
        self.countSpin.setEnabled(False)
        self.countSpin.setWrapping(False)
        self.countSpin.setMinimum(1)

        self.horizontalLayout_11.addWidget(self.countSpin)


        self.gridLayout_2.addWidget(self.Step30, 6, 1, 1, 1)

        self.Step1 = QGroupBox(self.centralwidget)
        self.Step1.setObjectName(u"Step1")
        sizePolicy3.setHeightForWidth(self.Step1.sizePolicy().hasHeightForWidth())
        self.Step1.setSizePolicy(sizePolicy3)
        self.Step1.setMinimumSize(QSize(0, 0))
        self.Step1.setStyleSheet(u"")
        self.horizontalLayout_2 = QHBoxLayout(self.Step1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.openFolderButton = QPushButton(self.Step1)
        self.openFolderButton.setObjectName(u"openFolderButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.openFolderButton.sizePolicy().hasHeightForWidth())
        self.openFolderButton.setSizePolicy(sizePolicy4)
        self.openFolderButton.setMinimumSize(QSize(0, 0))
        self.openFolderButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.openFolderButton.setStyleSheet(u"")
        icon = QIcon()
        iconThemeName = u"Segoe UI,9,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u"../Lite/gui/img/open-folder.png", QSize(), QIcon.Normal, QIcon.Off)

        self.openFolderButton.setIcon(icon)
        self.openFolderButton.setIconSize(QSize(36, 20))

        self.horizontalLayout_5.addWidget(self.openFolderButton)

        self.pathLine = QLineEdit(self.Step1)
        self.pathLine.setObjectName(u"pathLine")
        self.pathLine.setEnabled(False)
        self.pathLine.setMinimumSize(QSize(0, 24))

        self.horizontalLayout_5.addWidget(self.pathLine)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.includeFoldersCheckbox = QCheckBox(self.Step1)
        self.includeFoldersCheckbox.setObjectName(u"includeFoldersCheckbox")

        self.verticalLayout_3.addWidget(self.includeFoldersCheckbox)

        self.includeSubdirCheckbox = QCheckBox(self.Step1)
        self.includeSubdirCheckbox.setObjectName(u"includeSubdirCheckbox")

        self.verticalLayout_3.addWidget(self.includeSubdirCheckbox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.gridLayout_2.addWidget(self.Step1, 4, 1, 1, 1)

        self.verticalSpacerRight = QSpacerItem(30, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_2.addItem(self.verticalSpacerRight, 0, 7, 8, 1)

        self.verticalSpacerLeft = QSpacerItem(30, 40, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_2.addItem(self.verticalSpacerLeft, 0, 0, 8, 1)

        self.Step50 = QVBoxLayout()
        self.Step50.setObjectName(u"Step50")
        self.backupCheckbox = QCheckBox(self.centralwidget)
        self.backupCheckbox.setObjectName(u"backupCheckbox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.backupCheckbox.sizePolicy().hasHeightForWidth())
        self.backupCheckbox.setSizePolicy(sizePolicy5)
        self.backupCheckbox.setMinimumSize(QSize(0, 0))
        self.backupCheckbox.setStyleSheet(u"margin-left: 9px;")

        self.Step50.addWidget(self.backupCheckbox)

        self.separator = QFrame(self.centralwidget)
        self.separator.setObjectName(u"separator")
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)

        self.Step50.addWidget(self.separator)

        self.Step5 = QLabel(self.centralwidget)
        self.Step5.setObjectName(u"Step5")
        self.Step5.setStyleSheet(u"margin-left: 9px;")

        self.Step50.addWidget(self.Step5)

        self.Buttons = QHBoxLayout()
        self.Buttons.setObjectName(u"Buttons")
        self.Buttons.setSizeConstraint(QLayout.SetFixedSize)
        self.renameButton = QPushButton(self.centralwidget)
        self.renameButton.setObjectName(u"renameButton")
        self.renameButton.setMinimumSize(QSize(0, 26))

        self.Buttons.addWidget(self.renameButton)

        self.exitButton = QPushButton(self.centralwidget)
        self.exitButton.setObjectName(u"exitButton")
        self.exitButton.setMinimumSize(QSize(0, 26))

        self.Buttons.addWidget(self.exitButton)


        self.Step50.addLayout(self.Buttons)


        self.gridLayout_2.addLayout(self.Step50, 8, 1, 1, 1)

        self.Step2 = QGroupBox(self.centralwidget)
        self.Step2.setObjectName(u"Step2")
        sizePolicy.setHeightForWidth(self.Step2.sizePolicy().hasHeightForWidth())
        self.Step2.setSizePolicy(sizePolicy)
        self.Step2.setMinimumSize(QSize(0, 0))
        self.Step2.setMaximumSize(QSize(16777215, 200))
        self.Step2.setAutoFillBackground(False)
        self.horizontalLayout_3 = QHBoxLayout(self.Step2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.allFilesCheckbox = QCheckBox(self.Step2)
        self.allFilesCheckbox.setObjectName(u"allFilesCheckbox")
        self.allFilesCheckbox.setMinimumSize(QSize(0, 0))
        self.allFilesCheckbox.setCursor(QCursor(Qt.ArrowCursor))
        self.allFilesCheckbox.setChecked(True)

        self.verticalLayout.addWidget(self.allFilesCheckbox)

        self.horizontalSpacer = QSpacerItem(40, 8, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.horizontalSpacer)

        self.commonFilesCheckbox = QCheckBox(self.Step2)
        self.commonFilesCheckbox.setObjectName(u"commonFilesCheckbox")
        self.commonFilesCheckbox.setMinimumSize(QSize(0, 0))
        self.commonFilesCheckbox.setCursor(QCursor(Qt.ArrowCursor))
        self.commonFilesCheckbox.setCheckable(True)
        self.commonFilesCheckbox.setChecked(False)
        self.commonFilesCheckbox.setAutoExclusive(False)

        self.verticalLayout.addWidget(self.commonFilesCheckbox)

        self.commonFilesList = QListWidget(self.Step2)
        self.commonFilesList.setObjectName(u"commonFilesList")
        self.commonFilesList.setEnabled(False)
        self.commonFilesList.setFont(font)
        self.commonFilesList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.commonFilesList.setSpacing(1)
        self.commonFilesList.setViewMode(QListView.ListMode)
        self.commonFilesList.setUniformItemSizes(False)
        self.commonFilesList.setWordWrap(False)
        self.commonFilesList.setSelectionRectVisible(True)

        self.verticalLayout.addWidget(self.commonFilesList)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.specificFilesLine = QLineEdit(self.Step2)
        self.specificFilesLine.setObjectName(u"specificFilesLine")
        self.specificFilesLine.setEnabled(False)
        self.specificFilesLine.setMinimumSize(QSize(0, 24))
        self.specificFilesLine.setFont(font)

        self.gridLayout.addWidget(self.specificFilesLine, 1, 0, 1, 1)

        self.specificFilesCheckbox = QCheckBox(self.Step2)
        self.specificFilesCheckbox.setObjectName(u"specificFilesCheckbox")
        self.specificFilesCheckbox.setMinimumSize(QSize(0, 0))
        self.specificFilesCheckbox.setCursor(QCursor(Qt.ArrowCursor))

        self.gridLayout.addWidget(self.specificFilesCheckbox, 0, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.specificFilesAddButton = QPushButton(self.Step2)
        self.specificFilesAddButton.setObjectName(u"specificFilesAddButton")
        self.specificFilesAddButton.setEnabled(False)
        self.specificFilesAddButton.setStyleSheet(u"")
        self.specificFilesAddButton.setIconSize(QSize(24, 20))

        self.horizontalLayout.addWidget(self.specificFilesAddButton)

        self.specificFilesClearButton = QPushButton(self.Step2)
        self.specificFilesClearButton.setObjectName(u"specificFilesClearButton")
        self.specificFilesClearButton.setEnabled(False)
        self.specificFilesClearButton.setStyleSheet(u"")
        self.specificFilesClearButton.setIconSize(QSize(24, 20))

        self.horizontalLayout.addWidget(self.specificFilesClearButton)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.specificFilesList = QListWidget(self.Step2)
        self.specificFilesList.setObjectName(u"specificFilesList")
        self.specificFilesList.setEnabled(False)
        sizePolicy.setHeightForWidth(self.specificFilesList.sizePolicy().hasHeightForWidth())
        self.specificFilesList.setSizePolicy(sizePolicy)
        self.specificFilesList.setFont(font)
        self.specificFilesList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.specificFilesList.setProperty("showDropIndicator", False)
        self.specificFilesList.setSelectionMode(QAbstractItemView.NoSelection)
        self.specificFilesList.setResizeMode(QListView.Fixed)
        self.specificFilesList.setSpacing(1)
        self.specificFilesList.setViewMode(QListView.ListMode)
        self.specificFilesList.setUniformItemSizes(False)
        self.specificFilesList.setWordWrap(False)
        self.specificFilesList.setSelectionRectVisible(True)

        self.gridLayout.addWidget(self.specificFilesList, 3, 0, 1, 2)


        self.horizontalLayout_3.addLayout(self.gridLayout)


        self.gridLayout_2.addWidget(self.Step2, 5, 1, 1, 1)

        self.Frame = QVBoxLayout()
        self.Frame.setObjectName(u"Frame")
        self.Frame.setSizeConstraint(QLayout.SetFixedSize)
        self.filesList = QTableWidget(self.centralwidget)
        if (self.filesList.columnCount() < 5):
            self.filesList.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.filesList.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.filesList.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.filesList.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.filesList.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.filesList.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.filesList.setObjectName(u"filesList")
        self.filesList.setEnabled(True)
        sizePolicy.setHeightForWidth(self.filesList.sizePolicy().hasHeightForWidth())
        self.filesList.setSizePolicy(sizePolicy)
        self.filesList.setMaximumSize(QSize(500, 16777215))
        self.filesList.setFrameShape(QFrame.Box)
        self.filesList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.filesList.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.filesList.setAutoScroll(True)
        self.filesList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filesList.setTabKeyNavigation(False)
        self.filesList.setProperty("showDropIndicator", False)
        self.filesList.setDragDropOverwriteMode(False)
        self.filesList.setAlternatingRowColors(False)
        self.filesList.setSelectionMode(QAbstractItemView.NoSelection)
        self.filesList.setTextElideMode(Qt.ElideLeft)
        self.filesList.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.filesList.setShowGrid(False)
        self.filesList.setGridStyle(Qt.SolidLine)
        self.filesList.setSortingEnabled(True)
        self.filesList.setWordWrap(False)
        self.filesList.setCornerButtonEnabled(True)
        self.filesList.setRowCount(0)
        self.filesList.setColumnCount(5)
        self.filesList.horizontalHeader().setVisible(True)
        self.filesList.horizontalHeader().setCascadingSectionResizes(True)
        self.filesList.horizontalHeader().setMinimumSectionSize(80)
        self.filesList.horizontalHeader().setDefaultSectionSize(90)
        self.filesList.horizontalHeader().setHighlightSections(False)
        self.filesList.horizontalHeader().setStretchLastSection(False)
        self.filesList.verticalHeader().setVisible(False)
        self.filesList.verticalHeader().setCascadingSectionResizes(False)
        self.filesList.verticalHeader().setMinimumSectionSize(26)
        self.filesList.verticalHeader().setDefaultSectionSize(26)
        self.filesList.verticalHeader().setHighlightSections(False)
        self.filesList.verticalHeader().setProperty("showSortIndicator", False)
        self.filesList.verticalHeader().setStretchLastSection(False)

        self.Frame.addWidget(self.filesList)


        self.gridLayout_2.addLayout(self.Frame, 0, 6, 9, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1111, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuOptions = QMenu(self.menuBar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menuBar)
        QWidget.setTabOrder(self.helpButton, self.openFolderButton)
        QWidget.setTabOrder(self.openFolderButton, self.pathLine)
        QWidget.setTabOrder(self.pathLine, self.includeFoldersCheckbox)
        QWidget.setTabOrder(self.includeFoldersCheckbox, self.includeSubdirCheckbox)
        QWidget.setTabOrder(self.includeSubdirCheckbox, self.allFilesCheckbox)
        QWidget.setTabOrder(self.allFilesCheckbox, self.commonFilesCheckbox)
        QWidget.setTabOrder(self.commonFilesCheckbox, self.commonFilesList)
        QWidget.setTabOrder(self.commonFilesList, self.specificFilesCheckbox)
        QWidget.setTabOrder(self.specificFilesCheckbox, self.specificFilesLine)
        QWidget.setTabOrder(self.specificFilesLine, self.specificFilesAddButton)
        QWidget.setTabOrder(self.specificFilesAddButton, self.specificFilesClearButton)
        QWidget.setTabOrder(self.specificFilesClearButton, self.specificFilesList)
        QWidget.setTabOrder(self.specificFilesList, self.rulesCombo)
        QWidget.setTabOrder(self.rulesCombo, self.startSpin)
        QWidget.setTabOrder(self.startSpin, self.countSpin)
        QWidget.setTabOrder(self.countSpin, self.caseSentitiveCheckbox)
        QWidget.setTabOrder(self.caseSentitiveCheckbox, self.regexCheckbox)
        QWidget.setTabOrder(self.regexCheckbox, self.inneCombo)
        QWidget.setTabOrder(self.inneCombo, self.backupCheckbox)
        QWidget.setTabOrder(self.backupCheckbox, self.renameButton)
        QWidget.setTabOrder(self.renameButton, self.exitButton)
        QWidget.setTabOrder(self.exitButton, self.filesList)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuOptions.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAlways_backup_before_renaming)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuOptions.addAction(self.actionProtect_Paths)
        self.menuOptions.addSeparator()
        self.menuOptions.addAction(self.actionOpen_settings)

        self.retranslateUi(MainWindow)

        self.inneCombo.setCurrentIndex(0)
        self.rulesCombo.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionEnglish.setText(QCoreApplication.translate("MainWindow", u"English (en)", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionPortugues_BR.setText(QCoreApplication.translate("MainWindow", u"Portuguese (pt_BR)", None))
        self.actionAlways_backup_before_renaming.setText(QCoreApplication.translate("MainWindow", u"Always backup before renaming", None))
        self.actionProtect_Paths.setText(QCoreApplication.translate("MainWindow", u"Protect paths", None))
        self.actionOpen_Folder.setText(QCoreApplication.translate("MainWindow", u"Open Folder", None))
        self.actionOpen_settings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actiontest.setText(QCoreApplication.translate("MainWindow", u"test", None))
        self.Step4.setTitle(QCoreApplication.translate("MainWindow", u"Step 4: Choose some options", None))
        self.replaceLabel.setText(QCoreApplication.translate("MainWindow", u"... and replace with", None))
        self.inLabel.setText(QCoreApplication.translate("MainWindow", u"in", None))
        self.inneCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"Before", None))
        self.inneCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"After", None))

        self.findLabel.setText(QCoreApplication.translate("MainWindow", u"Find...", None))
        self.caseSentitiveCheckbox.setText(QCoreApplication.translate("MainWindow", u"Case Sensitive", None))
        self.regexCheckbox.setText(QCoreApplication.translate("MainWindow", u"Regular Expression", None))
        self.invalidLabel.setText("")
        self.helpButton.setText(QCoreApplication.translate("MainWindow", u"Welcome! If you need help, click me!", None))
        self.Step30.setTitle("")
        self.Step3.setText(QCoreApplication.translate("MainWindow", u"Step 3: Set the rules ", None))
        self.rulesCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"Add Text or Date", None))
        self.rulesCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"Replace File Name", None))
        self.rulesCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"Replace File Extension", None))
        self.rulesCombo.setItemText(3, QCoreApplication.translate("MainWindow", u"Make sequential", None))

        self.startLabel.setText(QCoreApplication.translate("MainWindow", u"Start at", None))
        self.countLabel.setText(QCoreApplication.translate("MainWindow", u"Count by", None))
        self.Step1.setTitle(QCoreApplication.translate("MainWindow", u"Step 1: Select the folder where the files are located", None))
        self.openFolderButton.setText("")
        self.includeFoldersCheckbox.setText(QCoreApplication.translate("MainWindow", u"Include folders", None))
        self.includeSubdirCheckbox.setText(QCoreApplication.translate("MainWindow", u"Include files in subdirectories", None))
        self.backupCheckbox.setText(QCoreApplication.translate("MainWindow", u"Backup files before renaming", None))
        self.Step5.setText(QCoreApplication.translate("MainWindow", u"Step 5: Rename them", None))
        self.renameButton.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.exitButton.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.Step2.setTitle(QCoreApplication.translate("MainWindow", u"Step 2: Select the types of files to rename", None))
        self.allFilesCheckbox.setText(QCoreApplication.translate("MainWindow", u"All types of files", None))
#if QT_CONFIG(whatsthis)
        self.commonFilesCheckbox.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.commonFilesCheckbox.setText(QCoreApplication.translate("MainWindow", u"Common types of files:", None))
        self.specificFilesLine.setText("")
        self.specificFilesLine.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ex: mkv", None))
#if QT_CONFIG(whatsthis)
        self.specificFilesCheckbox.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.specificFilesCheckbox.setText(QCoreApplication.translate("MainWindow", u"Specific types of files:", None))
        self.specificFilesAddButton.setText("")
        self.specificFilesClearButton.setText("")
        ___qtablewidgetitem = self.filesList.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"File name", None));
        ___qtablewidgetitem1 = self.filesList.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"New file name", None));
        ___qtablewidgetitem2 = self.filesList.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Extension", None));
        ___qtablewidgetitem3 = self.filesList.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Path", None));
        ___qtablewidgetitem4 = self.filesList.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Size", None));
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

