from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QTextBrowser,
    QScrollArea
)

from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtGui import (
    QFont,
    QFontMetrics,
    QTextDocument,
    QTextTable,
    QPainter,
    QPainterPath,
    QColor,
    QPen
)

import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
import re

# We use Pygments directly instead of CodeHiliteExtension
# because Qt's HTML renderer can't handle CSS classes properly
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import HtmlFormatter
    from pygments.util import ClassNotFound
    PYGMENTS_OK = True
except ImportError:
    PYGMENTS_OK = False

# Fenced code block pattern  ─────────────────────────────────────────────
# Matches ```lang\n code \n``` including triple backticks with optional lang
_FENCE_RE = re.compile(
    r'```(\w*)\n(.*?)```',
    re.DOTALL
)

# ── Inline-style formatter ─────────────────────────────────────────────
if PYGMENTS_OK:
    _FORMATTER = HtmlFormatter(
        style='monokai',
        noclasses=True,   # inline style= attributes — Qt renders these
        nowrap=False,     # let Pygments emit its own <div><pre>...</pre></div>
    )


class CodeTextBrowser(QTextBrowser):
    """QTextBrowser with rounded code-block backgrounds."""

    CODE_BG = QColor("#303541")
    CODE_BORDER = QColor("#454d5c")
    CODE_RADIUS = 10

    CODE_LEFT_MARGIN = 0
    CODE_RIGHT_MARGIN = 50

    def paintEvent(self, event):
        document = self.document()
        layout = document.documentLayout()
        root = document.rootFrame()

        scroll_x = self.horizontalScrollBar().value()
        scroll_y = self.verticalScrollBar().value()

        code_rects = []

        # ---------------------------------------------------------
        # Find code tables
        # ---------------------------------------------------------

        for frame in root.childFrames():
            if not isinstance(frame, QTextTable):
                continue

            rect = layout.frameBoundingRect(frame)

            # Convert document coordinates → viewport coordinates
            x = rect.x() - scroll_x
            y = rect.y() - scroll_y
            w = rect.width()
            h = rect.height()

            # Add margins
            x += self.CODE_LEFT_MARGIN
            w -= (
                self.CODE_LEFT_MARGIN
                + self.CODE_RIGHT_MARGIN
            )

            # Small vertical correction
            y += 1
            h -= 2
            if w <= 20 or h <= 5:
                continue
            if y + h < 0:
                continue
            if y > self.viewport().height():
                continue
            code_rects.append(
                (x, y, w, h)
            )

        # ---------------------------------------------------------
        # Paint rounded backgrounds FIRST
        # ---------------------------------------------------------

        painter = QPainter(
            self.viewport()
        )
        painter.setRenderHint(
            QPainter.Antialiasing,
            True
        )
        for x, y, w, h in code_rects:
            path = QPainterPath()
            path.addRoundedRect(
                x,
                y,
                w,
                h,
                self.CODE_RADIUS,
                self.CODE_RADIUS
            )
            painter.fillPath(
                path,
                self.CODE_BG
            )
        painter.end()

        # ---------------------------------------------------------
        # Let QTextBrowser paint the code/text
        # ---------------------------------------------------------

        super().paintEvent(event)

        # ---------------------------------------------------------
        # Paint rounded borders AFTER text
        # ---------------------------------------------------------

        painter = QPainter(
            self.viewport()
        )
        painter.setRenderHint(
            QPainter.Antialiasing,
            True
        )
        painter.setPen(
            QPen(
                self.CODE_BORDER,
                1
            )
        )
        painter.setBrush(
            Qt.NoBrush
        )
        for x, y, w, h in code_rects:
            path = QPainterPath()
            path.addRoundedRect(
                x,
                y,
                w,
                h,
                self.CODE_RADIUS,
                self.CODE_RADIUS
            )

            painter.drawPath(
                path
            )

        painter.end()
        

