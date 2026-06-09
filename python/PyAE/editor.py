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
    QPushButton, QLabel, QStatusBar, QComboBox,
)
from PySide6.QtGui import (
    QSyntaxHighlighter, QTextCharFormat, QColor, QFont,
    QKeySequence, QAction, QPainter, QTextCursor,
    QShortcut, QIcon, QPixmap,
)
from PySide6.QtCore import Qt, QRegularExpression, QSize, QRect, QRectF

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
        'syn_keyword': '#C586C0', 'syn_builtin': '#DCDCAA',
        'syn_string':  '#CE9178', 'syn_number':  '#B5CEA8',
        'syn_comment': '#6A9955',
    },
    'Light': {
        'editor_bg': '#FFFFFF', 'editor_fg': '#1E1E1E',
        'log_bg':    '#F8F8F8', 'log_fg':    '#0070C1',
        'line_bg':   '#F3F3F3', 'line_fg':   '#AAAAAA',
        'panel_bg':  '#E8E8E8', 'toolbar_bg':'#F0F0F0',
        'splitter':  '#CCCCCC', 'statusbar': '#0078D4',
        'outliner_bg':'#F3F3F3','outliner_fg':'#1E1E1E','outliner_sel':'#CCE4FF',
        'btn_bg':    '#E0E0E0', 'btn_hover': '#C8C8C8', 'btn_fg': '#1E1E1E',
        'syn_keyword': '#AF00DB', 'syn_builtin': '#795E26',
        'syn_string':  '#A31515', 'syn_number':  '#098658',
        'syn_comment': '#008000',
    },
    'Aura': {
        'editor_bg': '#15002B', 'editor_fg': '#EDECEE',
        'log_bg':    '#15002B', 'log_fg':    '#A277FF',
        'line_bg':   '#1A0035', 'line_fg':   '#6644AA',
        'panel_bg':  '#1E0040', 'toolbar_bg':'#200045',
        'splitter':  '#3D1A6E', 'statusbar': '#9999FF',
        'outliner_bg':'#1A0035','outliner_fg':'#EDECEE','outliner_sel':'#3D1A6E',
        'btn_bg':    '#2A0055', 'btn_hover': '#3D1A6E', 'btn_fg': '#EDECEE',
        'syn_keyword': '#FF79C6', 'syn_builtin': '#FFD580',
        'syn_string':  '#F1FA8C', 'syn_number':  '#BD93F9',
        'syn_comment': '#7970A9',
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
        self._rules = []

        kw = QTextCharFormat()
        kw.setForeground(QColor(t['syn_keyword']))
        kw.setFontWeight(QFont.Bold)
        for w in self._KEYWORDS:
            self._rules.append((QRegularExpression(r'\b' + w + r'\b'), kw))

        bi = QTextCharFormat()
        bi.setForeground(QColor(t['syn_builtin']))
        for w in self._BUILTINS:
            self._rules.append((QRegularExpression(r'\b' + w + r'\b'), bi))

        s = QTextCharFormat()
        s.setForeground(QColor(t['syn_string']))
        self._rules += [
            (QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), s),
            (QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), s),
        ]

        n = QTextCharFormat()
        n.setForeground(QColor(t['syn_number']))
        self._rules.append((QRegularExpression(r'\b\d+\.?\d*\b'), n))

        c = QTextCharFormat()
        c.setForeground(QColor(t['syn_comment']))
        self._rules.append((QRegularExpression(r'#[^\n]*'), c))

    def update_theme(self, t: dict):
        self._build_rules(t)
        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, fmt in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)


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

        # Ctrl+/ — QShortcut handles keyboard layout translation (works on AZERTY)
        sc = QShortcut(QKeySequence('Ctrl+/'), self)
        sc.setContext(Qt.WidgetShortcut)
        sc.activated.connect(self._toggle_comment)

    def set_theme(self, t: dict):
        self._theme = t
        self._apply_editor_style()
        self._highlighter.update_theme(t)
        self._line_area.update()

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.insertPlainText('    ')
        else:
            super().keyPressEvent(event)


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


# ── Editor section ────────────────────────────────────────────────────────────

class _EditorSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor = _CodeEditor()
        layout.addWidget(self.editor)

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

        self.set_theme(_THEMES['Dark'])

    def set_theme(self, t: dict):
        self.editor.set_theme(t)
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
