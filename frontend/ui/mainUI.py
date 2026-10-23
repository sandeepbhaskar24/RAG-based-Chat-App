# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainUInGoXrT.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

from ui_controllers.auto_grow_text_edit import AutoGrowTextEdit
from ui_controllers.py_toggle import PyToggle
from ui_controllers.sticky_search_button import StickyButton

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(990, 643)
        MainWindow.setStyleSheet(u"QMainWindow{\n"
"	background-color: rgb(45, 45, 45);\n"
"	border-radius:10px;\n"
"}\n"
"\n"
"/* Styles for the vertical scrollbar */\n"
"\n"
"QScrollBar:vertical {\n"
"	border-radius:4px;\n"
"    background-color: rgb(60, 60, 91);/* #F0F0F0; */\n"
"    width: 8px;\n"
"    margin: 0px 0px 20px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    /*background-color: #4F9FFE;*/\n"
"	background-color:rgb(80, 80, 122);\n"
"	border-radius:4px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    /*background-color: #4F9FFE;*/\n"
"	/*background-color: rgb(170, 0, 255);*/\n"
"	background-color:rgb(0, 128, 255);\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical {\n"
"    height: 0px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    width: 0px;\n"
""
                        "    height: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"\n"
"/*stylesheet for horizontal scrollbar*/\n"
"\n"
"\n"
"QScrollBar:horizontal {\n"
"	border-radius:5px;\n"
"    background-color: rgb(60, 60, 91);/* #F0F0F0; */\n"
"    width: 12px;\n"
"    margin: 0px 0px 0px 0px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal {\n"
"    /*background-color: #4F9FFE;*/\n"
"	background-color:rgb(80, 80, 122);\n"
"	border-radius:5px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal:hover {\n"
"    /*background-color: #4F9FFE;*/\n"
"	background-color: rgb(170, 0, 255);;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"    height: 0px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"    height: 0px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::left-arrow:horizontal, QScr"
                        "ollBar::right-arrow:horizontal {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"    background: none;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"border-radius:10px;")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.drop_shadow_frame = QFrame(self.centralwidget)
        self.drop_shadow_frame.setObjectName(u"drop_shadow_frame")
        self.drop_shadow_frame.setStyleSheet(u"QFrame{\n"
"	border-radius:10px;\n"
"}")
        self.drop_shadow_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.drop_shadow_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.drop_shadow_frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Top_Bar = QFrame(self.drop_shadow_frame)
        self.Top_Bar.setObjectName(u"Top_Bar")
        self.Top_Bar.setMaximumSize(QSize(16777215, 40))
        self.Top_Bar.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(38, 42, 52);\n"
"}")
        self.Top_Bar.setFrameShape(QFrame.Shape.StyledPanel)
        self.Top_Bar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.Top_Bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.toggle_frame = QFrame(self.Top_Bar)
        self.toggle_frame.setObjectName(u"toggle_frame")
        self.toggle_frame.setMaximumSize(QSize(70, 16777215))
        self.toggle_frame.setStyleSheet(u"QFrame{\n"
"	border-radius:0px;\n"
"	border-top-left-radius:10px;\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgba(79, 159, 254, 220);\n"
"}")
        self.toggle_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.toggle_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.toggle_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.toggle_button = QPushButton(self.toggle_frame)
        self.toggle_button.setObjectName(u"toggle_button")
        self.toggle_button.setMinimumSize(QSize(0, 40))
        self.toggle_button.setMaximumSize(QSize(80, 16777215))
        self.toggle_button.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"../Reqs/menu-50 copy.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toggle_button.setIcon(icon1)
        self.toggle_button.setIconSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.toggle_button)


        self.horizontalLayout.addWidget(self.toggle_frame)

        self.top_bar_frame = QFrame(self.Top_Bar)
        self.top_bar_frame.setObjectName(u"top_bar_frame")
        self.top_bar_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.top_bar_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.top_bar_frame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(10, 0, 0, 0)
        self.icon = QPushButton(self.top_bar_frame)
        self.icon.setObjectName(u"icon")
        self.icon.setMinimumSize(QSize(0, 35))
        self.icon.setMaximumSize(QSize(40, 16777215))
        self.icon.setStyleSheet(u"background-color: rgb(38, 42, 52);\n"
"border:none;")
        icon2 = QIcon()
        icon2.addFile(u"../Reqs/app_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.icon.setIcon(icon2)
        self.icon.setIconSize(QSize(24, 24))

        self.horizontalLayout_5.addWidget(self.icon)

        self.status_bar = QLabel(self.top_bar_frame)
        self.status_bar.setObjectName(u"status_bar")
        font = QFont()
        font.setFamilies([u"Roboto"])
        font.setPointSize(10)
        font.setBold(False)
        self.status_bar.setFont(font)
        self.status_bar.setStyleSheet(u"color: rgb(220, 220, 220);")

        self.horizontalLayout_5.addWidget(self.status_bar)


        self.horizontalLayout.addWidget(self.top_bar_frame)

        self.top_bar_button_frame = QFrame(self.Top_Bar)
        self.top_bar_button_frame.setObjectName(u"top_bar_button_frame")
        self.top_bar_button_frame.setMinimumSize(QSize(200, 0))
        self.top_bar_button_frame.setMaximumSize(QSize(200, 16777215))
        self.top_bar_button_frame.setStyleSheet(u"border-radius:0px;\n"
"border-top-right-radius:10px;\n"
"")
        self.top_bar_button_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.top_bar_button_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.top_bar_button_frame)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.button_minimize = QPushButton(self.top_bar_button_frame)
        self.button_minimize.setObjectName(u"button_minimize")
        self.button_minimize.setMinimumSize(QSize(0, 40))
        self.button_minimize.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	border-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(45, 50, 62);\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"../Reqs/subtract-24 copy.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_minimize.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.button_minimize)

        self.button_restore = QPushButton(self.top_bar_button_frame)
        self.button_restore.setObjectName(u"button_restore")
        self.button_restore.setEnabled(True)
        self.button_restore.setMinimumSize(QSize(0, 40))
        self.button_restore.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	border-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:  rgb(45, 50, 62);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"../Reqs/maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_restore.setIcon(icon4)

        self.horizontalLayout_3.addWidget(self.button_restore)

        self.button_close = QPushButton(self.top_bar_button_frame)
        self.button_close.setObjectName(u"button_close")
        self.button_close.setMinimumSize(QSize(0, 40))
        self.button_close.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	border-radius:0px;\n"
"	border-top-right-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgb(212, 58, 212)\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u"../Reqs/close-24 copy.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_close.setIcon(icon5)

        self.horizontalLayout_3.addWidget(self.button_close)


        self.horizontalLayout.addWidget(self.top_bar_button_frame)


        self.verticalLayout_2.addWidget(self.Top_Bar)

        self.Content = QFrame(self.drop_shadow_frame)
        self.Content.setObjectName(u"Content")
        self.Content.setStyleSheet(u"border-bottom-left-radius:10px;\n"
"border-bottom-right-radius:10px;")
        self.Content.setFrameShape(QFrame.Shape.StyledPanel)
        self.Content.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.Content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggle_frame_left = QFrame(self.Content)
        self.toggle_frame_left.setObjectName(u"toggle_frame_left")
        self.toggle_frame_left.setMinimumSize(QSize(70, 0))
        self.toggle_frame_left.setMaximumSize(QSize(70, 16777215))
        self.toggle_frame_left.setStyleSheet(u"background-color: #272C36;\n"
"border-radius:0px;\n"
"border-bottom-left-radius:10px;\n"
"")
        self.toggle_frame_left.setFrameShape(QFrame.Shape.StyledPanel)
        self.toggle_frame_left.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.toggle_frame_left)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_status = QFrame(self.toggle_frame_left)
        self.frame_status.setObjectName(u"frame_status")
        self.frame_status.setMinimumSize(QSize(0, 50))
        self.frame_status.setMaximumSize(QSize(16777215, 50))
        self.frame_status.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.frame_status.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"	border-bottom: 1px solid rgba(255, 255, 255, 30);\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:5px;\n"