def _highlight_code(code, lang):
    """Return a dark, syntax-highlighted code block."""

    if not PYGMENTS_OK:
        escaped = (code.replace("&", "&amp;")
                       .replace("<", "&lt;")
                       .replace(">", "&gt;"))

        return (
            '<table cellspacing="0" cellpadding="0" width="96%" '
            'style="background:transparent; border:none; margin:10px 0;">'
            '<tr><td style="padding:14px 16px; background:transparent;">'
            '<pre style="margin:0; padding:0; '
            'font-family:Consolas,\'Courier New\',monospace; '
            'font-size:9.5pt; line-height:1.6; '
            'white-space:pre-wrap; '
            'color:#e6edf3; '
            'background:transparent;">'
            f'{escaped}'
            '</pre>'
            '</td></tr></table>'
        )

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
    except ClassNotFound:
        try:
            lexer = guess_lexer(code)
        except ClassNotFound:
            lexer = TextLexer()

    raw_html = highlight(code, lexer, _FORMATTER)

    # Remove Pygments wrapper
    inner = re.sub(
        r'^<div[^>]*>(.*)</div>\s*$',
        r'\1',
        raw_html,
        flags=re.DOTALL
    )

    # Make the code text fit our design
    inner = re.sub(
        r'<pre[^>]*>',
        '<pre style="'
        'margin-left:20;'
        'padding:0;'
        'font-family:Consolas,\'Courier New\',monospace;'
        'font-size:10pt;'
        'line-height:1.2;'
        'white-space:pre-wrap;'
        'word-wrap:break-word;'
        'background:transparent;'
        'color:#e6edf3;'
        '">',
        inner
    )

    return (
        '<table cellspacing="0" cellpadding="0" width="100%" '
        'style="background:transparent; '
        'border:none; '
        'margin:0px 0;">'
        '<tr>'
        '<td style="padding:10px 10px; background:transparent;">'
        f'{inner}'
        '</td>'
        '</tr>'
        '</table>'
    )

def build_html(text):
    """
    Convert markdown to HTML with proper Pygments syntax highlighting.
    Fenced code blocks are extracted, highlighted with inline styles,
    then reinserted so Qt's limited HTML renderer handles them correctly.
    """
    placeholders = {}

    def sub_fence(m):
        lang = m.group(1).strip() or 'text'
        code = m.group(2)
        key  = f'CODEBLOCK{len(placeholders)}END'
        placeholders[key] = _highlight_code(code, lang)
        return f'\n\n`{key}`\n\n'

    text_with_placeholders = _FENCE_RE.sub(sub_fence, text)

    body = markdown.markdown(
        text_with_placeholders,
        extensions=['tables']
    )

    # Restore highlighted blocks — markdown wraps our key in <p><code>KEY</code></p>
    for key, html in placeholders.items():
        body = body.replace(f'<p><code>{key}</code></p>', html)
        body = body.replace(f'`{key}`', html)

    base_css = """
    <style>
    * { box-sizing: border-box; }
    body {
        color: rgba(255,255,255,220);
        font-family: 'Roboto', sans-serif;
        font-size: 10pt;
        margin: 0; padding: 0;
        background: transparent;
    }
    p { margin: 0 0 6px 0; line-height: 1.45; }
    p:last-child { margin-bottom: 0; }
    h1,h2,h3,h4 {
        color: rgba(255,255,255,230);
        margin: 8px 0 3px 0;
        line-height: 1.3;
    }
    ul,ol { margin: 2px 0 6px 0; padding-left: 20px; }
    li { margin: 1px 0; line-height: 1.45; }
    strong { color: white; }
    em { color: rgba(255,255,255,180); }
    p code, li code {
        font-family: 'Consolas', monospace;
        font-size: 9.5pt;
        background-color: rgba(110,118,129,0.2);
        color: rgba(255,255,255,210);
        padding: 1px 6px;
        border-radius: 4px;
        border: 1px solid rgba(110,118,129,0.3);
    }
    </style>
    """

    return base_css + body

