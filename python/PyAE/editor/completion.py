from PySide6.QtWidgets import QListWidget, QListWidgetItem
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Signal, QThread, QPoint

from .themes import _THEMES


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


class _CompletionPopup(QListWidget):
    """Floating completion list — child widget of the editor viewport."""

    inserted = Signal()

    _TYPE_ICON = {
        'function': 'ƒ', 'class': 'C', 'module': 'M',
        'keyword':  'k', 'instance': '○', 'statement': '=',
        'param': 'p', '_doc': '·',
    }
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
        super().__init__(editor.viewport())
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
        rect = self._editor.cursorRect()
        x    = rect.left()
        y    = rect.bottom() + 2
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
