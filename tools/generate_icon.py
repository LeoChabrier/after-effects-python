"""Generate assets/app.ico from the same QPainter recipe used in the app."""
import sys
import os
import struct

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QPixmap, QFont, QColor
from PySide6.QtCore import Qt, QRect, QRectF, QBuffer, QIODevice


def render_size(size: int) -> QPixmap:
    px = QPixmap(size, size)
    px.fill(Qt.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor('#252526'))
    m = size * 0.03
    r = size * 0.22
    p.drawRoundedRect(QRectF(m, m, size - 2 * m, size - 2 * m), r, r)
    p.setPen(QColor('#9999FF'))
    f = QFont('Arial', int(size * 0.34), QFont.Bold)
    p.setFont(f)
    p.drawText(QRect(0, 0, size, size), Qt.AlignCenter, 'Py')
    p.end()
    return px


def to_png(px: QPixmap) -> bytes:
    buf = QBuffer()
    buf.open(QIODevice.WriteOnly)
    px.save(buf, 'PNG')
    return bytes(buf.data())


def build_ico(sizes: list) -> bytes:
    images = [(s, to_png(render_size(s))) for s in sizes]

    header_size = 6
    dir_entry_size = 16
    data_offset = header_size + dir_entry_size * len(images)

    offsets = []
    off = data_offset
    for _, data in images:
        offsets.append(off)
        off += len(data)

    ico = struct.pack('<HHH', 0, 1, len(images))
    for i, (s, data) in enumerate(images):
        w = h = s if s < 256 else 0
        ico += struct.pack('<BBBBHHII', w, h, 0, 0, 1, 32, len(data), offsets[i])

    for _, data in images:
        ico += data

    return ico


if __name__ == '__main__':
    app = QApplication.instance() or QApplication(sys.argv)

    out = os.path.join(os.path.dirname(__file__), '..', 'assets', 'app.ico')
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)

    ico = build_ico([16, 24, 32, 48, 64, 128, 256])
    with open(out, 'wb') as f:
        f.write(ico)

    print(f'Generated assets/app.ico  ({len(ico):,} bytes)  sizes: 16 24 32 48 64 128 256')
