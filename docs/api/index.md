# API Reference

`after-effects-python` exposes two Python-facing APIs:

## PyFx

`PyFx` is the low-level C++ SDK binding. It mirrors the AE AEGP suite model directly — each suite is a Python class you instantiate to access its functions.

```python
import PyFx

# Every suite is instantiated the same way
suite = PyFx.LayerSuite()
```

| Module | Description |
|--------|-------------|
| [Project & Items](pyfx/project.md) | Open projects, iterate items, manage footage |
| [Compositions](pyfx/compositions.md) | Create and configure compositions |
| [Layers](pyfx/layers.md) | Add, query, and modify layers |
| [Properties & Keyframes](pyfx/properties.md) | Animate any layer property |
| [Effects & Masks](pyfx/effects.md) | Apply effects, edit mask paths |
| [Render](pyfx/render.md) | Render frames and manage the render queue |
| [Utilities](pyfx/utilities.md) | Undo groups, logging, world buffers |

## PyAE

`PyAE` is the Python package included with the plugin. Currently it provides the Script Editor UI.

| Module | Description |
|--------|-------------|
| [editor](editor.md) | Script Editor window — `PyAE.editor.main()` |

---

## Conventions

**Handles** — AE SDK objects are opaque handles. They are valid only within the current AE session.

**Time** — All time values use `A_Time` (a ratio: `value / scale`). Use `PyFx.UtilitySuite()` helpers to convert.

**Undo groups** — Any operation that modifies the project should be wrapped:

```python
util = PyFx.UtilitySuite()
util.startUndoGroup("my operation")
# ... your changes ...
util.endUndoGroup()
```
