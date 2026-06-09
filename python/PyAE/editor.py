import sys
import os
import io
import traceback
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QTreeWidget, QTreeWidgetItem,
    QPlainTextEdit, QToolBar, QFileDialog, QMessageBox,
    QApplication, QMenu, QInputDialog, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStatusBar, QComboBox, QListWidget, QListWidgetItem,
    QLineEdit, QTextEdit,
)
from PySide6.QtGui import (
    QSyntaxHighlighter, QTextCharFormat, QColor, QFont,
    QKeySequence, QAction, QPainter, QTextCursor,
    QShortcut, QIcon, QPixmap,
)
from PySide6.QtCore import Qt, QRegularExpression, QSize, QRect, QRectF, Signal, QPoint, QTimer, QThread

SCRIPTS_DIR = Path(os.environ.get('APPDATA', Path.home())) / 'after-effects-python' / 'scripts'

# ── Themes ────────────────────────────────────────────────────────────────────

_THEMES = {
    'Dark': {
        'editor_bg': '#1E1E1E', 'editor_fg': '#D4D4D4',
        'log_bg':    '#1E1E1E', 'log_fg':    '#9CDCFE',
        'line_bg':   '#252526', 'line_fg':   '#858585',
        'panel_bg':  '#2D2D2D', 'toolbar_bg':'#3C3C3C',
        'splitter':  '#444444', 'statusbar': '#007ACC',
        'outliner_bg':'#252526','outliner_fg':'#CCCCCC','outliner_sel':'#094771',
        'btn_bg':    '#3C3C3C', 'btn_hover': '#505050', 'btn_fg': '#CCCCCC',
        'syn_keyword':  '#C586C0', 'syn_builtin': '#DCDCAA',
        'syn_string':   '#CE9178', 'syn_number':  '#B5CEA8',
        'syn_comment':  '#6A9955',
        'syn_def_name': '#DCDCAA', 'syn_cls_name': '#4EC9B0',
        'syn_self':     '#9CDCFE', 'syn_deco':     '#C586C0',
        'syn_const':    '#9CDCFE', 'syn_magic':    '#DCDCAA',
        'syn_unused':   '#4A4A66',
    },
    'Light': {
        'editor_bg': '#FFFFFF', 'editor_fg': '#1E1E1E',
        'log_bg':    '#F8F8F8', 'log_fg':    '#0070C1',
        'line_bg':   '#F3F3F3', 'line_fg':   '#AAAAAA',
        'panel_bg':  '#E8E8E8', 'toolbar_bg':'#F0F0F0',
        'splitter':  '#CCCCCC', 'statusbar': '#0078D4',
        'outliner_bg':'#F3F3F3','outliner_fg':'#1E1E1E','outliner_sel':'#CCE4FF',
        'btn_bg':    '#E0E0E0', 'btn_hover': '#C8C8C8', 'btn_fg': '#1E1E1E',
        'syn_keyword':  '#AF00DB', 'syn_builtin': '#795E26',
        'syn_string':   '#A31515', 'syn_number':  '#098658',
        'syn_comment':  '#008000',
        'syn_def_name': '#795E26', 'syn_cls_name': '#267F99',
        'syn_self':     '#0000FF', 'syn_deco':     '#AF00DB',
        'syn_const':    '#0070C1', 'syn_magic':    '#795E26',
        'syn_unused':   '#B0B0B0',
    },
    'Aura': {
        'editor_bg': '#15002B', 'editor_fg': '#EDECEE',
        'log_bg':    '#15002B', 'log_fg':    '#A277FF',
        'line_bg':   '#1A0035', 'line_fg':   '#6644AA',
        'panel_bg':  '#1E0040', 'toolbar_bg':'#200045',
        'splitter':  '#3D1A6E', 'statusbar': '#9999FF',
        'outliner_bg':'#1A0035','outliner_fg':'#EDECEE','outliner_sel':'#3D1A6E',
        'btn_bg':    '#2A0055', 'btn_hover': '#3D1A6E', 'btn_fg': '#EDECEE',
        'syn_keyword':  '#FF79C6', 'syn_builtin': '#FFD580',
        'syn_string':   '#F1FA8C', 'syn_number':  '#BD93F9',
        'syn_comment':  '#7970A9',
        'syn_def_name': '#FFD580', 'syn_cls_name': '#80FFEA',
        'syn_self':     '#A277FF', 'syn_deco':     '#FF79C6',
        'syn_const':    '#A277FF', 'syn_magic':    '#FFD580',
        'syn_unused':   '#3A2A4A',
    },
}

# ── Window icon ───────────────────────────────────────────────────────────────

def _make_icon() -> QIcon:
    px = QPixmap(32, 32)
    px.fill(Qt.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor('#252526'))
    p.drawRoundedRect(QRectF(1, 1, 30, 30), 7, 7)
    p.setPen(QColor('#9999FF'))
    f = QFont('Arial', 11, QFont.Bold)
    p.setFont(f)
    p.drawText(QRect(0, 0, 32, 32), Qt.AlignCenter, 'Py')
    p.end()
    return QIcon(px)


def _small_btn_style(t: dict) -> str:
    return (
        f"QPushButton {{ background:{t['btn_bg']}; color:{t['btn_fg']}; "
        f"border:none; border-radius:3px; padding:0 8px; font-size:11px; }}"
        f"QPushButton:hover {{ background:{t['btn_hover']}; }}"
    )


# ── Syntax highlighter ────────────────────────────────────────────────────────

