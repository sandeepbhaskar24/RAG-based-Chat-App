"""
DocumentsPanel - the document library list shown in Settings > Documents.

  [ 3 documents                       + Add document ]
  [ PDF  report.pdf        42 chunks · 1.2 MB   ✓  ✕ ]
  [ DOCX notes.docx        ...                  ⏳ ✕ ]

Signals
    add_requested()          "+ Add document" clicked
    remove_requested(int)    ✕ clicked on a row (doc id)
"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QScrollArea, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

_STATUS = {
    "ready":      ("✓", "rgb(1,190,118)"),
    "processing": ("⏳", "rgb(240,180,50)"),
    "failed":     ("!", "rgb(220,70,70)"),
}


def _fmt_size(n: int) -> str:
    for unit in ("B", "KB", "MB"):
        if n < 1024 or unit == "MB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


class _DocRow(QFrame):
    remove_clicked = pyqtSignal(int)

    def __init__(self, doc: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("docRow")
        self.setFixedHeight(56)
        self.setStyleSheet("""
            QFrame#docRow { background-color: rgb(49,55,67); border-radius: 8px; }
            QFrame#docRow:hover { background-color: rgb(55,62,76); }
            QLabel { background: transparent; border: none; }
        """)
        doc_id = doc["id"]
        filename = doc.get("filename", "unknown")

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 6, 10, 6)
        row.setSpacing(12)

        ext = (doc.get("file_type") or os.path.splitext(filename)[1].lstrip(".")).upper()
        badge = QLabel(ext or "FILE")
        badge.setFixedSize(42, 32)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet("background-color: rgb(72,86,114); border-radius: 6px;"
                            "color: rgba(255,255,255,230); font-size: 8pt; font-weight: bold;")
        row.addWidget(badge)

        col = QVBoxLayout()
        col.setSpacing(1)
        col.setContentsMargins(0, 0, 0, 0)
        name = QLabel(self.fontMetrics().elidedText(filename, Qt.ElideMiddle, 330))
        name.setToolTip(filename)
        name.setStyleSheet("color: rgba(255,255,255,215); font-size: 10pt;")
        col.addWidget(name)

        status = doc.get("status", "")
        parts = [status.capitalize()]
        if status == "ready":
            parts = [f"{doc.get('chunk_count', 0)} chunks"]
        parts.append(_fmt_size(doc.get("size_bytes", 0)))
        meta = QLabel(" · ".join(parts))
        meta.setStyleSheet("color: rgba(255,255,255,100); font-size: 8pt;")
        if doc.get("error"):
            meta.setToolTip(doc["error"])
        col.addWidget(meta)
        row.addLayout(col, 1)

        glyph, color = _STATUS.get(status, ("•", "rgb(150,150,150)"))
        st = QLabel(glyph)
        st.setToolTip(status)
        st.setStyleSheet(f"color: {color}; font-size: 11pt; font-weight: bold;")
        row.addWidget(st)

        x_btn = QPushButton("✕")
        x_btn.setFixedSize(26, 26)
        x_btn.setCursor(Qt.PointingHandCursor)
        x_btn.setToolTip("Remove document")
        x_btn.setStyleSheet("""
            QPushButton { background: rgba(255,255,255,18); color: rgba(255,255,255,150);
                          border: none; border-radius: 13px; font-size: 9pt; }
            QPushButton:hover { background: rgb(232,0,116); color: white; }
        """)
        x_btn.clicked.connect(lambda: self.remove_clicked.emit(doc_id))
        row.addWidget(x_btn)


class DocumentsPanel(QWidget):
    add_requested = pyqtSignal()
    remove_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: transparent;")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)

        # header: count + add button
        header = QHBoxLayout()
        self._count = QLabel("0 documents")
        self._count.setStyleSheet("color: rgba(255,255,255,120); font-size: 9pt;"
                                  "padding-left: 50px; background: transparent;")
        header.addWidget(self._count)
        header.addStretch()
        self.add_btn = QPushButton("+ Add document")
        self.add_btn.setFixedHeight(32)
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setStyleSheet("""
            QPushButton { color: #5a9bd5; border: 2px solid rgba(90,155,213,200);
                          border-radius: 8px; padding: 0 14px; background: transparent; }
            QPushButton:hover { background-color: rgb(48,54,66);
                                border-color: rgba(90,155,213,160); }
            QPushButton:disabled { color: rgba(255,255,255,70);
                                   border-color: rgba(255,255,255,40); }
        """)
        self.add_btn.clicked.connect(self.add_requested)
        header.addWidget(self.add_btn)
        root.addLayout(header)

        # scrollable list
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self._container = QWidget()
        self._container.setObjectName("docsContainer")
        self._container.setStyleSheet("#docsContainer { background: transparent; }")
        self._list = QVBoxLayout(self._container)
        self._list.setContentsMargins(0, 0, 4, 0)
        self._list.setSpacing(6)
        self._list.setAlignment(Qt.AlignTop)
        self._scroll.setWidget(self._container)
        root.addWidget(self._scroll, 1)

        self._empty = QLabel("No documents yet.\nClick “+ Add document” to upload one.")
        self._empty.setAlignment(Qt.AlignCenter)
        self._empty.setStyleSheet("color: rgba(255,255,255,90); font-size: 10pt;"
                                  "background: transparent; padding: 30px;")
        self._list.addWidget(self._empty)

        self._rows = []

    # ── public API ────────────────────────────────────────────────────────────
    def set_documents(self, docs: list):
        """Replace the whole list (docs = list of DocumentOut dicts)."""
        for r in self._rows:
            r.setParent(None)
            r.deleteLater()
        self._rows = []
        for doc in docs:
            row = _DocRow(doc)
            row.remove_clicked.connect(self.remove_requested)
            self._list.addWidget(row)
            self._rows.append(row)
        self._empty.setVisible(not docs)
        n = len(docs)
        self._count.setText(f"{n} document{'s' if n != 1 else ''}")

    def clear(self):
        self.set_documents([])

    def set_busy(self, busy: bool):
        self.add_btn.setEnabled(not busy)
        self.add_btn.setText("Uploading…" if busy else "+ Add document")