"}")
        self.frame_status.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_status.setFrameShadow(QFrame.Shadow.Raised)
        self.button_new_chat = QPushButton(self.frame_status)
        self.button_new_chat.setObjectName(u"button_new_chat")
        self.button_new_chat.setGeometry(QRect(5, 0, 231, 50))
        self.button_new_chat.setMinimumSize(QSize(70, 50))
        self.button_new_chat.setMaximumSize(QSize(16777215, 50))
        font1 = QFont()
        font1.setFamilies([u"Noto Sans"])
        font1.setPointSize(10)
        self.button_new_chat.setFont(font1)
        self.button_new_chat.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_new_chat.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.button_new_chat.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon6 = QIcon()
        icon6.addFile(u"../Reqs/new_chat.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_new_chat.setIcon(icon6)
        self.button_new_chat.setIconSize(QSize(32, 32))

        self.verticalLayout_3.addWidget(self.frame_status)

        self.label_7 = QLabel(self.toggle_frame_left)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 40))
        self.label_7.setStyleSheet(u"background:none;\n"
"border:none;\n"
"padding-left:10px;\n"
"color: rgba(255, 255, 255, 140);")

        self.verticalLayout_3.addWidget(self.label_7)

        self.frame_driver_protection_2 = QFrame(self.toggle_frame_left)
        self.frame_driver_protection_2.setObjectName(u"frame_driver_protection_2")
        self.frame_driver_protection_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_driver_protection_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_driver_protection_2)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.chat_history = QListWidget(self.frame_driver_protection_2)
        self.chat_history.setObjectName(u"chat_history")

        self.verticalLayout_10.addWidget(self.chat_history)


        self.verticalLayout_3.addWidget(self.frame_driver_protection_2)

        self.frame_settings = QFrame(self.toggle_frame_left)
        self.frame_settings.setObjectName(u"frame_settings")
        self.frame_settings.setMinimumSize(QSize(0, 60))
        self.frame_settings.setMaximumSize(QSize(16777215, 60))
        self.frame_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.frame_settings.setStyleSheet(u"QFrame{\n"
"	border-radius: 0px;\n"
"	border-top: 1px solid rgba(255, 255, 255, 30);\n"
"}\n"
"QFrame:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"	border:2px solid rgba(0, 159, 238, 140);\n"
"	border-radius:0px;\n"
"	border-bottom-left-radius:10px;\n"
"}")
        self.frame_settings.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_settings.setFrameShadow(QFrame.Shadow.Raised)
        self.button_settings = QPushButton(self.frame_settings)
        self.button_settings.setObjectName(u"button_settings")
        self.button_settings.setGeometry(QRect(-2, 0, 221, 60))
        self.button_settings.setMinimumSize(QSize(0, 60))
        self.button_settings.setMaximumSize(QSize(250, 250))
        self.button_settings.setFont(font1)
        self.button_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_settings.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color: rgba(255, 255, 255, 180);")
        icon7 = QIcon()
        icon7.addFile(u"../Reqs/settings-50 copy.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.button_settings.setIcon(icon7)
        self.button_settings.setIconSize(QSize(30, 30))

        self.verticalLayout_3.addWidget(self.frame_settings)


        self.horizontalLayout_4.addWidget(self.toggle_frame_left)

        self.content_page_frame = QFrame(self.Content)
        self.content_page_frame.setObjectName(u"content_page_frame")
        self.content_page_frame.setStyleSheet(u"background-color:#2C313C;\n"
"border-radius:0px;\n"
"border-bottom-right-radius:10px;\n"
"")
        self.content_page_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.content_page_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.content_page_frame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.content_page_frame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setStyleSheet(u"")
        self.new_chat_page = QWidget()
        self.new_chat_page.setObjectName(u"new_chat_page")
        self.new_chat_page.setEnabled(True)
        self.verticalLayout_5 = QVBoxLayout(self.new_chat_page)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.new_chat_page)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.frame_8)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_7.addWidget(self.frame_11)

        self.frame_9 = QFrame(self.frame_8)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(600, 0))
        self.frame_9.setMaximumSize(QSize(600, 16777215))
        font2 = QFont()
        font2.setFamilies([u"MingLiU_HKSCS-ExtB"])
        self.frame_9.setFont(font2)
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_9)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_12 = QFrame(self.frame_9)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label = QLabel(self.frame_12)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"background:none;\n"
"border:none;")
        self.label.setPixmap(QPixmap(u"../../../../.designer/backup/C:/Users/san76/.designer/backup/Reqs/protected.png"))
        self.label.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.horizontalLayout_8.addWidget(self.label)


        self.verticalLayout_6.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.frame_9)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 400))
        self.frame_13.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.labelProtection = QLabel(self.frame_13)
        self.labelProtection.setObjectName(u"labelProtection")
        self.labelProtection.setGeometry(QRect(120, 60, 382, 54))
        self.labelProtection.setMaximumSize(QSize(16777215, 80))
        font3 = QFont()
        font3.setFamilies([u"Roboto"])
        font3.setPointSize(30)
        self.labelProtection.setFont(font3)
        self.labelProtection.setStyleSheet(u"background:none;\n"
"border:none;\n"
"color:rgba(255, 255, 255, 180);")
        self.labelProtection.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.searchButton = StickyButton(self.frame_13)
        self.searchButton.setObjectName(u"searchButton")
        self.searchButton.setGeometry(QRect(550, 141, 45, 45))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QSize(45, 45))
        self.searchButton.setMaximumSize(QSize(45, 45))
        font4 = QFont()
        font4.setFamilies([u"Noto Sans Medium"])
        font4.setPointSize(10)
        self.searchButton.setFont(font4)
        self.searchButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.searchButton.setStyleSheet(u"QPushButton{\n"
"	background:none;\n"
"	border:none;\n"
"	color:rgba(255, 255, 255, 180);\n"
"	background-color: rgb(41, 44, 53);\n"
"	border-radius: 21px ;\n"
"	margin-top:3px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(45, 48, 58);\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u"../Reqs/search.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.searchButton.setIcon(icon8)
        self.searchButton.setIconSize(QSize(27, 27))
        self.addButton = StickyButton(self.frame_13)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setGeometry(QRect(12, 140, 51, 45))
        self.addButton.setMinimumSize(QSize(0, 45))
        self.addButton.setMaximumSize(QSize(160, 16777215))
        self.addButton.setFont(font4)
        self.addButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addButton.setStyleSheet(u"QPushButton{\n"
"	background:none;\n"
"	border:none;\n"
"	color:rgba(255, 255, 255, 180);\n"
"	border-radius: 21px ;\n"
"	margin-top:3px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(45, 48, 58);\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u"../Reqs/add_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addButton.setIcon(icon9)
        self.addButton.setIconSize(QSize(22, 22))
        self.text_prompt = AutoGrowTextEdit(self.frame_13)
        self.text_prompt.setObjectName(u"text_prompt")
        self.text_prompt.setEnabled(True)
        self.text_prompt.setGeometry(QRect(10, 140, 581, 50))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.text_prompt.sizePolicy().hasHeightForWidth())
        self.text_prompt.setSizePolicy(sizePolicy1)
        self.text_prompt.setMinimumSize(QSize(0, 50))
        self.text_prompt.setMaximumSize(QSize(16777215, 50))
        self.text_prompt.setSizeIncrement(QSize(0, 0))
        self.text_prompt.setBaseSize(QSize(0, 0))
        font5 = QFont()
        font5.setFamilies([u"Roboto"])
        font5.setPointSize(10)
        self.text_prompt.setFont(font5)
        self.text_prompt.setStyleSheet(u"QTextEdit{\n"
" 	border:2px solid rgb(41, 44, 53);\n"
"    border-radius:22px;\n"
"	background-color: rgb(41, 44, 53);\n"
"    color:rgba(255, 	255, 255, 210);\n"
"    padding-left:20px;\n"
"	padding-top:10px;\n"
"	padding-right:15px;\n"
"	padding-bottom:45px;\n"
"}\n"
"\n"
"QTextEdit:hover{\n"
"	border:2px solid rgb(220, 0, 220);\n"
"}\n"
"\n"
"QTextEdit:focus{\n"
"	border:2px solid rgb(85,170,255);\n"
"}")
        self.text_prompt.setFrameShape(QFrame.Shape.StyledPanel)
        self.text_prompt.setFrameShadow(QFrame.Shadow.Plain)
        self.text_prompt.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.text_prompt.raise_()
        self.labelProtection.raise_()
        self.addButton.raise_()
        self.searchButton.raise_()

        self.verticalLayout_6.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.frame_9)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_6.addWidget(self.frame_14)


        self.horizontalLayout_7.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_10)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_21 = QFrame(self.frame_10)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMaximumSize(QSize(16777215, 100))
        self.frame_21.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.frame_23 = QFrame(self.frame_21)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_16.addWidget(self.frame_23)

        self.frame_24 = QFrame(self.frame_21)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setMinimumSize(QSize(120, 40))
        self.frame_24.setMaximumSize(QSize(160, 16777215))
        self.frame_24.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.login_button = QPushButton(self.frame_24)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setMaximumSize(QSize(16777215, 30))
        font6 = QFont()
        font6.setFamilies([u"Roboto"])
        self.login_button.setFont(font6)
        self.login_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button.setStyleSheet(u"QPushButton{\n"
"	color: rgba(255, 255, 255, 200);\n"
"	background-color: rgb(48, 53, 65);\n"
"	\n"
"	border-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"	color:rgb(85, 170, 255);\n"
"	background-color:rgb(52, 57, 70)\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u"../Reqs/user.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.login_button.setIcon(icon10)
        self.login_button.setIconSize(QSize(20, 20))

        self.horizontalLayout_17.addWidget(self.login_button)


        self.horizontalLayout_16.addWidget(self.frame_24)


        self.verticalLayout_11.addWidget(self.frame_21)

        self.frame_22 = QFrame(self.frame_10)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_11.addWidget(self.frame_22)


        self.horizontalLayout_7.addWidget(self.frame_10)


        self.verticalLayout_5.addWidget(self.frame_8)

        self.stackedWidget.addWidget(self.new_chat_page)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        self.verticalLayout_4 = QVBoxLayout(self.settings_page)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_48 = QFrame(self.settings_page)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_48.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_48)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.frame_49 = QFrame(self.frame_48)
        self.frame_49.setObjectName(u"frame_49")
        self.frame_49.setMinimumSize(QSize(250, 0))
        self.frame_49.setMaximumSize(QSize(250, 16777215))
        self.frame_49.setStyleSheet(u"background-color: rgb(43, 47, 58)")
        self.frame_49.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_49.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.frame_49)
        self.verticalLayout_27.setSpacing(10)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.frame_51 = QFrame(self.frame_49)
        self.frame_51.setObjectName(u"frame_51")
        self.frame_51.setMaximumSize(QSize(16777215, 60))
        self.frame_51.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_51.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_51)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.label_32 = QLabel(self.frame_51)
        self.label_32.setObjectName(u"label_32")
        font7 = QFont()
        font7.setFamilies([u"Roboto"])
        font7.setPointSize(12)
        self.label_32.setFont(font7)
        self.label_32.setStyleSheet(u"color:rgba(255, 255, 255, 180);\n"
"padding-left: 45px;")
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_23.addWidget(self.label_32)


        self.verticalLayout_27.addWidget(self.frame_51)

        self.frame_25 = QFrame(self.frame_49)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setMaximumSize(QSize(16777215, 40))
        self.frame_25.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.acc_button = QPushButton(self.frame_25)
        self.acc_button.setObjectName(u"acc_button")
        self.acc_button.setMinimumSize(QSize(0, 40))
        font8 = QFont()
        font8.setFamilies([u"Roboto"])
        font8.setPointSize(11)
        self.acc_button.setFont(font8)
        self.acc_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.acc_button.setStyleSheet(u"QPushButton{\n"
"	border-radius:5px;\n"
"	color:rgb(180, 180, 180);\n"
"	text-align:left;\n"
"	padding-left:40px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgb(59, 66, 81);\n"
"	border:2px solid rgb(212, 58, 212);\n"
"	border-radius:5px;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color: rgb(0, 151, 227);\n"
"    color: rgb(180, 180, 180);;\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u"../Reqs/user2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.acc_button.setIcon(icon11)
        self.acc_button.setIconSize(QSize(25, 25))

        self.horizontalLayout_18.addWidget(self.acc_button)


        self.verticalLayout_27.addWidget(self.frame_25)

        self.frame_56 = QFrame(self.frame_49)
        self.frame_56.setObjectName(u"frame_56")
        self.frame_56.setMaximumSize(QSize(16777215, 40))
        self.frame_56.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_56.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frame_56)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.buttonDocs = QPushButton(self.frame_56)
        self.buttonDocs.setObjectName(u"buttonDocs")
        self.buttonDocs.setMinimumSize(QSize(0, 40))
        self.buttonDocs.setFont(font8)
        self.buttonDocs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonDocs.setStyleSheet(u"QPushButton{\n"
"	border-radius:5px;\n"
"	color:rgb(180, 180, 180);\n"
"	text-align:left;\n"
"	padding-left:40px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgb(59, 66, 81);\n"
"	border:2px solid rgb(212, 58, 212);\n"
"	border-radius:5px;\n"
"}")
        icon12 = QIcon()
        icon12.addFile(u"../Reqs/ui_.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.buttonDocs.setIcon(icon12)
        self.buttonDocs.setIconSize(QSize(25, 25))

        self.horizontalLayout_24.addWidget(self.buttonDocs)


        self.verticalLayout_27.addWidget(self.frame_56)

        self.frame_53 = QFrame(self.frame_49)
        self.frame_53.setObjectName(u"frame_53")
        self.frame_53.setMaximumSize(QSize(16777215, 40))
        self.frame_53.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_53.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_53)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.buttonUpdate = QPushButton(self.frame_53)
        self.buttonUpdate.setObjectName(u"buttonUpdate")
        self.buttonUpdate.setMinimumSize(QSize(0, 40))
        self.buttonUpdate.setFont(font8)
        self.buttonUpdate.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonUpdate.setStyleSheet(u"QPushButton{\n"
"	border-radius:5px;\n"
"	color:rgb(180, 180, 180);\n"
"	text-align:left;\n"
"	padding-left:40px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgb(59, 66, 81);\n"
"	border:2px solid rgb(212, 58, 212);\n"
"	border-radius:5px;\n"
"}")
        icon13 = QIcon()
        icon13.addFile(u"../Reqs/update_.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.buttonUpdate.setIcon(icon13)
        self.buttonUpdate.setIconSize(QSize(25, 25))

        self.horizontalLayout_26.addWidget(self.buttonUpdate)


        self.verticalLayout_27.addWidget(self.frame_53)

        self.frame_54 = QFrame(self.frame_49)
        self.frame_54.setObjectName(u"frame_54")
        self.frame_54.setMaximumSize(QSize(16777215, 40))
        self.frame_54.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_54.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.frame_54)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.buttonAbout = QPushButton(self.frame_54)
        self.buttonAbout.setObjectName(u"buttonAbout")
        self.buttonAbout.setMinimumSize(QSize(0, 40))
        self.buttonAbout.setFont(font8)
        self.buttonAbout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.buttonAbout.setStyleSheet(u"QPushButton{\n"
"	border-radius:5px;\n"
"	color:rgb(180, 180, 180);\n"
"	text-align:left;\n"
"	padding-left:40px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgb(59, 66, 81);\n"
"	border:2px solid rgb(212, 58, 212);\n"
"	border-radius:5px;\n"
"}")
        icon14 = QIcon()
        icon14.addFile(u"../Reqs/about_.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.buttonAbout.setIcon(icon14)
        self.buttonAbout.setIconSize(QSize(25, 25))

        self.horizontalLayout_27.addWidget(self.buttonAbout)


        self.verticalLayout_27.addWidget(self.frame_54)

        self.frame_57 = QFrame(self.frame_49)
        self.frame_57.setObjectName(u"frame_57")
        self.frame_57.setMaximumSize(QSize(16777215, 50))
        self.frame_57.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_57.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_57)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_27.addWidget(self.frame_57)

        self.frame_55 = QFrame(self.frame_49)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_55.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_27.addWidget(self.frame_55)


        self.horizontalLayout_22.addWidget(self.frame_49)

        self.frame_50 = QFrame(self.frame_48)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_50.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_50)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.setting_pages = QStackedWidget(self.frame_50)
        self.setting_pages.setObjectName(u"setting_pages")
        self.setting_pages.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.Documents_page = QWidget()
        self.Documents_page.setObjectName(u"Documents_page")
        self.verticalLayout_19 = QVBoxLayout(self.Documents_page)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.frame_62 = QFrame(self.Documents_page)
        self.frame_62.setObjectName(u"frame_62")
        self.frame_62.setMaximumSize(QSize(16777215, 50))
        font9 = QFont()
        font9.setPointSize(10)
        self.frame_62.setFont(font9)
        self.frame_62.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_62.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_62)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(25, -1, -1, 0)
        self.label_8 = QLabel(self.frame_62)
        self.label_8.setObjectName(u"label_8")
        font10 = QFont()
        font10.setFamilies([u"Roboto Medium"])
        font10.setPointSize(12)
        self.label_8.setFont(font10)
        self.label_8.setStyleSheet(u"color: rgb(190, 190, 190);")

        self.horizontalLayout_35.addWidget(self.label_8)


        self.verticalLayout_19.addWidget(self.frame_62)

        self.frame_63 = QFrame(self.Documents_page)
        self.frame_63.setObjectName(u"frame_63")
        self.frame_63.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_63.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_63)
        self.horizontalLayout_36.setSpacing(0)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.frame_65 = QFrame(self.frame_63)
        self.frame_65.setObjectName(u"frame_65")
        self.frame_65.setMaximumSize(QSize(320, 16777215))
        self.frame_65.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_65.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_36.addWidget(self.frame_65)

        self.frame_64 = QFrame(self.frame_63)
        self.frame_64.setObjectName(u"frame_64")
        self.frame_64.setMinimumSize(QSize(650, 0))
        self.frame_64.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_64.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frame_64)
        self.verticalLayout_22.setSpacing(5)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(-1, 20, -1, -1)
        self.label_19 = QLabel(self.frame_64)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMaximumSize(QSize(16777215, 30))
        font11 = QFont()
        font11.setFamilies([u"Roboto Medium"])
        font11.setPointSize(11)
        self.label_19.setFont(font11)
        self.label_19.setStyleSheet(u"color: rgb(218, 218, 218);\n"
"padding-left: 50px;")

        self.verticalLayout_22.addWidget(self.label_19)

        self.frame_73 = QFrame(self.frame_64)
        self.frame_73.setObjectName(u"frame_73")
        self.frame_73.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_73.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.frame_73)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(0, -1, 0, -1)
        self.docs_list_frame = QFrame(self.frame_73)
        self.docs_list_frame.setObjectName(u"docs_list_frame")
        font12 = QFont()
        font12.setBold(False)
        self.docs_list_frame.setFont(font12)
        self.docs_list_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.docs_list_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_28.addWidget(self.docs_list_frame)


        self.verticalLayout_22.addWidget(self.frame_73)


        self.horizontalLayout_36.addWidget(self.frame_64)

        self.frame_66 = QFrame(self.frame_63)
        self.frame_66.setObjectName(u"frame_66")
        self.frame_66.setMaximumSize(QSize(320, 16777215))
        self.frame_66.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_66.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_36.addWidget(self.frame_66)


        self.verticalLayout_19.addWidget(self.frame_63)

        self.setting_pages.addWidget(self.Documents_page)
        self.account_page = QWidget()
        self.account_page.setObjectName(u"account_page")
        self.horizontalLayout_19 = QHBoxLayout(self.account_page)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.frame_27 = QFrame(self.account_page)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setMaximumSize(QSize(400, 16777215))
        self.frame_27.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_19.addWidget(self.frame_27)

        self.frame_28 = QFrame(self.account_page)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setMinimumSize(QSize(600, 0))
        self.frame_28.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_28)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 20, 0, 0)
        self.frame_29 = QFrame(self.frame_28)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setMaximumSize(QSize(16777215, 70))
        self.frame_29.setStyleSheet(u"")
        self.frame_29.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(5, -1, 20, -1)
        self.account_label = QLabel(self.frame_29)
        self.account_label.setObjectName(u"account_label")
        font13 = QFont()
        font13.setFamilies([u"Roboto"])
        font13.setPointSize(13)
        self.account_label.setFont(font13)
        self.account_label.setStyleSheet(u"color:rgb(180, 180, 180);\n"
"background:transparent;")

        self.horizontalLayout_20.addWidget(self.account_label)

        self.logged_in_label = QLabel(self.frame_29)
        self.logged_in_label.setObjectName(u"logged_in_label")
        self.logged_in_label.setFont(font5)
        self.logged_in_label.setStyleSheet(u"color: rgba(255, 0, 0, 200);")
        self.logged_in_label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_20.addWidget(self.logged_in_label)


        self.verticalLayout_12.addWidget(self.frame_29)

        self.frame_30 = QFrame(self.frame_28)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_30)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.frame_32 = QFrame(self.frame_30)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setMaximumSize(QSize(16777215, 100))
        self.frame_32.setStyleSheet(u"#frame_32{\n"
"	background-color: rgb(52, 58, 71);\n"
"	border-radius:0px;\n"
"	border-top-left-radius:10px;\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-left-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}")
        self.frame_32.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_32)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.username_label = QLabel(self.frame_32)
        self.username_label.setObjectName(u"username_label")
        self.username_label.setFont(font5)
        self.username_label.setStyleSheet(u"color:rgb(180, 180, 180);\n"
"background:transparent;\n"
"padding-left:20px;")

        self.verticalLayout_14.addWidget(self.username_label)

        self.email_label = QLabel(self.frame_32)
        self.email_label.setObjectName(u"email_label")
        self.email_label.setFont(font5)
        self.email_label.setStyleSheet(u"color:rgb(180, 180, 180);\n"
"background:transparent;\n"
"padding-left:20px;\n"
"border-top:2px solid rgb(58, 65, 79);\n"
"border-top-left-radius:0px;\n"
"border-top-right-radius:0px;")

        self.verticalLayout_14.addWidget(self.email_label)


        self.verticalLayout_13.addWidget(self.frame_32)

        self.frame_33 = QFrame(self.frame_30)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setMaximumSize(QSize(16777215, 70))
        self.frame_33.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, -1, 30, 20)
        self.frame_34 = QFrame(self.frame_33)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_34.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_21.addWidget(self.frame_34)

        self.button_edit_profile = QPushButton(self.frame_33)
        self.button_edit_profile.setObjectName(u"button_edit_profile")
        self.button_edit_profile.setMinimumSize(QSize(120, 35))
        self.button_edit_profile.setMaximumSize(QSize(120, 16777215))
        font14 = QFont()
        font14.setFamilies([u"Roboto Medium"])
        font14.setPointSize(9)
        self.button_edit_profile.setFont(font14)
        self.button_edit_profile.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_edit_profile.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_edit_profile.setStyleSheet(u"QPushButton{\n"
"	color:  #5a9bd5;\n"
"	border: 2px solid rgba(90, 155, 213, 200);\n"
"	border-radius : 8px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgb(48, 54, 66);\n"
"	border: 2px solid rgba(90, 155, 213, 160);\n"
"}")

        self.horizontalLayout_21.addWidget(self.button_edit_profile)


        self.verticalLayout_13.addWidget(self.frame_33)

        self.frame_31 = QFrame(self.frame_30)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_31)
        self.verticalLayout_23.setSpacing(0)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_31)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(16777215, 60))
        self.label_9.setFont(font8)
        self.label_9.setStyleSheet(u"color:rgb(180, 180, 180);\n"
"background:transparent;\n"
"padding-left:5px;\n"
"padding-top:20px;\n"
"border-top:2px solid rgb(50, 56, 68);\n"
"border-radius:0px;\n"
"")

        self.verticalLayout_23.addWidget(self.label_9)

        self.frame_75 = QFrame(self.frame_31)
        self.frame_75.setObjectName(u"frame_75")
        self.frame_75.setMaximumSize(QSize(16777215, 100))
        self.frame_75.setStyleSheet(u"QFrame#frame_75{\n"
"	border-radius:10px;\n"
"}")
        self.frame_75.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_75.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.frame_75)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.btn_change_pass = QPushButton(self.frame_75)
        self.btn_change_pass.setObjectName(u"btn_change_pass")
        self.btn_change_pass.setMinimumSize(QSize(0, 50))
        self.btn_change_pass.setFont(font5)
        self.btn_change_pass.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_change_pass.setStyleSheet(u"QPushButton{\n"
"	text-align:left;\n"
"    padding-left:20px;\n"
"	padding-right:20px;\n"
"	color:rgb(160, 160, 160);\n"
"	background-color: rgb(51, 57, 70);\n"
"	border-top-left-radius:10px;\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-left-radius:0px;\n"
"	border-bottom-right-radius:0px;\n"
"	\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(55, 62, 76)\n"
"}")
        icon15 = QIcon()
        icon15.addFile(u"../../../../.designer/Reqs/arrow-right.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_change_pass.setIcon(icon15)

        self.verticalLayout_24.addWidget(self.btn_change_pass)

        self.btn_2FA = QPushButton(self.frame_75)
        self.btn_2FA.setObjectName(u"btn_2FA")
        self.btn_2FA.setMinimumSize(QSize(0, 50))
        self.btn_2FA.setFont(font5)
        self.btn_2FA.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_2FA.setStyleSheet(u"QPushButton{\n"
"	text-align:left;\n"
"    padding-left:20px;\n"
"	padding-right:20px;\n"
"	color:rgb(160, 160, 160);\n"
"	background-color: rgb(51, 57, 70);\n"
"	border-top:2px solid rgb(58, 65, 79);\n"
"	border-top-left-radius:0px;\n"
"	border-top-right-radius:0px;\n"
"	border-bottom-left-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(55, 62, 76)\n"
"}")
        icon16 = QIcon()
        icon16.addFile(u"../../../../.designer/Reqs/arrow-right-off.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_2FA.setIcon(icon16)
        self.btn_2FA.setIconSize(QSize(45, 30))

        self.verticalLayout_24.addWidget(self.btn_2FA)


        self.verticalLayout_23.addWidget(self.frame_75)

        self.frame_76 = QFrame(self.frame_31)
        self.frame_76.setObjectName(u"frame_76")
        self.frame_76.setMaximumSize(QSize(16777215, 150))
        self.frame_76.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_76.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.frame_76)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.button_logout = QPushButton(self.frame_76)
        self.button_logout.setObjectName(u"button_logout")
        self.button_logout.setMinimumSize(QSize(100, 40))
        self.button_logout.setMaximumSize(QSize(250, 16777215))
        font15 = QFont()
        font15.setFamilies([u"Roboto Medium"])
        font15.setPointSize(10)
        self.button_logout.setFont(font15)
        self.button_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_logout.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.button_logout.setStyleSheet(u"QPushButton{\n"
"	color: rgba(1, 190, 118, 200);  /*rgb(190, 42, 42);*/ \n"
"	border: 2px solid rgba(1, 190, 118, 200); /*rgb(190, 42, 42);*/\n"
"	background-color: rgba(0, 170, 127, 20); /*rgba(70, 49, 60, 80);*/\n"
"	border-radius : 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgba(0, 170, 127, 10);\n"
"	border: 2px solid rgba(1, 190, 118, 170);\n"
"}")

        self.horizontalLayout_41.addWidget(self.button_logout)


        self.verticalLayout_23.addWidget(self.frame_76)

        self.frame_77 = QFrame(self.frame_31)
        self.frame_77.setObjectName(u"frame_77")
        self.frame_77.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_77.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_23.addWidget(self.frame_77)


        self.verticalLayout_13.addWidget(self.frame_31)


        self.verticalLayout_12.addWidget(self.frame_30)


        self.horizontalLayout_19.addWidget(self.frame_28)

        self.frame_26 = QFrame(self.account_page)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setMaximumSize(QSize(400, 16777215))
        self.frame_26.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_19.addWidget(self.frame_26)

        self.setting_pages.addWidget(self.account_page)
        self.update_page = QWidget()
        self.update_page.setObjectName(u"update_page")
        self.verticalLayout_41 = QVBoxLayout(self.update_page)
        self.verticalLayout_41.setSpacing(0)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.verticalLayout_41.setContentsMargins(0, 0, 0, 0)
        self.frame_126 = QFrame(self.update_page)
        self.frame_126.setObjectName(u"frame_126")
        self.frame_126.setMaximumSize(QSize(16777215, 50))
        self.frame_126.setFont(font9)
        self.frame_126.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_126.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_66 = QHBoxLayout(self.frame_126)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.horizontalLayout_66.setContentsMargins(25, -1, -1, 0)
        self.label_34 = QLabel(self.frame_126)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font10)
        self.label_34.setStyleSheet(u"color: rgb(190, 190, 190);")

        self.horizontalLayout_66.addWidget(self.label_34)


        self.verticalLayout_41.addWidget(self.frame_126)

        self.frame_98 = QFrame(self.update_page)
        self.frame_98.setObjectName(u"frame_98")
        self.frame_98.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_98.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_50 = QHBoxLayout(self.frame_98)
        self.horizontalLayout_50.setSpacing(0)
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.horizontalLayout_50.setContentsMargins(0, 0, 0, 0)
        self.frame_99 = QFrame(self.frame_98)
        self.frame_99.setObjectName(u"frame_99")
        self.frame_99.setMaximumSize(QSize(320, 16777215))
        self.frame_99.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_99.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_50.addWidget(self.frame_99)

        self.frame_100 = QFrame(self.frame_98)
        self.frame_100.setObjectName(u"frame_100")
        self.frame_100.setMinimumSize(QSize(650, 0))
        self.frame_100.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_100.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_100)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.frame_117 = QFrame(self.frame_100)
        self.frame_117.setObjectName(u"frame_117")
        self.frame_117.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_117.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frame_117)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(0, -1, 0, -1)
        self.label_35 = QLabel(self.frame_117)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setMaximumSize(QSize(16777215, 30))
        self.label_35.setFont(font11)
        self.label_35.setStyleSheet(u"color: rgb(218, 218, 218);")

        self.verticalLayout_37.addWidget(self.label_35)

        self.frame_118 = QFrame(self.frame_117)
        self.frame_118.setObjectName(u"frame_118")
        self.frame_118.setMinimumSize(QSize(0, 100))
        self.frame_118.setMaximumSize(QSize(16777215, 230))
        self.frame_118.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(49, 55, 67);\n"
