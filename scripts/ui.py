from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QSplitter, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextCursor
import sys
import os
import traceback
import json
import pprint

window = None

class ScriptEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("After Effects Script Editor")
        self.setGeometry(100, 100, 1000, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("After Effects Script Editor")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Splitter for editor and console
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Editor section
        editor_group = QGroupBox("Script Editor")
        editor_layout = QVBoxLayout()

        self.script_editor = QTextEdit()
        self.script_editor.setPlaceholderText("# Écrivez votre script Python ici...\n# Exemple:\nimport os\nprint('Environment:', os.environ)")

        # Set monospace font for editor
        editor_font = QFont("Consolas", 10)
        editor_font.setStyleHint(QFont.StyleHint.Monospace)
        self.script_editor.setFont(editor_font)
        self.script_editor.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #a9b7c6;
                border: 1px solid #555;
                padding: 5px;
            }
        """)

        editor_layout.addWidget(self.script_editor)
        editor_group.setLayout(editor_layout)
        splitter.addWidget(editor_group)

        # Console section
        console_group = QGroupBox("Console de sortie")
        console_layout = QVBoxLayout()

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setPlaceholderText("Les résultats d'exécution apparaîtront ici...")
        self.console_output.setAcceptRichText(True)  # Enable HTML formatting

        # Set monospace font for console
        console_font = QFont("Consolas", 9)
        console_font.setStyleHint(QFont.StyleHint.Monospace)
        self.console_output.setFont(console_font)
        self.console_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #cccccc;
                border: 1px solid #555;
                padding: 5px;
            }
        """)

        console_layout.addWidget(self.console_output)
        console_group.setLayout(console_layout)
        splitter.addWidget(console_group)

        # Set splitter proportions (60% editor, 40% console)
        splitter.setSizes([400, 300])
        main_layout.addWidget(splitter)

        # Buttons
        button_layout = QHBoxLayout()

        self.run_btn = QPushButton("▶ Exécuter (Ctrl+Enter)")
        self.run_btn.clicked.connect(self.on_run_script)
        self.run_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.run_btn)

        self.clear_console_btn = QPushButton("🗑 Effacer Console")
        self.clear_console_btn.clicked.connect(self.on_clear_console)
        self.clear_console_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        button_layout.addWidget(self.clear_console_btn)

        self.clear_all_btn = QPushButton("⟲ Tout Effacer")
        self.clear_all_btn.clicked.connect(self.on_clear_all)
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        button_layout.addWidget(self.clear_all_btn)

        self.env_btn = QPushButton("🌍 Afficher Environnement")
        self.env_btn.clicked.connect(self.on_show_environment)
        self.env_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        button_layout.addWidget(self.env_btn)

        main_layout.addLayout(button_layout)

    def on_run_script(self):
        """Execute the script in the editor"""
        script = self.script_editor.toPlainText()

        if not script.strip():
            self.print_warning("Aucun script à exécuter")
            return

        self.print_separator()
        self.print_info("▶ Exécution du script...")
        self.print_separator()

        # Capture stdout and create custom print
        from io import StringIO
        import builtins

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_print = builtins.print

        redirected_output = StringIO()
        redirected_error = StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_error

        # Create custom print function
        def custom_print(*args, **kwargs):
            # Format the output
            output_parts = []
            for arg in args:
                if isinstance(arg, (dict, list, tuple, set)):
                    formatted = pprint.pformat(arg, width=80, compact=False)
                    output_parts.append(formatted)
                else:
                    output_parts.append(str(arg))

            sep = kwargs.get('sep', ' ')
            end = kwargs.get('end', '\n')
            output = sep.join(output_parts) + end

            # Write to redirected output
            redirected_output.write(output)

        builtins.print = custom_print

        try:
            # Execute the script
            exec(script, globals())

            # Get output
            output = redirected_output.getvalue()
            error = redirected_error.getvalue()

            if output:
                self.print_output(output)

            if error:
                self.print_error(error)

            if not output and not error:
                self.print_success("Script exécuté sans sortie")
            else:
                self.print_success("Script exécuté avec succès")

        except Exception as e:
            error_msg = traceback.format_exc()
            self.print_error(f"Erreur d'exécution:\n{error_msg}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            builtins.print = old_print

        self.append_html("<br>")

    def append_html(self, html):
        """Append HTML content to console"""
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertHtml(html)
        self.console_output.setTextCursor(cursor)
        # Auto-scroll
        self.console_output.verticalScrollBar().setValue(
            self.console_output.verticalScrollBar().maximum()
        )

    def print_separator(self):
        """Print a separator line"""
        self.append_html('<hr style="border: 1px solid #444; margin: 5px 0;">')

    def print_info(self, text):
        """Print info message"""
        self.append_html(f'<div style="color: #58a6ff; margin: 2px 0;">ℹ {text}</div>')

    def print_success(self, text):
        """Print success message"""
        self.append_html(f'<div style="color: #3fb950; margin: 2px 0; font-weight: bold;">✓ {text}</div>')

    def print_warning(self, text):
        """Print warning message"""
        self.append_html(f'<div style="color: #d29922; margin: 2px 0;">⚠ {text}</div>')

    def print_error(self, text):
        """Print error message"""
        html_text = text.replace('\n', '<br>').replace(' ', '&nbsp;')
        self.append_html(f'<div style="color: #f85149; margin: 2px 0; font-family: Consolas, monospace; font-size: 9pt;">❌ {html_text}</div>')

    def print_output(self, text):
        """Print standard output"""
        # Replace newlines and spaces for proper HTML formatting
        html_text = text.replace('\n', '<br>').replace(' ', '&nbsp;')
        self.append_html(f'<div style="color: #c9d1d9; margin: 2px 0; font-family: Consolas, monospace; font-size: 9pt;">{html_text}</div>')

    def print_dict(self, title, data):
        """Pretty print a dictionary"""
        self.append_html(f'<div style="color: #79c0ff; margin: 5px 0; font-weight: bold;">📋 {title}</div>')
        formatted = pprint.pformat(data, width=80, compact=False)
        html_text = formatted.replace('\n', '<br>').replace(' ', '&nbsp;')
        self.append_html(f'<div style="color: #c9d1d9; margin-left: 20px; font-family: Consolas, monospace; font-size: 9pt;">{html_text}</div>')

    def on_clear_console(self):
        """Clear the console output"""
        self.console_output.clear()
        self.print_info("Console effacée")
        self.append_html("<br>")

    def on_clear_all(self):
        """Clear both editor and console"""
        self.script_editor.clear()
        self.console_output.clear()
        self.print_info("Éditeur et console effacés")
        self.append_html("<br>")

    def on_show_environment(self):
        """Display environment information"""
        self.print_separator()
        self.append_html('<div style="color: #79c0ff; font-size: 12pt; font-weight: bold; margin: 5px 0;">🌍 INFORMATIONS SUR L\'ENVIRONNEMENT</div>')
        self.print_separator()

        # Python info
        self.append_html('<div style="color: #79c0ff; font-weight: bold; margin: 10px 0 5px 0;">🐍 Python</div>')
        self.append_html(f'<div style="color: #c9d1d9; margin-left: 20px;">Version: <span style="color: #a5d6ff;">{sys.version.split()[0]}</span></div>')
        self.append_html(f'<div style="color: #c9d1d9; margin-left: 20px;">Exécutable: <span style="color: #a5d6ff;">{sys.executable}</span></div>')
        self.append_html(f'<div style="color: #c9d1d9; margin-left: 20px;">Plateforme: <span style="color: #a5d6ff;">{sys.platform}</span></div>')

        # Environment variables (filtered for readability)
        self.append_html('<div style="color: #79c0ff; font-weight: bold; margin: 10px 0 5px 0;">🔧 Variables d\'environnement clés</div>')

        important_vars = ['C14_PROJECT_NAME', 'C14_SHOT_NAME', 'C14_TASK_TASK_TYPE_NAME',
                         'PYTHONPATH', 'PATH', 'USERNAME', 'COMPUTERNAME',
                         'REZ_USED_RESOLVE', 'C14_WORKFILE_PATH']

        for key in important_vars:
            value = os.environ.get(key)
            if value:
                # Truncate long values
                display_value = value if len(value) < 100 else value[:97] + "..."
                self.append_html(f'<div style="color: #8b949e; margin-left: 20px; font-size: 8pt;"><span style="color: #ffa657;">{key}</span> = <span style="color: #a5d6ff;">{display_value}</span></div>')

        self.append_html('<div style="color: #8b949e; margin: 10px 0 5px 20px; font-style: italic; font-size: 8pt;">💡 Utilisez os.environ pour voir toutes les variables</div>')
        self.print_separator()
        self.append_html("<br>")


def main():
    global window
    app = QApplication(sys.argv)
    window = ScriptEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
