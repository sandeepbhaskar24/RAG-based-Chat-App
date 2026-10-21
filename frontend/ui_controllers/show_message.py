from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QDialog
from PyQt5.QtCore import Qt

class messageWindow(QDialog):        
    def __init__(self, main_win):
        super().__init__(main_win)
        
        from ui.message_ui import Ui_Dialog
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
        
        # close window
        self.ui.btn_ok.clicked.connect(lambda: self.close())
    
    def showError(self, error):
        self.ui.msg.setText('Message from Server: Error:{}'.format(error['status_code']))
        self.ui.info.setText('{}'.format(error['message']))