class _PythonHighlighter(QSyntaxHighlighter):
    _KEYWORDS = [
        'False','None','True','and','as','assert','async','await','break',
        'class','continue','def','del','elif','else','except','finally',
        'for','from','global','if','import','in','is','lambda','nonlocal',
        'not','or','pass','raise','return','try','while','with','yield',
    ]
    _BUILTINS = [
        'print','len','range','str','int','float','list','dict','set',
        'tuple','type','isinstance','hasattr','getattr','setattr',
        'enumerate','zip','map','filter','sorted','reversed','open',
        'super','property','staticmethod','classmethod',
    ]

    def __init__(self, parent=None, theme: dict | None = None):
        super().__init__(parent)
        self._rules: list = []
        self._build_rules(theme or _THEMES['Dark'])

    def _build_rules(self, t: dict):
        # Rules stored as (QRegularExpression, QTextCharFormat, capture_group)
        # group=0 → full match, group=1 → first capture group
        self._rules = []

        def fmt(color, bold=False, italic=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:   f.setFontWeight(QFont.Bold)
            if italic: f.setFontItalic(True)
            return f

        R = QRegularExpression

        # Strings (before keywords so f"..." isn't partially re-coloured)
        sf = fmt(t['syn_string'])
        self._rules += [
            (R(r'(f|b|r|rb|br)?"[^"\\]*(\\.[^"\\]*)*"'), sf, 0),
            (R(r"(f|b|r|rb|br)?'[^'\\]*(\\.[^'\\]*)*'"), sf, 0),
        ]

        # Keywords
        kf = fmt(t['syn_keyword'], bold=True)
        for w in self._KEYWORDS:
            self._rules.append((R(r'\b' + w + r'\b'), kf, 0))

        # Decorators (before builtins)
        self._rules.append((R(r'@[\w.]+'), fmt(t['syn_deco']), 0))

        # __dunder__ names
        self._rules.append((R(r'\b__\w+__\b'), fmt(t['syn_magic']), 0))

        # self / cls
        self._rules.append((R(r'\b(self|cls)\b'), fmt(t['syn_self']), 0))

        # def <name>  →  colour only the name (group 1)
        self._rules.append((R(r'\bdef\s+(\w+)'), fmt(t['syn_def_name']), 1))

        # class <name>  →  colour only the name (group 1)
        self._rules.append((R(r'\bclass\s+(\w+)'), fmt(t['syn_cls_name'], bold=True), 1))

        # ALL_CAPS constants (≥3 chars to avoid false positives like 'I')
        self._rules.append((R(r'\b[A-Z][A-Z0-9_]{2,}\b'), fmt(t['syn_const']), 0))

        # Builtins
        bf = fmt(t['syn_builtin'])
        for w in self._BUILTINS:
            self._rules.append((R(r'\b' + w + r'\b'), bf, 0))

        # Floats (before ints to avoid matching the integer part)
        self._rules.append((R(r'\b\d+\.\d*([eE][+-]?\d+)?\b|\b\d*\.\d+([eE][+-]?\d+)?\b'), fmt(t['syn_number']), 0))
        # Ints (hex, bin, oct, decimal)
        self._rules.append((R(r'\b(0x[0-9a-fA-F]+|0b[01]+|0o[0-7]+|\d+)\b'), fmt(t['syn_number']), 0))

        # Comments last (override everything on the line)
        self._rules.append((R(r'#[^\n]*'), fmt(t['syn_comment'], italic=True), 0))

    def update_theme(self, t: dict):
        self._build_rules(t)
        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, fmt, group in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m   = it.next()
                s   = m.capturedStart(group)
                ln  = m.capturedLength(group)
                if s >= 0 and ln > 0:
                    self.setFormat(s, ln, fmt)


# ── Completion popup ─────────────────────────────────────────────────────────

class _CompletionPopup(QListWidget):
    """Floating completion list — child widget of the editor (no separate window)."""

    inserted = Signal()

    _TYPE_ICON = {
        'function': 'ƒ', 'class': 'C', 'module': 'M',
        'keyword':  'k', 'instance': '○', 'statement': '=',
        'param': 'p', '_doc': '·',
    }
    # Fixed colors that read well on dark/light alike
    _TYPE_COLOR = {
        'function':  '#DCDCAA',
        'class':     '#4EC9B0',
        'module':    '#4FC1FF',
        'keyword':   '#C586C0',
        'instance':  '#9CDCFE',
        'statement': '#9CDCFE',
        'param':     '#CE9178',
        '_doc':      '#888888',
    }

    def __init__(self, editor):
        super().__init__(editor.viewport())  # child of viewport — renders ON TOP of text
        self._editor = editor
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFont(QFont('Consolas', 10))
        self.setFixedWidth(300)
        self.setMaximumHeight(200)
        self.itemClicked.connect(self._on_click)
        self.set_theme(_THEMES['Dark'])
        self.hide()

    def set_theme(self, t: dict):
        self.setStyleSheet(
            f"QListWidget {{ background:{t['panel_bg']}; color:{t['editor_fg']}; "
            f"border:1px solid {t['splitter']}; outline:none; }}"
            f"QListWidget::item {{ padding:2px 6px; }}"
            f"QListWidget::item:selected {{ background:{t['statusbar']}; color:#fff; }}"
        )

    def populate(self, completions: list):
        self.clear()
        for c in completions[:30]:
            ctype = getattr(c, 'type', '_doc')
            icon  = self._TYPE_ICON.get(ctype, '·')
            item  = QListWidgetItem(f"{icon}  {c.name}")
            item.setData(Qt.UserRole, c.complete)
            item.setForeground(QColor(self._TYPE_COLOR.get(ctype, '#D4D4D4')))
            self.addItem(item)
        if self.count():
            self.setCurrentRow(0)
            row_h = self.sizeHintForRow(0) + 2
            self.setFixedHeight(min(row_h * self.count() + 6, 200))

    def show_below_cursor(self):
        # cursorRect() is already in viewport coordinates — use directly
        rect = self._editor.cursorRect()
        x    = rect.left()
        y    = rect.bottom() + 2
        # Flip above cursor if too close to bottom of viewport
        vp_h = self._editor.viewport().height()
        if y + self.height() > vp_h - 4:
            y = rect.top() - self.height() - 2
        self.move(QPoint(x, max(0, y)))
        self.raise_()
        self.show()

    def move_selection(self, delta: int):
        self.setCurrentRow(max(0, min(self.currentRow() + delta, self.count() - 1)))

    def accept_current(self):
        item = self.currentItem()
        if item:
            self._editor.insertPlainText(item.data(Qt.UserRole))
        self.hide()
        self._editor.setFocus()
        self.inserted.emit()

    def _on_click(self, item):
        self._editor.insertPlainText(item.data(Qt.UserRole))
        self.hide()
        self._editor.setFocus()
        self.inserted.emit()


# ── Jedi worker (background thread) ─────────────────────────────────────────

class _JediWorker(QThread):
    done = Signal(list)

    def __init__(self):
        super().__init__()
        self._code = ''
        self._line = 1
        self._col  = 0

    def request(self, code: str, line: int, col: int):
        self._code, self._line, self._col = code, line, col

    def run(self):
        try:
            import jedi
            completions = jedi.Script(self._code).complete(self._line, self._col)
            self.done.emit(list(completions))
        except Exception:
            self.done.emit([])


# ── Line number area ──────────────────────────────────────────────────────────

class _LineArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self):
        return QSize(self._editor._line_area_width(), 0)

    def paintEvent(self, event):
        self._editor._paint_line_numbers(event)


