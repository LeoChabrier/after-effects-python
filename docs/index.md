# after-effects-python

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/LeoChabrier/after-effects-python/blob/main/LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)
[![After Effects](https://img.shields.io/badge/After%20Effects-2025+-9999FF.svg)](https://www.adobe.com/products/aftereffects.html)
[![C++17](https://img.shields.io/badge/C++-17-00599C.svg)](https://isocpp.org/)

**Python scripting inside Adobe After Effects** — a live AEGP plugin that embeds a Python interpreter in the AE process, exposes the AEGP SDK as a Python module (`PyFx`), and provides a full Script Editor UI.

---

## What is this?

After Effects has no equivalent to Maya's Script Editor. There is no way to write Python, execute it against a live AE session, and see what happens — at least not without building it yourself.

`after-effects-python` changes that. It runs **inside** AE and gives you:

- A **Script Editor** (Window > Python Script Editor) with syntax highlighting, line numbers, log panel, and a file browser
- The **`PyFx` module** — direct Python bindings for the AEGP C++ SDK
- **stdout/stderr capture** so print statements and errors show up in the log panel

---

## Quick example

```python
import PyFx

# Get the active composition
app   = PyFx.App()
proj  = app.getProject()
comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()

# Print all layer names
layer_suite = PyFx.LayerSuite()
n = layer_suite.GetCompNumLayers(comp)
for i in range(n):
    layer = layer_suite.GetCompLayerByIndex(comp, i)
    name  = layer_suite.GetLayerName(layer)
    print(name)
```

---

## Features

| Feature | Status |
|---------|--------|
| Python interpreter embedded in AE | ✅ |
| PySide6 UI running inside AE | ✅ |
| Script Editor with syntax highlighting | ✅ |
| Line numbers & collapsible outliner | ✅ |
| stdout/stderr capture with timestamps | ✅ |
| Script file browser (outliner) | ✅ |
| Window menu command (`Window > Python Script Editor`) | 🔜 |
| PyFx auto-completion stubs (.pyi) | 🔜 |
| AE action logging | 🔜 |

---

## Why not CEP / ExtendScript?

CEP is deprecated. ExtendScript doesn't give you Python, numpy, or access to the rest of your pipeline tooling. `after-effects-python` uses the native AEGP C++ plugin API and embeds CPython directly — same approach as Maya's Python integration.

---

[Get Started →](getting-started.md){ .md-button .md-button--primary }
[API Reference →](api/index.md){ .md-button }