def _get_scroll_area_viewport_width(widget):
    p = widget.parent()
    while p is not None:
        if isinstance(p, QScrollArea):
            return max(p.viewport().width() - 10, 100)
        p = p.parent()
    return None


class ChatBubble(QWidget):
    _FONT    = QFont("Roboto", 10)
    _MAX_W   = 550
    _PADDING = 52
    _CHIP_H  = 52    # height of attachment chip inside bubble
    _CHIP_GAP = 6    # gap between chip and text

    def __init__(self, text="", is_user=False, available_width=800, attachment=None):
        super().__init__()
        self.is_user          = is_user
        self._available_width = available_width
        self._user_text       = text if is_user else ""
        self._attachment      = attachment
        self._shown_once      = False
        self._streaming       = False

        self._height_timer = QTimer(self)
        self._height_timer.setSingleShot(True)
        self._height_timer.setInterval(150)
        self._height_timer.timeout.connect(self._do_adjust_height)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(10, 4, 10, 4)
        outer.setSpacing(0)

        self.bubble = QFrame()
        bubble_layout = QVBoxLayout(self.bubble)
        bubble_layout.setContentsMargins(12, 10, 12, 10)
        bubble_layout.setSpacing(self._CHIP_GAP)

        self.label = CodeTextBrowser()
        self.label.setOpenExternalLinks(True)
        self.label.setFrameShape(QTextBrowser.NoFrame)
        self.label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label.setMinimumHeight(36)
        self.label.document().setDocumentMargin(2)

        if is_user:
            self.bubble.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
            self.bubble.setStyleSheet(
                "QFrame { background-color: #1a56a0; border-radius: 12px; }")
            self.label.setStyleSheet(
                "QTextBrowser { color: white; background: transparent; "
                "font-family: Roboto; font-size: 10pt; border: none; }")

            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            outer.addWidget(spacer, 1)
            outer.addWidget(self.bubble, 0)
            self.bubble.setMaximumWidth(self._MAX_W)

            # ── Attachment chip inside the bubble (above text) ─────────
            if attachment:
                chip = self._build_chip(attachment)
                bubble_layout.addWidget(chip)

            bubble_layout.addWidget(self.label)

            if text:
                self.label.setPlainText(text)
                self._size_user_bubble(text, available_width, has_chip=bool(attachment))

        else:
            self.bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.bubble.setStyleSheet(
                "QFrame { background: transparent; border: none; }")
            self.label.setStyleSheet(
                "QTextBrowser { color: rgba(255,255,255,220); "
                "background: transparent; font-family: Roboto; "
                "font-size: 10pt; border: none; }")
            bubble_layout.addWidget(self.label)
            outer.addWidget(self.bubble, 1)

            if text:
                self.label.setHtml(build_html(text))
                QTimer.singleShot(0, self._do_adjust_height)

    def _build_chip(self, attachment):
        """Small file chip shown inside the user bubble above the text."""
        import os
        from PyQt5.QtWidgets import QLabel
        from PyQt5.QtGui import QPixmap, QPainter, QPainterPath

        chip = QFrame()
        chip.setFixedHeight(self._CHIP_H)
        chip.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        chip.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,18);
                border-radius: 8px;
                border: none;
            }
        """)
        row = QHBoxLayout(chip)
        row.setContentsMargins(8, 6, 10, 6)
        row.setSpacing(8)

        # Thumbnail or extension badge
        thumb = QLabel()
        thumb.setAlignment(Qt.AlignCenter)
        px = attachment.get("pixmap")
        if px and not px.isNull():
            scaled = px.scaled(40, 36, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            thumb.setPixmap(scaled)
            thumb.setFixedSize(40, 36)
        else:
            ext = os.path.splitext(attachment["filename"])[1].upper().lstrip('.') or "FILE"
            thumb.setText(ext)
            thumb.setFixedSize(36, 30)
            thumb.setStyleSheet("""
                background-color: rgba(255,255,255,22);
                border-radius: 5px;
                color: white;
                font-size: 8px;
                font-family: 'Roboto';
                font-weight: bold;
            """)
        row.addWidget(thumb)

        # Filename label
        from PyQt5.QtWidgets import QVBoxLayout as _VL
        col = _VL()
        col.setSpacing(1)
        col.setContentsMargins(0, 0, 0, 0)

        fn_lbl = QLabel()
        fn_lbl.setText(fn_lbl.fontMetrics().elidedText(
            attachment["filename"], Qt.ElideMiddle, 180))
        fn_lbl.setToolTip(attachment["filename"])
        fn_lbl.setStyleSheet(
            "color: rgba(255,255,255,210); font-family:'Roboto';"
            "font-size:9pt; background:transparent; border:none;")
        col.addWidget(fn_lbl)

        ext_str = os.path.splitext(attachment["filename"])[1].upper().lstrip('.')
        type_lbl = QLabel(f"{ext_str} file" if ext_str else "file")
        type_lbl.setStyleSheet(
            "color: rgba(255,255,255,90); font-family:'Roboto';"
            "font-size:8pt; background:transparent; border:none;")
        col.addWidget(type_lbl)

        row.addLayout(col)
        row.addStretch()
        return chip
    
     # ── Streaming ──────────────────────────────────────────────────────────────
    def start_stream(self):
        self._streaming = True
        self.label.setFixedHeight(36)

    def append_stream(self, full_text):
        self.label.setPlainText(full_text)
        if not self._height_timer.isActive():
            self._height_timer.start()

    def finish_stream(self, full_text):
        self._streaming = False
        self._height_timer.stop()
        self.label.setHtml(build_html(full_text))
        QTimer.singleShot(0, self._do_adjust_height)

    def _measure_text(self, text, max_inner_w):
        doc = QTextDocument()
        doc.setDefaultFont(self._FONT)
        doc.setPlainText(text)
        doc.setTextWidth(-1)
        natural_w = int(doc.idealWidth()) + 1
        if natural_w <= max_inner_w:
            doc.setTextWidth(natural_w)
        else:
            natural_w = max_inner_w
            doc.setTextWidth(max_inner_w)
        return natural_w, int(doc.size().height())

    def _size_user_bubble(self, text, container_width, has_chip=False):
        max_bubble_w = min(container_width, self._MAX_W)
        max_inner_w  = max(max_bubble_w - self._PADDING, 60)
        natural_w, wrapped_h = self._measure_text(text, max_inner_w)

        # If there's a chip, bubble must be at least wide enough for it
        min_w = (200 + self._PADDING) if has_chip else 60
        bubble_w = max(min(natural_w + self._PADDING, max_bubble_w), min_w)

        chip_extra = (self._CHIP_H + self._CHIP_GAP) if has_chip else 0

        self.bubble.setFixedWidth(bubble_w)
        self.label.setFixedHeight(max(36, wrapped_h + 8))

        # Set overall bubble frame height to include chip
        total_h = chip_extra + max(36, wrapped_h + 8) + 20  # 20 = top+bottom padding
        self.bubble.setFixedHeight(total_h)
        self.updateGeometry()

    def showEvent(self, event):
        super().showEvent(event)
        if self.is_user and self._user_text and not self._shown_once:
            self._shown_once = True
            vp_w = _get_scroll_area_viewport_width(self)
            if vp_w and vp_w > 50:
                self._size_user_bubble(self._user_text, vp_w,
                                       has_chip=bool(self._attachment))
            else:
                bw = self.bubble.width()
                if bw > 20:
                    self._size_user_bubble(self._user_text, bw + self._PADDING,
                                           has_chip=bool(self._attachment))

    def _do_adjust_height(self):
        width = self.label.viewport().width()
        if width < 10:
            vp = _get_scroll_area_viewport_width(self)
            width = vp if vp else max(self._available_width - 60, 400)
        self.label.document().setTextWidth(width)
        doc_h = int(self.label.document().size().height())
        self.label.setFixedHeight(max(36, doc_h + 16))
        self.updateGeometry()
