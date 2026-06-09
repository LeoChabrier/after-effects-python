from pathlib import Path

from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QInputDialog, QMessageBox
from PySide6.QtCore import Qt

from .themes import _THEMES
from .constants import SCRIPTS_DIR


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
