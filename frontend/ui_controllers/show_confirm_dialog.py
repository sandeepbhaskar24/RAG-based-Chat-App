from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QDialog
from PyQt5.QtCore import Qt

class ConfirmDialog(QDialog):        
    def __init__(self):
        super().__init__()
        
        from ui.confirm_dialog import Ui_Dialog
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # ==>> REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # self.ui.horizontalLayout.setContentsMargins(11, 11, 11, 11)

        ## drop shaodow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)
        
        # stay always abobe the main window
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(lambda: self.close())