# ── Code editor ───────────────────────────────────────────────────────────────

class _CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._font = QFont('Consolas', 11)
        self.setFont(self._font)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self._highlighter = _PythonHighlighter(self.document())
        self._theme = _THEMES['Dark']
        self._apply_editor_style()

        self._line_area = _LineArea(self)
        self.blockCountChanged.connect(self._update_line_area_width)
        self.updateRequest.connect(self._update_line_area)
        self._update_line_area_width(0)

        # Ctrl+/ (QWERTY) + Ctrl+: (AZERTY — same physical key, no Shift needed, mirrors VS Code)
        for ks in ('Ctrl+/', 'Ctrl+:'):
            sc = QShortcut(QKeySequence(ks), self)
            sc.setContext(Qt.WidgetShortcut)
            sc.activated.connect(self._toggle_comment)

        self._popup = _CompletionPopup(self)

        # Debounced completion (150ms for typing, 40ms for '.')
        self._complete_timer = QTimer(self)
        self._complete_timer.setSingleShot(True)
        self._complete_timer.timeout.connect(self._do_complete)

        # Async Jedi worker
        self._jedi_worker = _JediWorker()
        self._jedi_worker.done.connect(self._on_jedi_done)

        # Extra selections: find highlights + unused variables (merged on apply)
        self._search_sels: list = []
        self._unused_sels: list = []

        # Unused variable analysis (1.5s after last edit)
        self._unused_timer = QTimer(self)
        self._unused_timer.setSingleShot(True)
        self._unused_timer.setInterval(1500)
        self._unused_timer.timeout.connect(self._analyze_unused)
        self.document().contentsChanged.connect(self._unused_timer.start)

    def set_theme(self, t: dict):
        self._theme = t
        self._apply_editor_style()
        self._highlighter.update_theme(t)
        self._line_area.update()
        self._popup.set_theme(t)
        self._analyze_unused()  # recolor with new unused tint

    def _apply_editor_style(self):
        t = self._theme
        self.setStyleSheet(
            f'QPlainTextEdit {{ background:{t["editor_bg"]}; color:{t["editor_fg"]}; border:none; }}'
        )

    def _line_area_width(self):
        digits = max(3, len(str(self.blockCount())))
        return 8 + self.fontMetrics().horizontalAdvance('9') * digits

    def _update_line_area_width(self, _=None):
        self.setViewportMargins(self._line_area_width(), 0, 0, 0)

    def _update_line_area(self, rect, dy):
        if dy:
            self._line_area.scroll(0, dy)
        else:
            self._line_area.update(0, rect.y(), self._line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_line_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_area.setGeometry(cr.left(), cr.top(), self._line_area_width(), cr.height())

    def _paint_line_numbers(self, event):
        t = self._theme
        painter = QPainter(self._line_area)
        painter.fillRect(event.rect(), QColor(t['line_bg']))
        painter.setFont(self._font)

        block = self.firstVisibleBlock()
        num   = block.blockNumber()
        top   = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        h     = self.fontMetrics().height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor(t['line_fg']))
                painter.drawText(QRect(0, top, self._line_area.width() - 6, h),
                                 Qt.AlignRight, str(num + 1))
            block  = block.next()
            top    = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            num   += 1

    def _toggle_comment(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        sel_start = cursor.selectionStart()
        sel_end   = cursor.selectionEnd()

        c = self.textCursor()
        c.setPosition(sel_start)
        first_block = c.blockNumber()
        c.setPosition(sel_end)
        last_block  = c.blockNumber()
        if sel_end != sel_start and c.positionInBlock() == 0:
            last_block -= 1

        c.setPosition(sel_start)
        c.movePosition(QTextCursor.StartOfBlock)
        lines = []
        block = c.block()
        for _ in range(last_block - first_block + 1):
            lines.append(block.text())
            block = block.next()

        all_commented = all(ln.lstrip().startswith('#') for ln in lines if ln.strip())

        c.setPosition(sel_start)
        c.movePosition(QTextCursor.StartOfBlock)

        for i, line in enumerate(lines):
            c.movePosition(QTextCursor.StartOfBlock)
            if all_commented:
                stripped = line.lstrip()
                prefix   = '# ' if stripped.startswith('# ') else '#'
                indent   = len(line) - len(line.lstrip())
                c.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, indent)
                c.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(prefix))
                c.removeSelectedText()
            else:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    c.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, indent)
                    c.insertText('# ')
            if i < len(lines) - 1:
                c.movePosition(QTextCursor.NextBlock)

        cursor.endEditBlock()

    def _current_prefix(self) -> str:
        """Return the identifier fragment immediately before the cursor."""
        import re
        text = self.textCursor().block().text()
        col  = self.textCursor().positionInBlock()
        m    = re.search(r'[a-zA-Z_]\w*$', text[:col])
        return m.group() if m else ''

    def _doc_word_completions(self, prefix: str) -> list:
        import re
        if len(prefix) < 2:
            return []
        words   = set(re.findall(r'\b[a-zA-Z_]\w*\b', self.toPlainText()))
        matches = sorted(w for w in words if w.startswith(prefix) and w != prefix)

        class _W:
            def __init__(self, word, pfx):
                self.name     = word
                self.complete = word[len(pfx):]
                self.type     = '_doc'
        return [_W(w, prefix) for w in matches[:30]]

    def _runtime_completions(self) -> list:
        """dir()-based attribute completion using the actual runtime objects."""
        import re, sys
        text_before = self.textCursor().block().text()[:self.textCursor().positionInBlock()]
        m = re.search(r'([\w.]+)\.(\w*)$', text_before)
        if not m:
            return []
        obj_expr = m.group(1)
        prefix   = m.group(2)

        # Eval context: top-level sys.modules + last-run namespace
        ctx = {k: v for k, v in sys.modules.items() if '.' not in k and v is not None}
        ctx.update(getattr(self, '_namespace', {}))

        try:
            obj = eval(obj_expr, ctx)
        except Exception:
            return []

        attrs = [a for a in dir(obj) if a.startswith(prefix) and not a.startswith('_')]
        if not attrs:
            return []

        class _Attr:
            def __init__(self, name, pfx, parent):
                self.name     = name
                self.complete = name[len(pfx):]
                try:
                    self.type = 'function' if callable(getattr(parent, name)) else 'instance'
                except Exception:
                    self.type = 'instance'
        return [_Attr(a, prefix, obj) for a in attrs]

    def _request_completions(self, delay: int = 150):
        """Restart the debounce timer; _do_complete fires after `delay` ms."""
        self._complete_timer.start(delay)

    def _do_complete(self):
        """Called by the debounce timer. Runs fast sync fallbacks immediately,
        kicks off async Jedi in parallel."""
        # Fast sync fallbacks first
        completions = self._runtime_completions()
        if not completions:
            completions = self._doc_word_completions(self._current_prefix())

        if completions:
            self._popup.populate(completions)
            self._popup.show_below_cursor()

        # Start async Jedi (will update popup when done if it returns more)
        code   = self.toPlainText()
        cursor = self.textCursor()
        line   = cursor.blockNumber() + 1
        col    = cursor.positionInBlock()
        if not self._jedi_worker.isRunning():
            self._jedi_worker.request(code, line, col)
            self._jedi_worker.start()

    def _on_jedi_done(self, completions: list):
        """Slot: called when async Jedi finishes. Update popup if still relevant."""
        if not completions:
            return
        # Only replace if prefix still matches (user didn't move on)
        if self._current_prefix() or '.' in (self.textCursor().block().text()
                                              [:self.textCursor().positionInBlock()]):
            self._popup.populate(completions)
            self._popup.show_below_cursor()

    def _apply_extra_sels(self):
        """Merge find highlights + unused variable dim, apply to editor."""
        self.setExtraSelections(self._search_sels + self._unused_sels)

    def _analyze_unused(self):
        """Find Store-only names (never Loaded) and dim them via ExtraSelections."""
        import ast
        code = self.toPlainText()
        self._unused_sels = []
        try:
            tree = ast.parse(code)
        except SyntaxError:
            self._apply_extra_sels()
            return

        stored: dict[str, list[ast.AST]] = {}
        loaded: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):
                    stored.setdefault(node.id, []).append(node)
                elif isinstance(node.ctx, ast.Load):
                    loaded.add(node.id)

        unused_names = {n for n in stored if n not in loaded and not n.startswith('_')}
        if not unused_names:
            self._apply_extra_sels()
            return

        color = QColor(self._theme.get('syn_unused', '#4A4A66'))
        fmt = QTextCharFormat()
        fmt.setForeground(color)

        doc = self.document()
        for name, nodes in stored.items():
            if name not in unused_names:
                continue
            for node in nodes:
                # ast line numbers are 1-based
                block = doc.findBlockByLineNumber(node.lineno - 1)
                if not block.isValid():
                    continue
                start = block.position() + node.col_offset
                length = len(name)
                cursor = self.textCursor()
                cursor.setPosition(start)
                cursor.setPosition(start + length, cursor.KeepAnchor)
                sel = QTextEdit.ExtraSelection()
                sel.cursor = cursor
                sel.format = fmt
                self._unused_sels.append(sel)

        self._apply_extra_sels()

    def focusOutEvent(self, event):
        self._popup.hide()
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        ctrl = bool(event.modifiers() & Qt.ControlModifier)
        key  = event.key()

        # Popup navigation intercept
        if self._popup.isVisible():
            if key == Qt.Key_Down:
                self._popup.move_selection(1);  event.accept(); return
            if key == Qt.Key_Up:
                self._popup.move_selection(-1); event.accept(); return
            if key in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab):
                self._popup.accept_current();   event.accept(); return
            if key == Qt.Key_Escape:
                self._popup.hide();             event.accept(); return
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Home, Qt.Key_End):
                self._popup.hide()

        # Normal edit
        if key == Qt.Key_Tab:
            self.insertPlainText('    ')
            event.accept()
        elif ctrl and key in (Qt.Key_Slash, Qt.Key_Colon):
            self._toggle_comment()
            event.accept()
        elif ctrl and key == Qt.Key_Space:
            self._do_complete()
            event.accept()
        else:
            super().keyPressEvent(event)
            ch = event.text()
            if ch == '.':
                self._request_completions(delay=40)
            elif ch and (ch.isalnum() or ch == '_'):
                if len(self._current_prefix()) >= 2:
                    self._request_completions(delay=150)
                else:
                    self._popup.hide()
            elif key in (Qt.Key_Backspace, Qt.Key_Delete):
                if self._popup.isVisible():
                    self._request_completions(delay=100)
            elif ch and ch not in ('.', '_') and not ch.isalnum():
                self._popup.hide()