"	border-radius:10px;\n"
"}\n"
"")
        self.frame_118.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_118.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_118)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(0, -1, 0, -1)
        self.pushButton = QPushButton(self.frame_118)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))
        self.pushButton.setFont(font5)
        self.pushButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.pushButton.setStyleSheet(u"background:none;\n"
"color: rgb(190, 190, 190);\n"
"text-align:left;\n"
"padding-left:50px;\n"
"padding-right:30px;")
        icon17 = QIcon()
        icon17.addFile(u"../../../../.designer/Reqs/check.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon17)
        self.pushButton.setIconSize(QSize(40, 40))

        self.verticalLayout_38.addWidget(self.pushButton)

        self.label_42 = QLabel(self.frame_118)
        self.label_42.setObjectName(u"label_42")
        self.label_42.setMinimumSize(QSize(400, 0))
        self.label_42.setMaximumSize(QSize(16777215, 40))
        self.label_42.setFont(font5)
        self.label_42.setStyleSheet(u"color: rgb(190, 190, 190);\n"
"padding-left:30px;")
        self.label_42.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_38.addWidget(self.label_42)

        self.frame_103 = QFrame(self.frame_118)
        self.frame_103.setObjectName(u"frame_103")
        self.frame_103.setStyleSheet(u"border-top:2px solid rgba(189, 189, 189, 20);\n"
"border-radius:0px;")
        self.frame_103.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_103.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_51 = QHBoxLayout(self.frame_103)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.btn_check_update = QPushButton(self.frame_103)
        self.btn_check_update.setObjectName(u"btn_check_update")
        self.btn_check_update.setMinimumSize(QSize(100, 40))
        self.btn_check_update.setMaximumSize(QSize(250, 16777215))
        self.btn_check_update.setFont(font15)
        self.btn_check_update.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_check_update.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_check_update.setStyleSheet(u"QPushButton{\n"
"	color: rgb(0, 133, 200); \n"
"	border: 2px solid rgba(0, 133, 200, 200); \n"
"	background-color: rgba(0, 133, 200, 20); \n"
"	border-radius : 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgba(0, 133, 200, 10);\n"
"	border: 2px solid rgba(0, 133, 200, 170);\n"
"}")

        self.horizontalLayout_51.addWidget(self.btn_check_update)


        self.verticalLayout_38.addWidget(self.frame_103)


        self.verticalLayout_37.addWidget(self.frame_118)

        self.label_38 = QLabel(self.frame_117)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setMinimumSize(QSize(0, 50))
        self.label_38.setMaximumSize(QSize(16777215, 30))
        self.label_38.setFont(font11)
        self.label_38.setStyleSheet(u"color: rgb(218, 218, 218);")

        self.verticalLayout_37.addWidget(self.label_38)

        self.frame_101 = QFrame(self.frame_117)
        self.frame_101.setObjectName(u"frame_101")
        self.frame_101.setMaximumSize(QSize(16777215, 105))
        self.frame_101.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_101.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_39 = QVBoxLayout(self.frame_101)
        self.verticalLayout_39.setSpacing(0)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.frame_129 = QFrame(self.frame_101)
        self.frame_129.setObjectName(u"frame_129")
        self.frame_129.setMinimumSize(QSize(0, 100))
        self.frame_129.setMaximumSize(QSize(16777215, 100))
        self.frame_129.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(49, 55, 67);\n"
"	border-radius:10px;\n"
"}\n"
"")
        self.frame_129.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_129.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.frame_129)
        self.verticalLayout_40.setSpacing(0)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(20, 0, 0, 0)
        self.frame_130 = QFrame(self.frame_129)
        self.frame_130.setObjectName(u"frame_130")
        self.frame_130.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_130.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_68 = QHBoxLayout(self.frame_130)
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.horizontalLayout_68.setContentsMargins(11, -1, 50, -1)
        self.label_39 = QLabel(self.frame_130)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setMinimumSize(QSize(400, 0))
        self.label_39.setMaximumSize(QSize(16777215, 40))
        self.label_39.setFont(font5)
        self.label_39.setStyleSheet(u"color: rgb(190, 190, 190);")

        self.horizontalLayout_68.addWidget(self.label_39)

        self.checkBox_12 = PyToggle(self.frame_130)
        self.checkBox_12.setObjectName(u"checkBox_12")

        self.horizontalLayout_68.addWidget(self.checkBox_12)


        self.verticalLayout_40.addWidget(self.frame_130)

        self.frame_131 = QFrame(self.frame_129)
        self.frame_131.setObjectName(u"frame_131")
        self.frame_131.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_131.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_69 = QHBoxLayout(self.frame_131)
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.horizontalLayout_69.setContentsMargins(-1, -1, 50, -1)
        self.label_40 = QLabel(self.frame_131)
        self.label_40.setObjectName(u"label_40")
        self.label_40.setMinimumSize(QSize(400, 0))
        self.label_40.setMaximumSize(QSize(16777215, 40))
        self.label_40.setFont(font5)
        self.label_40.setStyleSheet(u"color: rgb(190, 190, 190);")

        self.horizontalLayout_69.addWidget(self.label_40)

        self.checkBox_13 = PyToggle(self.frame_131)
        self.checkBox_13.setObjectName(u"checkBox_13")

        self.horizontalLayout_69.addWidget(self.checkBox_13)


        self.verticalLayout_40.addWidget(self.frame_131)


        self.verticalLayout_39.addWidget(self.frame_129)


        self.verticalLayout_37.addWidget(self.frame_101)

        self.frame_102 = QFrame(self.frame_117)
        self.frame_102.setObjectName(u"frame_102")
        self.frame_102.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_102.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_37.addWidget(self.frame_102)


        self.verticalLayout_33.addWidget(self.frame_117)


        self.horizontalLayout_50.addWidget(self.frame_100)

        self.frame_134 = QFrame(self.frame_98)
        self.frame_134.setObjectName(u"frame_134")
        self.frame_134.setMaximumSize(QSize(320, 16777215))
        self.frame_134.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_134.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_50.addWidget(self.frame_134)


        self.verticalLayout_41.addWidget(self.frame_98)

        self.setting_pages.addWidget(self.update_page)
        self.about_page = QWidget()
        self.about_page.setObjectName(u"about_page")
        self.verticalLayout_15 = QVBoxLayout(self.about_page)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_127 = QFrame(self.about_page)
        self.frame_127.setObjectName(u"frame_127")
        self.frame_127.setMaximumSize(QSize(16777215, 50))
        self.frame_127.setFont(font9)
        self.frame_127.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_127.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_67 = QHBoxLayout(self.frame_127)
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.horizontalLayout_67.setContentsMargins(25, -1, -1, 0)
        self.label_36 = QLabel(self.frame_127)
        self.label_36.setObjectName(u"label_36")
        font16 = QFont()
        font16.setFamilies([u"Roboto Medium"])
        font16.setPointSize(14)
        self.label_36.setFont(font16)
        self.label_36.setStyleSheet(u"color: rgb(190, 190, 190);")

        self.horizontalLayout_67.addWidget(self.label_36)


        self.verticalLayout_15.addWidget(self.frame_127)

        self.frame_104 = QFrame(self.about_page)
        self.frame_104.setObjectName(u"frame_104")
        self.frame_104.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_104.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_52 = QHBoxLayout(self.frame_104)
        self.horizontalLayout_52.setSpacing(0)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.horizontalLayout_52.setContentsMargins(0, 0, 0, 0)
        self.frame_105 = QFrame(self.frame_104)
        self.frame_105.setObjectName(u"frame_105")
        self.frame_105.setMaximumSize(QSize(320, 16777215))
        self.frame_105.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_105.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_52.addWidget(self.frame_105)

        self.frame_106 = QFrame(self.frame_104)
        self.frame_106.setObjectName(u"frame_106")
        self.frame_106.setMinimumSize(QSize(650, 0))
        self.frame_106.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_106.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.frame_106)
        self.verticalLayout_17.setSpacing(10)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.frame_132 = QFrame(self.frame_106)
        self.frame_132.setObjectName(u"frame_132")
        self.frame_132.setMinimumSize(QSize(0, 100))
        self.frame_132.setMaximumSize(QSize(16777215, 200))
        self.frame_132.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(49, 55, 67);\n"
