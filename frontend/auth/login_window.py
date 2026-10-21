from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QDialog
from PyQt5.QtCore import Qt

from PIL import Image, ImageFilter
import io

from services.handle_requests import signup, login

class LoginWindow(QDialog):
    def __init__(self, main_win):
        super().__init__()
        self.main_window = main_win

        from ui.login_page_ui import Ui_Dialog
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # ==>> REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        self.ui.verticalLayout.setContentsMargins(11, 11, 11, 11)

        ## drop shaodow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 255))
        self.ui.drop_shadow_frame.setGraphicsEffect(self.shadow)
        
        # stay always above the main window
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        # CLOSE
        # self.ui.button_close.clicked.connect(lambda: sys.exit())
        self.ui.button_close.clicked.connect(lambda: self.close())
        
        self.ui.signup_page_button.clicked.connect(lambda: self.setSignupPage())
        self.ui.login_page_button.clicked.connect(lambda: [self.setLoginPage(), self.ui.info_label.setText('')])
        
        # signup button --handle_request
        self.ui.signup_button.clicked.connect(lambda: signup(self))
        
        # login button --handle_request
        self.ui.login_button.clicked.connect(lambda: login(self, self.main_window))
    
    def setSignupPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.signup_page)
        
    def setLoginPage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)
        
        

class BlurOverlay(LoginWindow):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        blurred = self.grab_and_blur(self.ui.info_label2)

        self.ui.info_label2.setPixmap(blurred)
        self.ui.info_label2.setScaledContents(True)

        self.resize(parent.size())
        self.ui.info_label2.resize(self.size())
        
    def grab_and_blur(self, widget, radius=15):
        pixmap = widget.grab()

        image = pixmap.toImage()
        ptr = image.bits()
        ptr.setsize(image.byteCount())

        img = Image.frombuffer(
            "RGBA",
            (image.width(), image.height()),
            bytes(ptr),
            "raw",
            "BGRA",
            0,
            1
        )

        blurred = img.filter(ImageFilter.GaussianBlur(radius))

        data = io.BytesIO()
        blurred.save(data, format="PNG")

        result = QPixmap()
        result.loadFromData(data.getvalue())

        return result
