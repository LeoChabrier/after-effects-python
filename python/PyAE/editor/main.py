import sys

from PySide6.QtWidgets import QApplication

from .window import ScriptEditorWindow

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
