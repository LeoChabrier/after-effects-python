# Getting Started

## Requirements

| Requirement | Version |
|------------|---------|
| Windows | 10 / 11 x64 |
| Adobe After Effects | 2025+ |
| Visual Studio | 2022 (v143 toolset) |
| Python | 3.11 x64 |
| vcpkg | latest |

Python must be installed at `C:\Program Files\Python311`. The `VCPKG_ROOT` environment variable must point to your vcpkg installation (default: `C:\vcpkg`).

---

## 1. Install vcpkg dependencies

```bat
cd C:\vcpkg
.\vcpkg.exe install icu:x64-windows-static-md pybind11:x64-windows-static-md stb:x64-windows-static-md
```

These use the `x64-windows-static-md` triplet — static libraries with dynamic CRT (`/MD`), required for compatibility with MSVC 17.3+.

---

## 2. Build the plugin

```bat
git clone https://github.com/LeoChabrier/after-effects-python
```

Open `after-effects-python.sln` in Visual Studio 2022 and build **Release|x64**.

This will:

1. Compile `AETK` as a static library
2. Compile `PyAE.aex` and copy it to `C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\`
3. Copy the `PyAE` Python package next to the `.aex`

!!! note "Custom output directory"
    Set the `AEPluginDir` environment variable before building to change the output path.

---

## 3. First run

1. Launch After Effects
2. Open **Window > Python Script Editor**
3. Type a script and press **Ctrl+Enter** (or click ▶ Run)

```python
import PyFx

app  = PyFx.App()
proj = app.getProject()
name = PyFx.ProjSuite().GetProjectName(proj)
print(f"Project: {name}")
```

Output appears in the log panel with a `[HH:MM:SS]` timestamp.

---

## Scripts directory

Scripts are saved to:

```
%APPDATA%\after-effects-python\scripts\
```

Use the outliner panel on the left to browse, create, rename, and delete scripts. Double-click a script to open it in the editor.

---

## Troubleshooting

The plugin writes a log file on startup:

```
%APPDATA%\after-effects-python\plugin.log
```

Check this file if the menu item doesn't appear or the editor fails to open.

### Common issues

| Symptom | Likely cause |
|---------|-------------|
| Menu item missing | Plugin not in `MediaCore\` or AE restarted without loading | 
| `PyFx import failed` in log | Python 3.11 not at `C:\Program Files\Python311` |
| Editor opens but crashes on Run | PySide6 not installed in Python 3.11 |

Install PySide6 if missing:

```bat
"C:\Program Files\Python311\python.exe" -m pip install PySide6
```
