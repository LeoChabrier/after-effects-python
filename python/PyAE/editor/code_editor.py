from __future__ import annotations

import re
import ast

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtGui import (
    QFont, QTextCursor, QTextCharFormat, QColor, QPainter,
    QKeySequence, QShortcut,
)
from PySide6.QtCore import Qt, QSize, QRect, QTimer

from .themes import _THEMES
from .highlighter import _PythonHighlighter
from .completion import _CompletionPopup, _JediWorker


class _LineArea(QWidget):
    def __init__(self, editor: _CodeEditor):
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self):
        return QSize(self._editor._line_area_width(), 0)

    def paintEvent(self, event):
        self._editor._paint_line_numbers(event)


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

        # Ctrl+/ (QWERTY) + Ctrl+: (AZERTY)
        for ks in ('Ctrl+/', 'Ctrl+:'):
            sc = QShortcut(QKeySequence(ks), self)
            sc.setContext(Qt.WidgetShortcut)
            sc.activated.connect(self._toggle_comment)

        self._popup = _CompletionPopup(self)

        # Debounced completion (40ms for '.', 150ms for typing)
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
        self._analyze_unused()

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

        block  = self.firstVisibleBlock()
        num    = block.blockNumber()
        top    = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())
        h      = self.fontMetrics().height()

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
        text = self.textCursor().block().text()
        col  = self.textCursor().positionInBlock()
        m    = re.search(r'[a-zA-Z_]\w*$', text[:col])
        return m.group() if m else ''

    def _doc_word_completions(self, prefix: str) -> list:
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
        import sys
        text_before = self.textCursor().block().text()[:self.textCursor().positionInBlock()]
        m = re.search(r'([\w.]+)\.(\w*)$', text_before)
        if not m:
            return []
        obj_expr = m.group(1)
        prefix   = m.group(2)

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
        self._complete_timer.start(delay)

    def _do_complete(self):
        completions = self._runtime_completions()
        if not completions:
            completions = self._doc_word_completions(self._current_prefix())

        if completions:
            self._popup.populate(completions)
            self._popup.show_below_cursor()

        code   = self.toPlainText()
        cursor = self.textCursor()
        line   = cursor.blockNumber() + 1
        col    = cursor.positionInBlock()
        if not self._jedi_worker.isRunning():
            self._jedi_worker.request(code, line, col)
            self._jedi_worker.start()

    def _on_jedi_done(self, completions: list):
        if not completions:
            return
        if self._current_prefix() or '.' in (self.textCursor().block().text()
                                              [:self.textCursor().positionInBlock()]):
            self._popup.populate(completions)
            self._popup.show_below_cursor()

    def _apply_extra_sels(self):
        self.setExtraSelections(self._search_sels + self._unused_sels)

    def _analyze_unused(self):
        code = self.toPlainText()
        self._unused_sels = []
        try:
            tree = ast.parse(code)
        except SyntaxError:
            self._apply_extra_sels()
            return

        stored: dict[str, list] = {}
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
                block = doc.findBlockByLineNumber(node.lineno - 1)
                if not block.isValid():
                    continue
                start  = block.position() + node.col_offset
                length = len(name)
                cursor = self.textCursor()
                cursor.setPosition(start)
                cursor.setPosition(start + length, cursor.KeepAnchor)
                sel = QTextEdit.ExtraSelection()
                sel.cursor = cursor
                sel.format  = fmt
                self._unused_sels.append(sel)

        self._apply_extra_sels()

    def focusOutEvent(self, event):
        self._popup.hide()
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        ctrl = bool(event.modifiers() & Qt.ControlModifier)
        key  = event.key()

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
