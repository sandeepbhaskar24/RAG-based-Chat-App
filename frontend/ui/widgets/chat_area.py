from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt


class ChatArea(QScrollArea):
    def __init__(self):
        super().__init__()
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(8, 8, 8, 8)

        # ── CRITICAL: align bubbles to the TOP so the last bubble never
        # stretches to fill remaining scroll-area height.  Without this,
        # the AI bubble (last item) expands to fill all empty space and
        # appears as a giant empty box while streaming.
        self.layout.setAlignment(Qt.AlignTop)

        self.setWidgetResizable(True)
        self.setWidget(self.container)

        # Remove the scrollbar frame so it doesn't add visual borders
        self.setFrameShape(QScrollArea.NoFrame)

    def add_bubble(self, bubble):
        self.layout.addWidget(bubble)
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        )