# ── Log panel ─────────────────────────────────────────────────────────────────

class _LogPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._text = QPlainTextEdit()
        self._text.setReadOnly(True)
        self._text.setFont(QFont('Consolas', 10))
        layout.addWidget(self._text)

        self._footer = QWidget()
        self._footer.setFixedHeight(28)
        fl = QHBoxLayout(self._footer)
        fl.setContentsMargins(6, 0, 6, 0)
        fl.addStretch()
        self._btn = QPushButton('Clear log')
        self._btn.setFixedHeight(20)
        self._btn.clicked.connect(self._text.clear)
        fl.addWidget(self._btn)
        layout.addWidget(self._footer)

        self.set_theme(_THEMES['Dark'])

    def set_theme(self, t: dict):
        self._text.setStyleSheet(
            f'QPlainTextEdit {{ background:{t["log_bg"]}; color:{t["log_fg"]}; border:none; }}'
        )
        self._footer.setStyleSheet(f'background:{t["panel_bg"]};')
        self._btn.setStyleSheet(_small_btn_style(t))

    def log(self, text: str, error: bool = False):
        ts = datetime.now().strftime('%H:%M:%S')
        for line in text.rstrip('\n').split('\n'):
            if line:
                self._text.appendPlainText(f'[{ts}] {line}')