"	border-radius:10px;\n"
"}\n"
"")
        self.frame_132.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_132.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frame_132)
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.frame_35 = QFrame(self.frame_132)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setMaximumSize(QSize(200, 16777215))
        self.frame_35.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_35.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frame_35)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.app_icon = QPushButton(self.frame_35)
        self.app_icon.setObjectName(u"app_icon")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.app_icon.sizePolicy().hasHeightForWidth())
        self.app_icon.setSizePolicy(sizePolicy2)
        self.app_icon.setStyleSheet(u"border:none;\n"
"background:none;")
        icon18 = QIcon()
        icon18.addFile(u"../../../../.designer/Reqs/app_icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.app_icon.setIcon(icon18)
        self.app_icon.setIconSize(QSize(60, 60))

        self.horizontalLayout_30.addWidget(self.app_icon)


        self.horizontalLayout_29.addWidget(self.frame_35)

        self.frame_36 = QFrame(self.frame_132)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_36.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_36)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 20, -1, -1)
        self.label_43 = QLabel(self.frame_36)
        self.label_43.setObjectName(u"label_43")
        self.label_43.setMinimumSize(QSize(400, 0))
        self.label_43.setMaximumSize(QSize(16777215, 40))
        self.label_43.setFont(font16)
        self.label_43.setStyleSheet(u"color: rgb(190, 190, 190);\n"
"padding-left:15px;")
        self.label_43.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_16.addWidget(self.label_43)

        self.label_46 = QLabel(self.frame_36)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(400, 0))
        self.label_46.setMaximumSize(QSize(16777215, 40))
        self.label_46.setFont(font5)
        self.label_46.setStyleSheet(u"color: rgb(190, 190, 190);\n"
"padding-left:15px;")
        self.label_46.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_16.addWidget(self.label_46)


        self.horizontalLayout_29.addWidget(self.frame_36)


        self.verticalLayout_17.addWidget(self.frame_132)

        self.frame_108 = QFrame(self.frame_106)
        self.frame_108.setObjectName(u"frame_108")
        self.frame_108.setMaximumSize(QSize(16777215, 250))
        self.frame_108.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_108.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_45 = QVBoxLayout(self.frame_108)
        self.verticalLayout_45.setSpacing(0)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.verticalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.frame_133 = QFrame(self.frame_108)
        self.frame_133.setObjectName(u"frame_133")
        self.frame_133.setMinimumSize(QSize(0, 250))
        self.frame_133.setMaximumSize(QSize(16777215, 250))
        self.frame_133.setStyleSheet(u"QFrame{\n"
"	background-color: rgb(49, 55, 67);\n"
"	border-radius:10px;\n"
"}\n"
"")
        self.frame_133.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_133.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_42 = QVBoxLayout(self.frame_133)
        self.verticalLayout_42.setSpacing(0)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.link_website = QPushButton(self.frame_133)
        self.link_website.setObjectName(u"link_website")
        sizePolicy2.setHeightForWidth(self.link_website.sizePolicy().hasHeightForWidth())
        self.link_website.setSizePolicy(sizePolicy2)
        self.link_website.setFont(font15)
        self.link_website.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.link_website.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	color:rgb(190, 190, 190);\n"
