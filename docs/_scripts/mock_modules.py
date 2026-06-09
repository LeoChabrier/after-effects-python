"""
Mock modules so mkdocstrings can import PyAE without needing
a live After Effects process (PyFx) or a display server (PySide6).
"""
import sys
from unittest.mock import MagicMock


class _Mock(MagicMock):
    @classmethod
    def __get_validators__(cls):
        yield cls

    def __class_getitem__(cls, item):
        return cls


MOCK_MODULES = [
    "PyFx",
    "PySide6",
    "PySide6.QtWidgets",
    "PySide6.QtGui",
    "PySide6.QtCore",
]

for mod in MOCK_MODULES:
    sys.modules[mod] = _Mock()
