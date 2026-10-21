from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PyToggle(QCheckBox):

    def __init__(
        self,
        parent=None,
        width=50,
        height=25,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#2982F0",
        animation_curve=QEasingCurve.OutBounce
    ):
        super().__init__(parent)

        # Store dimensions
        self.toggle_width = width
        self.toggle_height = height
        self.circle_size = height - 6   # 19px

        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)

        # Colors
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        # Initial circle position
        self._circle_position = 3

        # Animation
        self.animation = QPropertyAnimation(
            self,
            b"circle_position"
        )
        self.animation.setDuration(300)
        self.animation.setEasingCurve(animation_curve)

        self.stateChanged.connect(
            self.start_transition
        )

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_transition(self):
        self.animation.stop()

        if self.isChecked():
            end_pos = self.width() - self.circle_size - 3
        else:
            end_pos = 3

        self.animation.setEndValue(end_pos)
        self.animation.start()

    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        rect = QRect(
            0,
            0,
            self.width(),
            self.height()
        )

        # Background
        if self.isChecked():
            p.setBrush(QColor(self._active_color))
        else:
            p.setBrush(QColor(self._bg_color))

        p.drawRoundedRect(
            rect,
            self.height()/2,
            self.height()/2
        )

        # Circle
        p.setBrush(QColor(self._circle_color))
        p.drawEllipse(
            int(self._circle_position),
            3,
            self.circle_size,
            self.circle_size
        )

        p.end()