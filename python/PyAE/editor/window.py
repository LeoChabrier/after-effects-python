from __future__ import annotations

import sys
import traceback
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QSplitter, QToolBar, QFileDialog, QMessageBox,
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStatusBar, QComboBox,
)
from PySide6.QtGui import QKeySequence, QAction, QShortcut
from PySide6.QtCore import Qt, QSize

from .themes import _THEMES, make_icon, small_btn_style
from .code_editor import _CodeEditor
from .find_bar import _FindBar
from .log_panel import _LogPanel, _LogCapture
from .outliner import _Outliner
from .constants import SCRIPTS_DIR


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
        self._btn.setStyleSheet(small_btn_style(t))


class ScriptEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Python Script Editor')
        self.setWindowIcon(make_icon())
        self.resize(1100, 720)
        self._current_file: Path | None = None
        self._loading    = False
        self._pinned     = False
        self._theme_name = 'Dark'
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

        self._h_split  = QSplitter(Qt.Horizontal)
        self._outliner = _Outliner()
        self._outliner.itemDoubleClicked.connect(self._open_from_outliner)
        self._h_split.addWidget(self._outliner)

        self._v_split        = QSplitter(Qt.Vertical)
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

        self._pin_action = QAction('⊤', self)
        self._pin_action.setToolTip('Always on top')
        self._pin_action.setCheckable(True)
        self._pin_action.toggled.connect(self._toggle_pin)
        tb.addAction(self._pin_action)

        tb.addSeparator()

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

    # ── Theme ──────────────────────────────────────────────────────────────────

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

    # ── Pin ────────────────────────────────────────────────────────────────────

    def _toggle_pin(self, checked: bool):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()

    # ── Outliner toggle ────────────────────────────────────────────────────────

    def _toggle_outliner(self):
        if self._outliner.isVisible():
            self._outliner_width = self._h_split.sizes()[0]
            self._outliner.hide()
        else:
            self._outliner.show()
            w     = getattr(self, '_outliner_width', 180)
            total = sum(self._h_split.sizes())
            self._h_split.setSizes([w, total - w])

    # ── File ops ───────────────────────────────────────────────────────────────

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

    # ── Run ────────────────────────────────────────────────────────────────────

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

        self._editor._namespace = {k: v for k, v in namespace.items()
                                    if k not in ('__name__', '__builtins__', '__doc__')}