"	padding-right: 30px;\n"
"	padding-left:30px;\n"
"	text-align:left;\n"
"	border-bottom: 2px solid rgba(179, 179, 179, 20);\n"
"	border-bottom-left-radius:0px;\n"
"	border-bottom-right-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:  rgb(55, 62, 76);\n"
"}")
        icon19 = QIcon()
        icon19.addFile(u"../../../../.designer/Reqs/link.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.link_website.setIcon(icon19)
        self.link_website.setIconSize(QSize(30, 30))

        self.verticalLayout_42.addWidget(self.link_website)

        self.link_support = QPushButton(self.frame_133)
        self.link_support.setObjectName(u"link_support")
        sizePolicy2.setHeightForWidth(self.link_support.sizePolicy().hasHeightForWidth())
        self.link_support.setSizePolicy(sizePolicy2)
        self.link_support.setFont(font15)
        self.link_support.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.link_support.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	color:rgb(190, 190, 190);\n"
"	padding-right: 30px;\n"
"	padding-left:30px;\n"
"	text-align:left;\n"
"	border-bottom: 2px solid rgba(179, 179, 179, 20);\n"
"	border-bottom-left-radius:0px;\n"
"	border-bottom-right-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:  rgb(55, 62, 76);\n"
"}")
        self.link_support.setIcon(icon19)
        self.link_support.setIconSize(QSize(30, 30))

        self.verticalLayout_42.addWidget(self.link_support)

        self.link_privacy_policy = QPushButton(self.frame_133)
        self.link_privacy_policy.setObjectName(u"link_privacy_policy")
        sizePolicy2.setHeightForWidth(self.link_privacy_policy.sizePolicy().hasHeightForWidth())
        self.link_privacy_policy.setSizePolicy(sizePolicy2)
        self.link_privacy_policy.setFont(font15)
        self.link_privacy_policy.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.link_privacy_policy.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	color:rgb(190, 190, 190);\n"