# ── Find / Replace bar ────────────────────────────────────────────────────────

class _FindBar(QWidget):
    def __init__(self, editor: '_CodeEditor'):
        super().__init__()
        self._editor    = editor
        self._matches   = []
        self._current   = -1
        self._building  = False
        self._build_ui()
        self.hide()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 4, 6, 4)
        root.setSpacing(2)

        # Find row
        fr = QHBoxLayout()
        fr.setSpacing(4)
        self._lbl_find   = QLabel('Find:')
        self._lbl_find.setFixedWidth(36)
        self._find_input = QLineEdit()
        self._find_input.setFixedHeight(24)
        self._find_input.setPlaceholderText('Search…')
        self._find_input.textChanged.connect(self._refresh)
        self._find_input.returnPressed.connect(self._next)

        self._btn_prev  = QPushButton('▲')
        self._btn_next  = QPushButton('▼')
        self._btn_case  = QPushButton('Aa')
        self._btn_close = QPushButton('✕')
        self._lbl_count = QLabel('')
        for b in (self._btn_prev, self._btn_next, self._btn_case, self._btn_close):
            b.setFixedSize(24, 24)
        self._btn_case.setCheckable(True)
        self._btn_prev.clicked.connect(self._prev)
        self._btn_next.clicked.connect(self._next)
        self._btn_case.toggled.connect(lambda _: self._refresh())
        self._btn_close.clicked.connect(self.close_bar)

        fr.addWidget(self._lbl_find)
        fr.addWidget(self._find_input, 1)
        fr.addWidget(self._lbl_count)
        fr.addWidget(self._btn_prev)
        fr.addWidget(self._btn_next)
        fr.addWidget(self._btn_case)
        fr.addWidget(self._btn_close)
        root.addLayout(fr)

        # Replace row (hidden in find-only mode)
        self._repl_row = QWidget()
        rr = QHBoxLayout(self._repl_row)
        rr.setContentsMargins(0, 0, 0, 0)
        rr.setSpacing(4)
        self._lbl_repl   = QLabel('Repl:')
        self._lbl_repl.setFixedWidth(36)
        self._repl_input = QLineEdit()
        self._repl_input.setFixedHeight(24)
        self._repl_input.setPlaceholderText('Replace with…')
        self._btn_repl     = QPushButton('Replace')
        self._btn_repl_all = QPushButton('Replace All')
        self._btn_repl.setFixedHeight(24)
        self._btn_repl_all.setFixedHeight(24)
        self._btn_repl.clicked.connect(self._replace_one)
        self._btn_repl_all.clicked.connect(self._replace_all)
        rr.addWidget(self._lbl_repl)
        rr.addWidget(self._repl_input, 1)
        rr.addWidget(self._btn_repl)
        rr.addWidget(self._btn_repl_all)
        self._repl_row.hide()
        root.addWidget(self._repl_row)

    # ── Public API ────────────────────────────────────────────────────────────

    def open_find(self):
        self._repl_row.hide()
        self.show()
        self._find_input.setFocus()
        self._find_input.selectAll()
        self._refresh()

    def open_replace(self):
        self._repl_row.show()
        self.show()
        self._find_input.setFocus()
        self._find_input.selectAll()
        self._refresh()

    def close_bar(self):
        self.hide()
        self._clear_highlights()
        self._editor.setFocus()

    def set_theme(self, t: dict):
        bg = t['panel_bg']
        fg = t['editor_fg']
        inp = (f"QLineEdit {{ background:{t['editor_bg']}; color:{fg}; border:1px solid {t['splitter']};"
               f" border-radius:3px; padding:0 4px; }}")
        lbl = f"QLabel {{ color:{fg}; font-size:11px; }}"
        self.setStyleSheet(f"_FindBar {{ background:{bg}; }}" + inp + lbl)
        bs = _small_btn_style(t)
        for b in (self._btn_prev, self._btn_next, self._btn_case,
                  self._btn_close, self._btn_repl, self._btn_repl_all):
            b.setStyleSheet(bs)
        self._lbl_count.setStyleSheet(f'color:{t["line_fg"]}; font-size:10px; min-width:50px;')
        # Match highlight colours (stored for _highlight_all)
        self._hl_all  = t.get('statusbar', '#007ACC') + '55'   # semi-transparent
        self._hl_cur  = '#FF8C00'

    # ── Search logic ─────────────────────────────────────────────────────────

    def _flags(self):
        from PySide6.QtGui import QTextDocument
        f = QTextDocument.FindFlags()
        if self._btn_case.isChecked():
            f |= QTextDocument.FindCaseSensitively
        return f

    def _refresh(self):
        query = self._find_input.text()
        doc   = self._editor.document()
        self._matches = []
        if query:
            flags = self._flags()
            c = doc.find(query, 0, flags)
            while not c.isNull():
                self._matches.append(QTextCursor(c))
                c = doc.find(query, c, flags)
        n = len(self._matches)
        if n == 0:
            self._current = -1
            self._lbl_count.setText('No results' if query else '')
        else:
            self._current = max(0, min(self._current, n - 1))
            self._goto(self._current)
        self._highlight_all()

    def _highlight_all(self):
        sels = []
        bg_all = QColor(getattr(self, '_hl_all', '#3D5A8088'))
        bg_cur = QColor(getattr(self, '_hl_cur', '#FF8C00'))
        for i, c in enumerate(self._matches):
            sel = QTextEdit.ExtraSelection()
            sel.format.setBackground(bg_cur if i == self._current else bg_all)
            sel.cursor = c
            sels.append(sel)
        self._editor._search_sels = sels
        self._editor._apply_extra_sels()

    def _goto(self, idx):
        if not self._matches:
            return
        self._current = idx % len(self._matches)
        self._editor.setTextCursor(self._matches[self._current])
        self._editor.ensureCursorVisible()
        self._lbl_count.setText(f'{self._current + 1} / {len(self._matches)}')
        self._highlight_all()

    def _next(self):
        if self._matches:
            self._goto(self._current + 1)

    def _prev(self):
        if self._matches:
            self._goto(self._current - 1)

    def _replace_one(self):
        if not self._matches or self._current < 0:
            return
        c = QTextCursor(self._matches[self._current])
        c.insertText(self._repl_input.text())
        self._refresh()

    def _replace_all(self):
        query = self._find_input.text()
        if not query:
            return
        repl  = self._repl_input.text()
        doc   = self._editor.document()
        flags = self._flags()
        root  = QTextCursor(doc)
        root.beginEditBlock()
        count = 0
        c = doc.find(query, 0, flags)
        while not c.isNull():
            c.insertText(repl)
            count += 1
            c = doc.find(query, c, flags)
        root.endEditBlock()
        self._lbl_count.setText(f'{count} replaced')
        self._matches = []
        self._clear_highlights()

    def _clear_highlights(self):
        self._editor._search_sels = []
        self._editor._apply_extra_sels()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_bar()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if event.modifiers() & Qt.ShiftModifier:
                self._prev()
            else:
                self._next()
        else:
            super().keyPressEvent(event)


