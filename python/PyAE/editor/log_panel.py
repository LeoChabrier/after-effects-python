from __future__ import annotations

import io
from datetime import datetime

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QPushButton
from PySide6.QtGui import QFont

from .themes import _THEMES, small_btn_style


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
        self._btn.setStyleSheet(small_btn_style(t))

    def log(self, text: str, error: bool = False):
        ts = datetime.now().strftime('%H:%M:%S')
        for line in text.rstrip('\n').split('\n'):
            if line:
                self._text.appendPlainText(f'[{ts}] {line}')


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
