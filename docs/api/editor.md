# Script Editor

The `PyAE.editor` module provides the Script Editor window. It is loaded by the plugin when the user clicks **Window > Python Script Editor**.

## Entry point

```python
import PyAE.editor
PyAE.editor.main()
```

If the window is already open, `main()` brings it to the foreground instead of creating a second instance.

## `ScriptEditorWindow`

::: PyAE.editor.ScriptEditorWindow

---

## Constants

```python
SCRIPTS_DIR: Path
```

Default scripts directory: `%APPDATA%\after-effects-python\scripts\`

Scripts saved here appear automatically in the outliner.

---

## Internal classes

These are not part of the public API but document the editor's components.

### `_CodeEditor`

`QPlainTextEdit` subclass with:

- Python syntax highlighting (`_PythonHighlighter`)
- Line number gutter (`_LineArea`)
- Tab key inserts 4 spaces
- `Ctrl+/` toggles line comments on selection

### `_LogPanel`

`QWidget` wrapping a read-only `QPlainTextEdit` with a **Clear log** button. Each line is prefixed `[HH:MM:SS]`.

### `_Outliner`

`QTreeWidget` browsing `SCRIPTS_DIR`. Context menu: New Script, New Folder, Rename, Delete.

### `_LogCapture`

`io.RawIOBase` subclass that redirects `sys.stdout` and `sys.stderr` to the log panel during script execution.
