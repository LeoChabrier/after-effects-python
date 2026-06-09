# Script Editor

Open from **Window > Python Script Editor**.

## Layout

```
┌──────────┬──────────────────────────────────────┐
│          │  Log panel (stdout / stderr)          │
│ Outliner │──────────────────────────────────────│
│          │  Code editor                          │
│          │──────────────────────────────────────│
│          │                         Clear editor  │
└──────────┴──────────────────────────────────────┘
                                  Clear log ↗
```

- **Outliner** (left, collapsible) — file browser for `%APPDATA%\after-effects-python\scripts\`
- **Log panel** (top right) — timestamped output from `print()`, exceptions, and AE errors
- **Code editor** (bottom right) — full Python editor with syntax highlighting and line numbers

## Toolbar

| Button | Shortcut | Action |
|--------|----------|--------|
| ≡ | — | Toggle outliner |
| New | Ctrl+N | New script |
| Open | Ctrl+O | Open file dialog |
| Save | Ctrl+S | Save current script |
| ▶ Run | Ctrl+Enter | Execute the script |

## Keyboard shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Run script |
| `Ctrl+N` | New script |
| `Ctrl+O` | Open script |
| `Ctrl+S` | Save script |
| `Tab` | Insert 4 spaces |

## Script execution

Scripts run in an isolated namespace with `PyFx` pre-imported (when inside AE). The script's `__name__` is set to `'__main__'` so `if __name__ == '__main__':` guards work as expected.

```python
import PyFx

comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()
layer = PyFx.LayerSuite().GetCompLayerByIndex(comp, 0)
name  = PyFx.LayerSuite().GetLayerName(layer)
print(f"First layer: {name}")
```

Exceptions are caught and printed to the log panel with a full traceback.

## Log panel

Every line is prefixed with a `[HH:MM:SS]` timestamp.

```
[14:23:01] First layer: Background
[14:25:42] Traceback (most recent call last):
[14:25:42]   File "<editor>", line 3, in <module>
[14:25:42] AttributeError: 'NoneType' object has no attribute 'GetLayerName'
```

Use **Clear log** to clear the output between runs. Opening a script from the outliner also clears the log automatically.

## Managing scripts

### Creating a script

Click **New** in the toolbar, or right-click in the outliner and choose **New Script**. New scripts are pre-populated with `import PyFx`.

### Opening a script

Double-click a script in the outliner to open it. If the current editor has unsaved changes, you will be prompted to discard them.

### Saving a script

**Ctrl+S** saves to the current file. If the script hasn't been saved yet, a file dialog opens. The title bar shows an asterisk `*` when there are unsaved changes.

### Organizing scripts

Right-click in the outliner for context menu options:

- **New Script** — creates a `.py` file in the scripts directory
- **New Folder** — creates a subfolder
- **Rename** — renames the selected file
- **Delete** — removes the selected file (with confirmation)

## Tips

!!! note "Undo groups"
    Wrap modifications in a `startUndoGroup` / `endUndoGroup` call so your script can be undone as a single action in AE's edit history.

```python
import PyFx

util = PyFx.UtilitySuite()
util.startUndoGroup("rename layers")

layer_suite = PyFx.LayerSuite()
comp = PyFx.CompSuite().GetMostRecentlyUsedComp()
n = layer_suite.GetCompNumLayers(comp)
for i in range(n):
    layer = layer_suite.GetCompLayerByIndex(comp, i)
    layer_suite.SetLayerName(layer, f"Layer_{i+1:03d}")

util.endUndoGroup()
print("Done.")
```