# ── Editor section ────────────────────────────────────────────────────────────

class _EditorSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor = _CodeEditor()
        layout.addWidget(self.editor)

        self._find_bar = _FindBar(self.editor)
        layout.addWidget(self._find_bar)

        self._footer = QWidget()
        self._footer.setFixedHeight(28)
        fl = QHBoxLayout(self._footer)
        fl.setContentsMargins(6, 0, 6, 0)
        fl.addStretch()
        self._btn = QPushButton('Clear editor')
        self._btn.setFixedHeight(20)
        self._btn.clicked.connect(self.editor.clear)
        fl.addWidget(self._btn)
        layout.addWidget(self._footer)

        # Ctrl+F / Ctrl+H — active whenever this section or a child has focus
        for ks, fn in (('Ctrl+F', self._find_bar.open_find),
                       ('Ctrl+H', self._find_bar.open_replace)):
            sc = QShortcut(QKeySequence(ks), self)
            sc.setContext(Qt.WidgetWithChildrenShortcut)
            sc.activated.connect(fn)

        self.set_theme(_THEMES['Dark'])

    def set_theme(self, t: dict):
        self.editor.set_theme(t)
        self._find_bar.set_theme(t)
        self._footer.setStyleSheet(f'background:{t["panel_bg"]};')
        self._btn.setStyleSheet(_small_btn_style(t))


# ── Outliner ──────────────────────────────────────────────────────────────────

