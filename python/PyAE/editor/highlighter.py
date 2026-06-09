from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

from .themes import _THEMES


class _PythonHighlighter(QSyntaxHighlighter):
    _KEYWORDS = [
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break',
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal',
        'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
    ]
    _BUILTINS = [
        'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set',
        'tuple', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr',
        'enumerate', 'zip', 'map', 'filter', 'sorted', 'reversed', 'open',
        'super', 'property', 'staticmethod', 'classmethod',
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
                m  = it.next()
                s  = m.capturedStart(group)
                ln = m.capturedLength(group)
                if s >= 0 and ln > 0:
                    self.setFormat(s, ln, fmt)
