from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTextEdit,
)
from PySide6.QtGui import QColor, QTextCursor, QTextDocument
from PySide6.QtCore import Qt

from .themes import _THEMES, small_btn_style

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .code_editor import _CodeEditor


class _FindBar(QWidget):
    def __init__(self, editor: _CodeEditor):
        super().__init__()
        self._editor   = editor
        self._matches  = []
        self._current  = -1
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

    # ── Public API ─────────────────────────────────────────────────────────────

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
        bg  = t['panel_bg']
        fg  = t['editor_fg']
        inp = (f"QLineEdit {{ background:{t['editor_bg']}; color:{fg}; border:1px solid {t['splitter']};"
               f" border-radius:3px; padding:0 4px; }}")
        lbl = f"QLabel {{ color:{fg}; font-size:11px; }}"
        self.setStyleSheet(f"_FindBar {{ background:{bg}; }}" + inp + lbl)
        bs = small_btn_style(t)
        for b in (self._btn_prev, self._btn_next, self._btn_case,
                  self._btn_close, self._btn_repl, self._btn_repl_all):
            b.setStyleSheet(bs)
        self._lbl_count.setStyleSheet(f'color:{t["line_fg"]}; font-size:10px; min-width:50px;')
        self._hl_all = t.get('statusbar', '#007ACC') + '55'
        self._hl_cur = '#FF8C00'

    # ── Search logic ──────────────────────────────────────────────────────────

    def _flags(self):
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
        sels   = []
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
        QTextCursor(self._matches[self._current]).insertText(self._repl_input.text())
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