class _Outliner(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.setMinimumWidth(140)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_menu)
        self.set_theme(_THEMES['Dark'])
        self.refresh()

    def set_theme(self, t: dict):
        self.setStyleSheet(
            f"QTreeWidget {{ background:{t['outliner_bg']}; color:{t['outliner_fg']}; border:none; }}"
            f"QTreeWidget::item:selected {{ background:{t['outliner_sel']}; }}"
        )

    def refresh(self):
        expanded = {self._path(i) for i in self._walk() if i.isExpanded()}
        self.clear()
        if SCRIPTS_DIR.exists():
            self._populate(self.invisibleRootItem(), SCRIPTS_DIR)
        for item in self._walk():
            if self._path(item) in expanded:
                item.setExpanded(True)

    def _populate(self, parent, directory: Path):
        for entry in sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            if entry.is_dir():
                node = QTreeWidgetItem(parent, [entry.name])
                node.setData(0, Qt.UserRole, str(entry))
                self._populate(node, entry)
            elif entry.suffix == '.py':
                item = QTreeWidgetItem(parent, [entry.stem])
                item.setData(0, Qt.UserRole, str(entry))

    def _walk(self):
        def _r(p):
            for i in range(p.childCount()):
                c = p.child(i)
                yield c
                yield from _r(c)
        yield from _r(self.invisibleRootItem())

    def _path(self, item) -> str:
        return item.data(0, Qt.UserRole) or ''

    def _show_menu(self, pos):
        item = self.itemAt(pos)
        menu = QMenu(self)
        menu.addAction('New Script', self._new_script)
        menu.addAction('New Folder', self._new_folder)
        if item:
            path = Path(self._path(item))
            if path.is_file():
                menu.addSeparator()
                menu.addAction('Rename', lambda: self._rename(item, path))
                menu.addAction('Delete', lambda: self._delete(path))
        menu.exec(self.mapToGlobal(pos))

    def _new_script(self):
        name, ok = QInputDialog.getText(self, 'New Script', 'Name:')
        if ok and name:
            SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
            p = SCRIPTS_DIR / (name if name.endswith('.py') else name + '.py')
            p.write_text('import PyFx\n\n', encoding='utf-8')
            self.refresh()

    def _new_folder(self):
        name, ok = QInputDialog.getText(self, 'New Folder', 'Name:')
        if ok and name:
            (SCRIPTS_DIR / name).mkdir(parents=True, exist_ok=True)
            self.refresh()

    def _rename(self, item, path: Path):
        name, ok = QInputDialog.getText(self, 'Rename', 'New name:', text=path.name)
        if ok and name:
            path.rename(path.parent / name)
            self.refresh()

    def _delete(self, path: Path):
        if QMessageBox.question(self, 'Delete', f'Delete {path.name}?') == QMessageBox.Yes:
            path.unlink()
            self.refresh()


# ── Log capture ───────────────────────────────────────────────────────────────

class _LogCapture(io.RawIOBase):
    def __init__(self, panel: _LogPanel, error: bool = False):
        self._panel = panel
        self._error = error
        self._buf   = ''

    def write(self, text):
        self._buf += text
        while '\n' in self._buf:
            line, self._buf = self._buf.split('\n', 1)
            if line:
                self._panel.log(line, error=self._error)
        return len(text)

    def flush(self):
        if self._buf.strip():
            self._panel.log(self._buf, error=self._error)
            self._buf = ''


# ── Main window ───────────────────────────────────────────────────────────────

class ScriptEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Python Script Editor')
        self.setWindowIcon(_make_icon())
        self.resize(1100, 720)
        self._current_file: Path | None = None
        self._loading     = False
        self._pinned      = False
        self._theme_name  = 'Dark'
        SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        self._build_ui()
        self._build_toolbar()
        self._build_statusbar()
        self._apply_theme('Dark')

    def _build_ui(self):
        central = QWidget()
        central.setObjectName('central')
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._h_split = QSplitter(Qt.Horizontal)
        self._outliner = _Outliner()
        self._outliner.itemDoubleClicked.connect(self._open_from_outliner)
        self._h_split.addWidget(self._outliner)

        self._v_split = QSplitter(Qt.Vertical)
        self._log            = _LogPanel()
        self._editor_section = _EditorSection()
        self._editor         = self._editor_section.editor
        self._editor.document().contentsChanged.connect(self._on_content_changed)
        self._v_split.addWidget(self._log)
        self._v_split.addWidget(self._editor_section)
        self._v_split.setSizes([220, 460])

        self._h_split.addWidget(self._v_split)
        self._h_split.setSizes([180, 920])
        layout.addWidget(self._h_split)

    def _build_toolbar(self):
        tb: QToolBar = self.addToolBar('Main')
        tb.setMovable(False)
        tb.setIconSize(QSize(16, 16))
        self._tb = tb

        toggle = QAction('≡', self)
        toggle.setToolTip('Toggle outliner')
        toggle.triggered.connect(self._toggle_outliner)
        tb.addAction(toggle)
        tb.addSeparator()

        for label, shortcut, slot in [
            ('New',  QKeySequence.New,  self._new_file),
            ('Open', QKeySequence.Open, self._open_file),
            ('Save', QKeySequence.Save, self._save_file),
        ]:
            act = QAction(label, self)
            act.setShortcut(shortcut)
            act.triggered.connect(slot)
            tb.addAction(act)

        tb.addSeparator()

        run = QAction('▶  Run', self)
        run.setShortcut(QKeySequence('Ctrl+Return'))
        run.triggered.connect(self._run)
        tb.addAction(run)

        tb.addSeparator()

        # Always-on-top pin
        self._pin_action = QAction('⊤', self)
        self._pin_action.setToolTip('Always on top')
        self._pin_action.setCheckable(True)
        self._pin_action.toggled.connect(self._toggle_pin)
        tb.addAction(self._pin_action)

        tb.addSeparator()

        # Theme selector
        self._theme_combo = QComboBox()
        self._theme_combo.addItems(list(_THEMES.keys()))
        self._theme_combo.setFixedWidth(80)
        self._theme_combo.setToolTip('Color theme')
        self._theme_combo.currentTextChanged.connect(self._apply_theme)
        tb.addWidget(self._theme_combo)

    def _build_statusbar(self):
        self._sb = QStatusBar()
        self._sb.setSizeGripEnabled(False)
        self._status_file = QLabel('Untitled')
        self._sb.addPermanentWidget(self._status_file)
        self.setStatusBar(self._sb)

    # ── Theme ─────────────────────────────────────────────────────────────────

    def _apply_theme(self, name: str):
        self._theme_name = name
        t = _THEMES[name]

        splitter_style = (
            f"QSplitter::handle:vertical   {{ background:{t['splitter']}; height:2px; }}"
            f"QSplitter::handle:horizontal {{ background:{t['splitter']}; width:2px; }}"
        )
        self._h_split.setStyleSheet(splitter_style)
        self._v_split.setStyleSheet(splitter_style)

        self._outliner.set_theme(t)
        self._log.set_theme(t)
        self._editor_section.set_theme(t)

        self._tb.setStyleSheet(
            f"QToolBar {{ background:{t['toolbar_bg']}; border:none; spacing:4px; padding:2px 6px; }}"
            f"QToolButton {{ color:{t['btn_fg']}; padding:4px 10px; border:none; border-radius:3px; }}"
            f"QToolButton:hover {{ background:{t['btn_hover']}; }}"
            f"QToolButton:pressed, QToolButton:checked {{ background:{t['statusbar']}; color:#fff; }}"
        )
        self._theme_combo.setStyleSheet(
            f"QComboBox {{ background:{t['btn_bg']}; color:{t['btn_fg']}; "
            f"border:none; border-radius:3px; padding:2px 6px; }}"
            f"QComboBox::drop-down {{ border:none; }}"
            f"QComboBox QAbstractItemView {{ background:{t['panel_bg']}; color:{t['btn_fg']}; }}"
        )
        self._sb.setStyleSheet(
            f"QStatusBar {{ background:{t['statusbar']}; color:#fff; font-size:11px; }}"
        )
        self._status_file.setStyleSheet('color:white; padding:0 8px;')
        self.setStyleSheet(f'QMainWindow, QWidget#central {{ background:{t["editor_bg"]}; }}')

    # ── Pin ───────────────────────────────────────────────────────────────────

    def _toggle_pin(self, checked: bool):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()

    # ── Outliner toggle ───────────────────────────────────────────────────────

    def _toggle_outliner(self):
        if self._outliner.isVisible():
            self._outliner_width = self._h_split.sizes()[0]
            self._outliner.hide()
        else:
            self._outliner.show()
            w     = getattr(self, '_outliner_width', 180)
            total = sum(self._h_split.sizes())
            self._h_split.setSizes([w, total - w])

    # ── File ops ──────────────────────────────────────────────────────────────

    def _on_content_changed(self):
        if not self._loading:
            title = self.windowTitle()
            if not title.startswith('*'):
                self.setWindowTitle('* ' + title)

    def _confirm_discard(self):
        if not self.windowTitle().startswith('*'):
            return True
        return QMessageBox.question(self, 'Unsaved changes', 'Discard unsaved changes?') == QMessageBox.Yes

    def _load(self, path: Path):
        self._loading = True
        self._editor.setPlainText(path.read_text(encoding='utf-8'))
        self._loading = False
        self._current_file = path
        self.setWindowTitle(f'Python Script Editor - {path.name}')
        self._status_file.setText(path.name)

    def _new_file(self):
        if not self._confirm_discard():
            return
        self._loading = True
        self._editor.setPlainText('import PyFx\n\n')
        self._loading = False
        self._current_file = None
        self.setWindowTitle('Python Script Editor')
        self._status_file.setText('Untitled')

    def _open_file(self):
        if not self._confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(self, 'Open Script', str(SCRIPTS_DIR), 'Python (*.py)')
        if path:
            self._load(Path(path))

    def _save_file(self):
        if self._current_file is None:
            path, _ = QFileDialog.getSaveFileName(self, 'Save Script', str(SCRIPTS_DIR), 'Python (*.py)')
            if not path:
                return
            self._current_file = Path(path)
        self._current_file.write_text(self._editor.toPlainText(), encoding='utf-8')
        self.setWindowTitle(f'Python Script Editor - {self._current_file.name}')
        self._status_file.setText(self._current_file.name)
        self._outliner.refresh()

    def _open_from_outliner(self, item):
        path = Path(item.data(0, Qt.UserRole) or '')
        if path.is_file() and self._confirm_discard():
            self._load(path)
            self._log._text.clear()

    # ── Run ───────────────────────────────────────────────────────────────────

    def _run(self):
        code = self._editor.toPlainText().strip()
        if not code:
            return

        namespace: dict = {'__name__': '__main__'}
        try:
            import PyFx
            namespace['PyFx'] = PyFx
        except ImportError:
            pass

        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = _LogCapture(self._log, error=False)
        sys.stderr = _LogCapture(self._log, error=True)
        try:
            exec(compile(code, str(self._current_file or '<editor>'), 'exec'), namespace)
        except SystemExit:
            pass
        except Exception:
            self._log.log(traceback.format_exc(), error=True)
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            sys.stdout, sys.stderr = old_out, old_err

        # Expose run namespace to editor for runtime completion (proj_suite. etc.)
        self._editor._namespace = {k: v for k, v in namespace.items()
                                    if k not in ('__name__', '__builtins__', '__doc__')}


# ── Entry point ───────────────────────────────────────────────────────────────

_window: ScriptEditorWindow | None = None


def main():
    global _window
    QApplication.instance() or QApplication(sys.argv)
    if _window is not None and _window.isVisible():
        _window.raise_()
        _window.activateWindow()
        return
    _window = ScriptEditorWindow()
    _window.show()


if __name__ == '__main__':
    main()
    sys.exit(QApplication.instance().exec())