"	padding-right: 30px;\n"
"	padding-left:30px;\n"
"	text-align:left;\n"
"	border-bottom: 2px solid rgba(179, 179, 179, 20);\n"
"	border-bottom-left-radius:0px;\n"
"	border-bottom-right-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:  rgb(55, 62, 76);\n"
"}")
        self.link_privacy_policy.setIcon(icon19)
        self.link_privacy_policy.setIconSize(QSize(30, 30))

        self.verticalLayout_42.addWidget(self.link_privacy_policy)

        self.link_terms_services = QPushButton(self.frame_133)
        self.link_terms_services.setObjectName(u"link_terms_services")
        sizePolicy2.setHeightForWidth(self.link_terms_services.sizePolicy().hasHeightForWidth())
        self.link_terms_services.setSizePolicy(sizePolicy2)
        self.link_terms_services.setFont(font15)
        self.link_terms_services.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.link_terms_services.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	color:rgb(190, 190, 190);\n"
"	padding-right: 30px;\n"
"	padding-left:30px;\n"
"	text-align:left;\n"
"	border-bottom: 2px solid rgba(179, 179, 179, 20);\n"
"	border-bottom-left-radius:0px;\n"
"	border-bottom-right-radius:0px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:  rgb(55, 62, 76);\n"
"}")
        self.link_terms_services.setIcon(icon19)
        self.link_terms_services.setIconSize(QSize(30, 30))

        self.verticalLayout_42.addWidget(self.link_terms_services)

        self.link_open_source = QPushButton(self.frame_133)
        self.link_open_source.setObjectName(u"link_open_source")
        sizePolicy2.setHeightForWidth(self.link_open_source.sizePolicy().hasHeightForWidth())
        self.link_open_source.setSizePolicy(sizePolicy2)
        self.link_open_source.setFont(font15)
        self.link_open_source.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.link_open_source.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	background:none;\n"
