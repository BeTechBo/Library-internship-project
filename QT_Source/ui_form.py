# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(0, 100))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_8 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"Impact"])
        font.setPointSize(72)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.uploadFilesButton = QPushButton(self.centralwidget)
        self.uploadFilesButton.setObjectName(u"uploadFilesButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uploadFilesButton.sizePolicy().hasHeightForWidth())
        self.uploadFilesButton.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Impact"])
        font1.setPointSize(36)
        self.uploadFilesButton.setFont(font1)

        self.verticalLayout_6.addWidget(self.uploadFilesButton)

        self.beginLabelingButton = QPushButton(self.centralwidget)
        self.beginLabelingButton.setObjectName(u"beginLabelingButton")
        sizePolicy.setHeightForWidth(self.beginLabelingButton.sizePolicy().hasHeightForWidth())
        self.beginLabelingButton.setSizePolicy(sizePolicy)
        self.beginLabelingButton.setFont(font1)

        self.verticalLayout_6.addWidget(self.beginLabelingButton)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.verticalLayout_7.setStretch(0, 3)
        self.verticalLayout_7.setStretch(1, 2)

        self.verticalLayout_8.addLayout(self.verticalLayout_7)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Unlabeled Files", None))
        self.uploadFilesButton.setText(QCoreApplication.translate("MainWindow", u"Upload Files", None))
        self.beginLabelingButton.setText(QCoreApplication.translate("MainWindow", u"Begin Labeling", None))
    # retranslateUi

