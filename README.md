# after-effects-python

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)
[![After Effects](https://img.shields.io/badge/After%20Effects-2025+-9999FF.svg)](https://www.adobe.com/fr/products/aftereffects.html)
[![C++](https://img.shields.io/badge/C++-17-00599C.svg)](https://isocpp.org/)

Python scripting inside Adobe After Effects — a live AEGP plugin with SDK bindings and a PySide6 script editor.

> **Status:** Early development. The plugin loads and runs Python scripts inside AE. The script editor UI is in progress. Contributions welcome.

---

## Why this exists

After Effects has no equivalent to Maya's Script Editor. There is no way to write Python, execute it against a live AE session, and see what happens — at least not without building it yourself.

There is almost no open-source work on AEGP C++ plugins that embed Python. This project exists to change that and serve as a common foundation for AE TDs who keep hitting the same wall.

This is different from [py-aep](https://github.com/forticheprod/py-aep) (Fortiche Production), which parses `.aep` files headlessly without a running AE instance. `after-effects-python` runs **inside** AE and has full access to the live session via the AEGP SDK.

---

## Architecture

```
AE SDK (Adobe C API)       ← raw function pointers, suites
        ↓
AETK (C++ static lib)      ← modern C++ wrapper — App, Project, Items, Layers...
        ↓
PyFx (pybind11 module)     ← Python bindings for AETK, imported inside AE
        ↓
ae (Python package)        ← high-level API + script editor + logging  [WIP]
```

The plugin is a `.aex` file (Windows DLL) loaded by AE at startup. It bootstraps a Python interpreter inside the AE process, then exposes the AEGP SDK to Python via `PyFx`.

---

## Requirements

- Windows 10/11 x64
- Adobe After Effects 2025+
- Visual Studio 2022 (v143 toolset)
- Python 3.11 x64 — installed at `C:\Program Files\Python311`
- [vcpkg](https://github.com/microsoft/vcpkg) — installed at `C:\vcpkg`, with `VCPKG_ROOT=C:\vcpkg` environment variable set
- Dependencies via vcpkg (use the `x64-windows-static-md` triplet — static libs with dynamic CRT, required for MSVC 17.3+ compatibility):

```
cd C:\vcpkg
.\vcpkg.exe install icu:x64-windows-static-md pybind11:x64-windows-static-md stb:x64-windows-static-md
```

---

## Build

```
git clone https://github.com/<you>/after-effects-python
cd after-effects-python
```

Open `after-effects-python.sln` in Visual Studio 2022.

Build **Release|x64**. This will:
1. Compile `AETK` as a static library
2. Compile `PyAE` as a `.aex` plugin, output to `C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\`

> To output to a different directory, set the `AEPluginDir` environment variable before building.

---

## Usage

Open the script editor from **Window > Python Script Editor** in After Effects.

Scripts are saved to `%APPDATA%\after-effects-python\scripts\` by default and are browsable from the outliner panel on the left.

Inside a script, import `PyFx` to interact with the live AE session:

```python
# Third-Party
import PyFx


proj_suite  = PyFx.ProjSuite()
item_suite  = PyFx.ItemSuite()
comp_suite  = PyFx.CompSuite()
layer_suite = PyFx.LayerSuite()

project = proj_suite.GetProjectByIndex(0)
print(f"Project : {proj_suite.GetProjectPath(project)}")


item = item_suite.GetFirstProjItem(project)
first_comp = None

while item is not None:
    try:
        name = item_suite.GetItemName(item)
        kind = str(item_suite.GetItemType(item))
        print(f"  {kind:<20} {name}")
        if first_comp is None and 'COMP' in kind.upper():
            first_comp = item
        item = item_suite.GetNextProjItem(project, item)
    except Exception:
        break

if first_comp is not None:
    comp_name = item_suite.GetItemName(first_comp)
    comp      = comp_suite.GetCompFromItem(first_comp)
    n_layers  = layer_suite.GetCompNumLayers(comp)
    print(f"\nComp '{comp_name}' — {n_layers} layer(s)")
    for i in range(n_layers):
        layer = layer_suite.GetCompLayerByIndex(comp, i)
        name  = layer_suite.GetLayerName(layer)
        kind  = str(layer_suite.GetLayerObjectType(layer))
        print(f"  [{i}] {kind:<16} {name}")
else:
    print("\nNo comp found in current project.")

```

Press **Ctrl+Enter** (or the ▶ Run button) to execute. stdout and stderr are captured to the log panel.

---

## Roadmap

- [x] Python interpreter embedded in AE process
- [x] PySide6 UI running inside AE (no separate window manager needed)
- [x] Script editor with syntax highlighting and line numbers
- [x] Output panel (stdout/stderr capture with timestamps)
- [x] Script file browser (outliner with new/rename/delete)
- [ ] Wire up `Window > Python Script Editor` menu command in C++
- [ ] PyFx auto-completion (.pyi stubs)
- [ ] AE action logging (command hooks + project state polling)
- [ ] `ae` high-level Python package on top of PyFx

---

## Project structure

```
after-effects-python/
├── AETK/              C++ AEGP wrapper (static lib sources)
├── Headers/           AE SDK headers
├── Resources/         PiPLtool.exe
├── Util/              AEGP_SuiteHandler, helpers
├── src/               Plugin entry point (PyShiftAE.cpp, PiPL)
├── python/            PyFx package and ae module
├── scripts/           Example scripts
├── AETK.vcxproj       Static lib project
├── PyAE.vcxproj       Plugin project
└── after-effects-python.sln   Visual Studio solution
```

---

## Contributing

This project is early and the hardest part (getting Python running inside AE) is done. If you are an AE TD who has been looking for this, contributions are very welcome — especially:

- PyFx bindings coverage (more AEGP suites)
- The `ae` high-level Python API
- macOS support (requires a separate build system)
- Documentation of AE SDK quirks

---

## Acknowledgements

Based on [PyShiftAE](https://github.com/Trentonom0r3/PyShiftAE) by Trentonom0r3 (accounts no longer active).
