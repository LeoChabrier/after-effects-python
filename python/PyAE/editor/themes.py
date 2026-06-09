from PySide6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor
from PySide6.QtCore import Qt, QRect, QRectF

_THEMES = {
    'Dark': {
        'editor_bg': '#1E1E1E', 'editor_fg': '#D4D4D4',
        'log_bg':    '#1E1E1E', 'log_fg':    '#9CDCFE',
        'line_bg':   '#252526', 'line_fg':   '#858585',
        'panel_bg':  '#2D2D2D', 'toolbar_bg':'#3C3C3C',
        'splitter':  '#444444', 'statusbar': '#007ACC',
        'outliner_bg':'#252526','outliner_fg':'#CCCCCC','outliner_sel':'#094771',
        'btn_bg':    '#3C3C3C', 'btn_hover': '#505050', 'btn_fg': '#CCCCCC',
        'syn_keyword':  '#C586C0', 'syn_builtin': '#DCDCAA',
        'syn_string':   '#CE9178', 'syn_number':  '#B5CEA8',
        'syn_comment':  '#6A9955',
        'syn_def_name': '#DCDCAA', 'syn_cls_name': '#4EC9B0',
        'syn_self':     '#9CDCFE', 'syn_deco':     '#C586C0',
        'syn_const':    '#9CDCFE', 'syn_magic':    '#DCDCAA',
        'syn_unused':   '#4A4A66',
    },
    'Light': {
        'editor_bg': '#FFFFFF', 'editor_fg': '#1E1E1E',
        'log_bg':    '#F8F8F8', 'log_fg':    '#0070C1',
        'line_bg':   '#F3F3F3', 'line_fg':   '#AAAAAA',
        'panel_bg':  '#E8E8E8', 'toolbar_bg':'#F0F0F0',
        'splitter':  '#CCCCCC', 'statusbar': '#0078D4',
        'outliner_bg':'#F3F3F3','outliner_fg':'#1E1E1E','outliner_sel':'#CCE4FF',
        'btn_bg':    '#E0E0E0', 'btn_hover': '#C8C8C8', 'btn_fg': '#1E1E1E',
        'syn_keyword':  '#AF00DB', 'syn_builtin': '#795E26',
        'syn_string':   '#A31515', 'syn_number':  '#098658',
        'syn_comment':  '#008000',
        'syn_def_name': '#795E26', 'syn_cls_name': '#267F99',
        'syn_self':     '#0000FF', 'syn_deco':     '#AF00DB',
        'syn_const':    '#0070C1', 'syn_magic':    '#795E26',
        'syn_unused':   '#B0B0B0',
    },
    'Aura': {
        'editor_bg': '#15002B', 'editor_fg': '#EDECEE',
        'log_bg':    '#15002B', 'log_fg':    '#A277FF',
        'line_bg':   '#1A0035', 'line_fg':   '#6644AA',
        'panel_bg':  '#1E0040', 'toolbar_bg':'#200045',
        'splitter':  '#3D1A6E', 'statusbar': '#9999FF',
        'outliner_bg':'#1A0035','outliner_fg':'#EDECEE','outliner_sel':'#3D1A6E',
        'btn_bg':    '#2A0055', 'btn_hover': '#3D1A6E', 'btn_fg': '#EDECEE',
        'syn_keyword':  '#FF79C6', 'syn_builtin': '#FFD580',
        'syn_string':   '#F1FA8C', 'syn_number':  '#BD93F9',
        'syn_comment':  '#7970A9',
        'syn_def_name': '#FFD580', 'syn_cls_name': '#80FFEA',
        'syn_self':     '#A277FF', 'syn_deco':     '#FF79C6',
        'syn_const':    '#A277FF', 'syn_magic':    '#FFD580',
        'syn_unused':   '#3A2A4A',
    },
}


def make_icon() -> QIcon:
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


def small_btn_style(t: dict) -> str:
    return (
        f"QPushButton {{ background:{t['btn_bg']}; color:{t['btn_fg']}; "
        f"border:none; border-radius:3px; padding:0 8px; font-size:11px; }}"
        f"QPushButton:hover {{ background:{t['btn_hover']}; }}"
    )
