from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QObject, QEvent


class StickyButton(QPushButton):
    """
    A QPushButton anchored to a corner of an AutoGrowTextEdit (or any QWidget).

    Anchors
    -------
    'bottom-right'  – sits inside the right edge, aligned to the bottom row.
    'bottom-left'   – same on the left edge.

    The button repositions itself on:
      • QEvent.Resize / QEvent.Move on the target widget
      • total_height_changed signal  (AutoGrowTextEdit)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widget  = None
        self._margin  = 8
        self._anchor  = "bottom-right"
        self.setFixedSize(45, 45)

    # ── Public API ─────────────────────────────────────────────────────────────

    def setTextEdit(self, widget):
        """Attach to an AutoGrowTextEdit (or plain QTextEdit / QWidget)."""
        self._widget = widget
        widget.installEventFilter(self)

        # Subscribe to the composite widget's height signal if available
        if hasattr(widget, "total_height_changed"):
            widget.total_height_changed.connect(self._on_height_changed)

        self.update_position()

    def setAnchor(self, anchor: str):
        """anchor: 'bottom-right' | 'bottom-left'"""
        self._anchor = anchor
        self.update_position()

    # ── Event filter ──────────────────────────────────────────────────────────

    def eventFilter(self, obj: QObject, event: QEvent):
        if obj is self._widget and event.type() in (QEvent.Resize, QEvent.Move):
            self.update_position()
        return super().eventFilter(obj, event)

    def _on_height_changed(self, _: int):
        self.update_position()

    # ── Position calculation ───────────────────────────────────────────────────

    def update_position(self):
        if self._widget is None:
            return

        w   = self._widget
        btn = self

        # Bottom of the widget — stays fixed as widget grows upward
        y = w.y() + w.height() - btn.height() - self._margin

        if self._anchor == "bottom-left":
            x = w.x() + self._margin
        else:
            x = w.x() + w.width() - btn.width() - self._margin

        btn.move(x, y)
        btn.raise_()