"	color:rgb(190, 190, 190);\n"
"	padding-right: 30px;\n"
"	padding-left:30px;\n"
"	text-align:left;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"}")
        self.link_open_source.setIcon(icon19)
        self.link_open_source.setIconSize(QSize(30, 30))

        self.verticalLayout_42.addWidget(self.link_open_source)


        self.verticalLayout_45.addWidget(self.frame_133)


        self.verticalLayout_17.addWidget(self.frame_108)

        self.frame_39 = QFrame(self.frame_106)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_39.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_44 = QVBoxLayout(self.frame_39)
        self.verticalLayout_44.setSpacing(0)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.verticalLayout_44.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_39)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(0, 60))
        self.label_11.setMaximumSize(QSize(16777215, 60))
        self.label_11.setFont(font8)
        self.label_11.setStyleSheet(u"color:rgb(180, 180, 180);\n"
"background:transparent;\n"
"border-radius:0px;\n"
"padding-top:10px;\n"
"")

        self.verticalLayout_44.addWidget(self.label_11)

        self.frame_107 = QFrame(self.frame_39)
        self.frame_107.setObjectName(u"frame_107")
        self.frame_107.setMaximumSize(QSize(16777215, 100))
        self.frame_107.setStyleSheet(u"QFrame#frame_75{\n"
"	border-radius:10px;\n"
"}")
        self.frame_107.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_107.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_43 = QVBoxLayout(self.frame_107)
        self.verticalLayout_43.setSpacing(0)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.btn_linkedIn = QPushButton(self.frame_107)
        self.btn_linkedIn.setObjectName(u"btn_linkedIn")
        self.btn_linkedIn.setMinimumSize(QSize(0, 50))
        self.btn_linkedIn.setFont(font15)
        self.btn_linkedIn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_linkedIn.setStyleSheet(u"QPushButton{\n"
"	text-align:left;\n"
"    padding-left:30px;\n"
"	padding-right:30px;\n"
"	color:rgb(180, 180, 180);\n"
"	background-color: rgb(51, 57, 70);\n"
"	border-top-left-radius:10px;\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-left-radius:0px;\n"
"	border-bottom-right-radius:0px;\n"
"	\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(55, 62, 76);\n"
"}")
        icon20 = QIcon()
        icon20.addFile(u"../../../../.designer/Reqs/LinkedIn.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_linkedIn.setIcon(icon20)
        self.btn_linkedIn.setIconSize(QSize(30, 30))

        self.verticalLayout_43.addWidget(self.btn_linkedIn)

        self.btn_gitHub = QPushButton(self.frame_107)
        self.btn_gitHub.setObjectName(u"btn_gitHub")
        self.btn_gitHub.setMinimumSize(QSize(0, 50))
        self.btn_gitHub.setFont(font15)
        self.btn_gitHub.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.btn_gitHub.setStyleSheet(u"QPushButton{\n"
"	text-align:left;\n"
"    padding-left:30px;\n"
"	padding-right:30px;\n"
"	color:rgb(180, 180, 180);\n"
"	background-color: rgb(51, 57, 70);\n"
"	border-top:2px solid rgb(58, 65, 79);\n"
"	border-top-left-radius:0px;\n"
"	border-top-right-radius:0px;\n"
"	border-bottom-left-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(55, 62, 76)\n"
"}")
        icon21 = QIcon()
        icon21.addFile(u"../../../../.designer/Reqs/GitHub.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_gitHub.setIcon(icon21)
        self.btn_gitHub.setIconSize(QSize(30, 30))

        self.verticalLayout_43.addWidget(self.btn_gitHub)


        self.verticalLayout_44.addWidget(self.frame_107)


        self.verticalLayout_17.addWidget(self.frame_39)

        self.frame_38 = QFrame(self.frame_106)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_38.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_17.addWidget(self.frame_38)


        self.horizontalLayout_52.addWidget(self.frame_106)

        self.frame_137 = QFrame(self.frame_104)
        self.frame_137.setObjectName(u"frame_137")
        self.frame_137.setMaximumSize(QSize(320, 16777215))
        self.frame_137.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_137.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_52.addWidget(self.frame_137)


        self.verticalLayout_15.addWidget(self.frame_104)

        self.setting_pages.addWidget(self.about_page)

        self.verticalLayout_8.addWidget(self.setting_pages)


        self.horizontalLayout_22.addWidget(self.frame_50)


        self.verticalLayout_4.addWidget(self.frame_48)

        self.stackedWidget.addWidget(self.settings_page)
        self.conversation_page = QWidget()
        self.conversation_page.setObjectName(u"conversation_page")
        self.verticalLayout_7 = QVBoxLayout(self.conversation_page)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.conversation_page)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.frame)
        self.horizontalLayout_33.setSpacing(0)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(0, 0, 0, 0)
        self.frame_46 = QFrame(self.frame)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setMinimumSize(QSize(100, 0))
        self.frame_46.setMaximumSize(QSize(400, 16777215))
        self.frame_46.setStyleSheet(u"background-color: rgb(50, 56, 68);")
        self.frame_46.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_46.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_33.addWidget(self.frame_46)

        self.frame_45 = QFrame(self.frame)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setMinimumSize(QSize(700, 0))
        self.frame_45.setMaximumSize(QSize(1100, 16777215))
        self.frame_45.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_45.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_45)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frame_58 = QFrame(self.frame_45)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setMaximumSize(QSize(16777215, 16777215))
        self.frame_58.setStyleSheet(u"background-color: rgb(50, 56, 68);")
        self.frame_58.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_58.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.frame_58)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 50, 0, 0)
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setObjectName(u"chat_layout")

        self.verticalLayout_20.addLayout(self.chat_layout)


        self.verticalLayout_18.addWidget(self.frame_58)

        self.frame_2 = QFrame(self.frame_45)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(0, 150))
        self.frame_2.setMaximumSize(QSize(16777215, 150))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.frame_59 = QFrame(self.frame_2)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setStyleSheet(u"background-color: rgb(50, 56, 68);")
        self.frame_59.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_59.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_34.addWidget(self.frame_59)

        self.frame_60 = QFrame(self.frame_2)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setMinimumSize(QSize(700, 0))
        self.frame_60.setStyleSheet(u"background-color: rgb(50, 56, 68);")
        self.frame_60.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_60.setFrameShadow(QFrame.Shadow.Raised)
        self.addButton_2 = StickyButton(self.frame_60)
        self.addButton_2.setObjectName(u"addButton_2")
        self.addButton_2.setGeometry(QRect(50, 50, 51, 45))
        self.addButton_2.setMinimumSize(QSize(0, 45))
        self.addButton_2.setMaximumSize(QSize(160, 16777215))
        self.addButton_2.setFont(font4)
        self.addButton_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addButton_2.setStyleSheet(u"QPushButton{\n"
"	background:none;\n"
"	border:none;\n"
"	color:rgba(255, 255, 255, 180);\n"
"	border-radius: 21px ;\n"
"	margin-top:3px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(45, 48, 58);\n"
"}")
        self.addButton_2.setIcon(icon9)
        self.addButton_2.setIconSize(QSize(22, 22))
        self.text_prompt_2 = AutoGrowTextEdit(self.frame_60)
        self.text_prompt_2.setObjectName(u"text_prompt_2")
        self.text_prompt_2.setEnabled(True)
        self.text_prompt_2.setGeometry(QRect(50, 50, 591, 50))
        sizePolicy1.setHeightForWidth(self.text_prompt_2.sizePolicy().hasHeightForWidth())
        self.text_prompt_2.setSizePolicy(sizePolicy1)
        self.text_prompt_2.setMinimumSize(QSize(0, 50))
        self.text_prompt_2.setMaximumSize(QSize(16777215, 50))
        self.text_prompt_2.setSizeIncrement(QSize(0, 0))
        self.text_prompt_2.setBaseSize(QSize(0, 0))
        self.text_prompt_2.setFont(font5)
        self.text_prompt_2.setStyleSheet(u"QTextEdit{\n"
" 	border:2px solid rgb(41, 44, 53);\n"
"    border-radius:22px;\n"
"	background-color: rgb(41, 44, 53);\n"
"    color:rgba(255, 	255, 255, 210);\n"
"    padding-left:20px;\n"
"	padding-top:10px;\n"
"	padding-right:15px;\n"
"	padding-bottom:45px;\n"
"}\n"
"\n"
"QTextEdit:hover{\n"
"	border:2px solid rgb(220, 0, 220);\n"
"}\n"
"\n"
"QTextEdit:focus{\n"
"	border:2px solid rgb(85,170,255);\n"
"}")
        self.text_prompt_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.text_prompt_2.setFrameShadow(QFrame.Shadow.Plain)
        self.text_prompt_2.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.searchButton_2 = StickyButton(self.frame_60)
        self.searchButton_2.setObjectName(u"searchButton_2")
        self.searchButton_2.setGeometry(QRect(590, 50, 45, 45))
        sizePolicy.setHeightForWidth(self.searchButton_2.sizePolicy().hasHeightForWidth())
        self.searchButton_2.setSizePolicy(sizePolicy)
        self.searchButton_2.setMinimumSize(QSize(45, 45))
        self.searchButton_2.setMaximumSize(QSize(45, 45))
        self.searchButton_2.setFont(font4)
        self.searchButton_2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.searchButton_2.setStyleSheet(u"QPushButton{\n"
"	background:none;\n"
"	border:none;\n"
"	color:rgba(255, 255, 255, 180);\n"
"	background-color: rgb(41, 44, 53);\n"
"	border-radius: 21px ;\n"
"	margin-top:3px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: rgb(45, 48, 58);\n"
"}")
        self.searchButton_2.setIcon(icon8)
        self.searchButton_2.setIconSize(QSize(27, 27))
        self.text_prompt_2.raise_()
        self.addButton_2.raise_()
        self.searchButton_2.raise_()

        self.horizontalLayout_34.addWidget(self.frame_60)

        self.frame_61 = QFrame(self.frame_2)
        self.frame_61.setObjectName(u"frame_61")
        self.frame_61.setStyleSheet(u"background-color: rgb(50, 56, 68);")
        self.frame_61.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_61.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_34.addWidget(self.frame_61)


        self.verticalLayout_18.addWidget(self.frame_2)


        self.horizontalLayout_33.addWidget(self.frame_45)

        self.frame_47 = QFrame(self.frame)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setMinimumSize(QSize(100, 0))
        self.frame_47.setMaximumSize(QSize(400, 16777215))
        self.frame_47.setStyleSheet(u"background-color: rgb(50, 56, 68);")
        self.frame_47.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_47.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_33.addWidget(self.frame_47)


        self.verticalLayout_7.addWidget(self.frame)

        self.stackedWidget.addWidget(self.conversation_page)

        self.horizontalLayout_6.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.content_page_frame)


        self.verticalLayout_2.addWidget(self.Content)


        self.verticalLayout.addWidget(self.drop_shadow_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toggle_button.setText("")
        self.icon.setText("")
        self.status_bar.setText(QCoreApplication.translate("MainWindow", u"  RAG based Chat App", None))
        self.button_minimize.setText("")
        self.button_restore.setText("")
        self.button_close.setText("")
        self.button_new_chat.setText(QCoreApplication.translate("MainWindow", u"     New Chat                         ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Recent chats", None))
        self.button_settings.setText(QCoreApplication.translate("MainWindow", u"      Settings                     ", None))
        self.label.setText("")
        self.labelProtection.setText(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Roboto'; font-size:30pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'ui-sans-serif','-apple-system','system-ui','Segoe UI','Helvetica','Apple Color Emoji','Arial','sans-serif','Segoe UI Emoji','Segoe UI Symbol'; font-size:24pt;\">What can I help with?</span></p></body></html>", None))
        self.searchButton.setText("")
        self.addButton.setText("")
        self.text_prompt.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Roboto'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:7.8pt;\"><br /></p></body></html>", None))
        self.text_prompt.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ask Anything", None))
#if QT_CONFIG(tooltip)
        self.login_button.setToolTip(QCoreApplication.translate("MainWindow", u"Not logged in!", None))
#endif // QT_CONFIG(tooltip)
        self.login_button.setText(QCoreApplication.translate("MainWindow", u"    Log In", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.acc_button.setText(QCoreApplication.translate("MainWindow", u"   Account", None))
        self.buttonDocs.setText(QCoreApplication.translate("MainWindow", u"   Documents", None))
        self.buttonUpdate.setText(QCoreApplication.translate("MainWindow", u"   Update", None))
        self.buttonAbout.setText(QCoreApplication.translate("MainWindow", u"   About", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Documents", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Your Docs in RAG:", None))
        self.account_label.setText(QCoreApplication.translate("MainWindow", u"Account", None))
        self.logged_in_label.setText(QCoreApplication.translate("MainWindow", u" Not Logged In", None))
#if QT_CONFIG(whatsthis)
        self.username_label.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.username_label.setText(QCoreApplication.translate("MainWindow", u"Username: ", None))
        self.email_label.setText(QCoreApplication.translate("MainWindow", u"Email: ", None))
        self.button_edit_profile.setText(QCoreApplication.translate("MainWindow", u"Edit profile", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Security", None))
        self.btn_change_pass.setText(QCoreApplication.translate("MainWindow", u"Change Password", None))
        self.btn_2FA.setText(QCoreApplication.translate("MainWindow", u"Two-Factor Authentication", None))
        self.button_logout.setText(QCoreApplication.translate("MainWindow", u"Log In", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Update", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Current Version", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Version: 1.0.0", None))
        self.label_42.setText(QCoreApplication.translate("MainWindow", u"You are running the latest version", None))
        self.btn_check_update.setText(QCoreApplication.translate("MainWindow", u"Check for update", None))
        self.label_38.setText(QCoreApplication.translate("MainWindow", u"Update Settings", None))
        self.label_39.setText(QCoreApplication.translate("MainWindow", u"Check for updates automatically", None))
        self.checkBox_12.setText("")
        self.label_40.setText(QCoreApplication.translate("MainWindow", u"Download updates in background", None))
        self.checkBox_13.setText("")
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.app_icon.setText("")
        self.label_43.setText(QCoreApplication.translate("MainWindow", u"RAG based Chat App", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"Version: 1.0.0", None))
        self.link_website.setText(QCoreApplication.translate("MainWindow", u"Website", None))
        self.link_support.setText(QCoreApplication.translate("MainWindow", u"Support", None))
        self.link_privacy_policy.setText(QCoreApplication.translate("MainWindow", u"Privacy policy", None))
        self.link_terms_services.setText(QCoreApplication.translate("MainWindow", u"Terms of Services", None))
        self.link_open_source.setText(QCoreApplication.translate("MainWindow", u"Open Source Licenses", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Credits: Sandeep Bhaskar", None))
        self.btn_linkedIn.setText(QCoreApplication.translate("MainWindow", u"LinkedIn", None))
        self.btn_gitHub.setText(QCoreApplication.translate("MainWindow", u"GitHub", None))
        self.addButton_2.setText("")
        self.text_prompt_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Roboto'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'MS Shell Dlg 2'; font-size:7.8pt;\"><br /></p></body></html>", None))
        self.text_prompt_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Ask Anything", None))
        self.searchButton_2.setText("")
    # retranslateUi

