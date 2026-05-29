# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(794, 554)
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"QMainWindow, QWidget {\n"
"    background-color: #202124;\n"
"    color: #eeeeee;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #eeeeee;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLineEdit, QPlainTextEdit {\n"
"    background-color: #2b2d31;\n"
"    color: #f2f2f2;\n"
"    border: 1px solid #555b63;\n"
"    border-radius: 6px;\n"
"    padding: 4px 6px;\n"
"}\n"
"\n"
"QLineEdit:read-only, QPlainTextEdit:read-only {\n"
"    background-color: #25272b;\n"
"    color: #dcdcdc;\n"
"}\n"
"\n"
"QListWidget {\n"
"    background-color: #181a1f;\n"
"    color: #eeeeee;\n"
"    border: 1px solid #555b63;\n"
"    border-radius: 8px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 5px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #2d89ef;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #2d89ef;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius:"
                        " 7px;\n"
"    padding: 6px 12px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3b97ff;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1f6fc7;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #4a4a4a;\n"
"    color: #9a9a9a;\n"
"}\n"
"\n"
"QStatusBar {\n"
"    background-color: #202124;\n"
"    color: #cccccc;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.logListWidget = QListWidget(self.centralwidget)
        self.logListWidget.setObjectName(u"logListWidget")
        self.logListWidget.setGeometry(QRect(30, 110, 461, 371))
        self.logListWidget.setFont(font)
        self.remoteHostLineEdit = QLineEdit(self.centralwidget)
        self.remoteHostLineEdit.setObjectName(u"remoteHostLineEdit")
        self.remoteHostLineEdit.setGeometry(QRect(590, 130, 181, 26))
        self.remoteHostLineEdit.setFont(font)
        self.remoteHostLineEdit.setReadOnly(True)
        self.previousButton = QPushButton(self.centralwidget)
        self.previousButton.setObjectName(u"previousButton")
        self.previousButton.setGeometry(QRect(30, 490, 81, 26))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.previousButton.setFont(font1)
        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setObjectName(u"nextButton")
        self.nextButton.setGeometry(QRect(410, 490, 81, 26))
        self.nextButton.setFont(font1)
        self.remoteHostLabel = QLabel(self.centralwidget)
        self.remoteHostLabel.setObjectName(u"remoteHostLabel")
        self.remoteHostLabel.setGeometry(QRect(500, 130, 81, 16))
        self.remoteHostLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.timestampLabelsWidget = QWidget(self.centralwidget)
        self.timestampLabelsWidget.setObjectName(u"timestampLabelsWidget")
        self.timestampLabelsWidget.setGeometry(QRect(510, 190, 75, 101))
        self.timestampLabelsWidget.setFont(font)
        self.verticalLayout = QVBoxLayout(self.timestampLabelsWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.dateLabel = QLabel(self.timestampLabelsWidget)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.dateLabel)

        self.timeLabel = QLabel(self.timestampLabelsWidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.timeLabel)

        self.timezoneLabel = QLabel(self.timestampLabelsWidget)
        self.timezoneLabel.setObjectName(u"timezoneLabel")
        self.timezoneLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout.addWidget(self.timezoneLabel)

        self.timestampFieldsWidget = QWidget(self.centralwidget)
        self.timestampFieldsWidget.setObjectName(u"timestampFieldsWidget")
        self.timestampFieldsWidget.setGeometry(QRect(590, 190, 181, 101))
        self.timestampFieldsWidget.setFont(font)
        self.verticalLayout_5 = QVBoxLayout(self.timestampFieldsWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.dateLineEdit = QLineEdit(self.timestampFieldsWidget)
        self.dateLineEdit.setObjectName(u"dateLineEdit")
        self.dateLineEdit.setFont(font)
        self.dateLineEdit.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.dateLineEdit)

        self.timeLineEdit = QLineEdit(self.timestampFieldsWidget)
        self.timeLineEdit.setObjectName(u"timeLineEdit")
        self.timeLineEdit.setFont(font)
        self.timeLineEdit.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.timeLineEdit)

        self.timezoneLineEdit = QLineEdit(self.timestampFieldsWidget)
        self.timezoneLineEdit.setObjectName(u"timezoneLineEdit")
        self.timezoneLineEdit.setFont(font)
        self.timezoneLineEdit.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.timezoneLineEdit)

        self.fileSelectionWidget = QWidget(self.centralwidget)
        self.fileSelectionWidget.setObjectName(u"fileSelectionWidget")
        self.fileSelectionWidget.setGeometry(QRect(30, 30, 741, 32))
        self.fileSelectionWidget.setFont(font)
        self.horizontalLayout = QHBoxLayout(self.fileSelectionWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.selectedFileLineEdit = QLineEdit(self.fileSelectionWidget)
        self.selectedFileLineEdit.setObjectName(u"selectedFileLineEdit")
        self.selectedFileLineEdit.setFont(font)
        self.selectedFileLineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.selectedFileLineEdit)

        self.browseButton = QPushButton(self.fileSelectionWidget)
        self.browseButton.setObjectName(u"browseButton")
        self.browseButton.setFont(font1)

        self.horizontalLayout.addWidget(self.browseButton)

        self.toFilterWidget = QWidget(self.centralwidget)
        self.toFilterWidget.setObjectName(u"toFilterWidget")
        self.toFilterWidget.setGeometry(QRect(260, 70, 245, 31))
        self.horizontalLayout_2 = QHBoxLayout(self.toFilterWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.toLabel = QLabel(self.toFilterWidget)
        self.toLabel.setObjectName(u"toLabel")
        self.toLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.toLabel)

        self.DateTo = QDateTimeEdit(self.toFilterWidget)
        self.DateTo.setObjectName(u"DateTo")
        self.DateTo.setDateTime(QDateTime(QDate(2026, 5, 1), QTime(0, 0, 0)))
        self.DateTo.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.DateTo)

        self.fromFilterWidget = QWidget(self.centralwidget)
        self.fromFilterWidget.setObjectName(u"fromFilterWidget")
        self.fromFilterWidget.setGeometry(QRect(30, 70, 233, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.fromFilterWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.fromLabel = QLabel(self.fromFilterWidget)
        self.fromLabel.setObjectName(u"fromLabel")

        self.horizontalLayout_3.addWidget(self.fromLabel)

        self.DateFrom = QDateTimeEdit(self.fromFilterWidget)
        self.DateFrom.setObjectName(u"DateFrom")
        self.DateFrom.setDateTime(QDateTime(QDate(2026, 5, 1), QTime(0, 0, 0)))
        self.DateFrom.setCalendarPopup(True)

        self.horizontalLayout_3.addWidget(self.DateFrom)

        self.resourceLabel = QLabel(self.centralwidget)
        self.resourceLabel.setObjectName(u"resourceLabel")
        self.resourceLabel.setGeometry(QRect(530, 450, 52, 18))
        self.resourceLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.resourcePlainTextEdit = QPlainTextEdit(self.centralwidget)
        self.resourcePlainTextEdit.setObjectName(u"resourcePlainTextEdit")
        self.resourcePlainTextEdit.setGeometry(QRect(530, 470, 251, 51))
        self.resourcePlainTextEdit.setFont(font)
        self.resourcePlainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.resourcePlainTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.resourcePlainTextEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.resourcePlainTextEdit.setReadOnly(True)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(510, 310, 261, 127))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.statusCodeLabel = QLabel(self.layoutWidget)
        self.statusCodeLabel.setObjectName(u"statusCodeLabel")
        self.statusCodeLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.statusCodeLabel)

        self.methodLabel = QLabel(self.layoutWidget)
        self.methodLabel.setObjectName(u"methodLabel")
        self.methodLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.methodLabel)

        self.sizeLabel = QLabel(self.layoutWidget)
        self.sizeLabel.setObjectName(u"sizeLabel")
        self.sizeLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_3.addWidget(self.sizeLabel)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.statusCodeLineEdit = QLineEdit(self.layoutWidget)
        self.statusCodeLineEdit.setObjectName(u"statusCodeLineEdit")
        self.statusCodeLineEdit.setFont(font)
        self.statusCodeLineEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.statusCodeLineEdit)

        self.methodLineEdit = QLineEdit(self.layoutWidget)
        self.methodLineEdit.setObjectName(u"methodLineEdit")
        self.methodLineEdit.setFont(font)
        self.methodLineEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.methodLineEdit)

        self.sizeLineEdit = QLineEdit(self.layoutWidget)
        self.sizeLineEdit.setObjectName(u"sizeLineEdit")
        self.sizeLineEdit.setFont(font)
        self.sizeLineEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.sizeLineEdit)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.mainStatusBar = QStatusBar(MainWindow)
        self.mainStatusBar.setObjectName(u"mainStatusBar")
        MainWindow.setStatusBar(self.mainStatusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.previousButton.setText(QCoreApplication.translate("MainWindow", u"Prev", None))
        self.nextButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.remoteHostLabel.setText(QCoreApplication.translate("MainWindow", u"Remote host", None))
        self.dateLabel.setText(QCoreApplication.translate("MainWindow", u"Date", None))
        self.timeLabel.setText(QCoreApplication.translate("MainWindow", u"Time", None))
        self.timezoneLabel.setText(QCoreApplication.translate("MainWindow", u"Timezone", None))
        self.browseButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.toLabel.setText(QCoreApplication.translate("MainWindow", u"To", None))
        self.DateTo.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm:ss.zzz", None))
        self.fromLabel.setText(QCoreApplication.translate("MainWindow", u"From", None))
        self.DateFrom.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm:ss.zzz", None))
        self.resourceLabel.setText(QCoreApplication.translate("MainWindow", u"Resource", None))
        self.statusCodeLabel.setText(QCoreApplication.translate("MainWindow", u"Status code", None))
        self.methodLabel.setText(QCoreApplication.translate("MainWindow", u"Method", None))
        self.sizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size", None))
    # retranslateUi

