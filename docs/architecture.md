# Architecture

## The stack

```
┌─────────────────────────────────────────────────────┐
│  Adobe After Effects (Win64 process)                │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  AE SDK — C function pointer suites          │   │
│  │  (AEGP_SuiteHandler, PF_InData, etc.)       │   │
│  └────────────────┬────────────────────────────┘   │
│                   │ wraps                           │
│  ┌────────────────▼────────────────────────────┐   │
│  │  AETK — C++ static lib                       │   │
│  │  App, Project, Items, Layers, Suites…        │   │
│  └────────────────┬────────────────────────────┘   │
│                   │ pybind11                        │
│  ┌────────────────▼────────────────────────────┐   │
│  │  PyFx — Python extension module              │   │
│  │  import PyFx  →  PyFx.LayerSuite() etc.      │   │
│  └────────────────┬────────────────────────────┘   │
│                   │ imported by                     │
│  ┌────────────────▼────────────────────────────┐   │
│  │  PyAE — Python package                       │   │
│  │  Script Editor UI (PySide6 QMainWindow)      │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## How Python is embedded

The plugin is a Windows DLL (`.aex`) loaded by After Effects at startup via the `MediaCore` plug-ins directory. On first menu click:

1. `Py_Initialize()` is called on a **background thread** (never the AE main thread)
2. The plugin directory is added to `sys.path` so `import PyAE` resolves
3. `PyFx` is imported — this brings in the pybind11 bindings that wrap the AEGP suites
4. PySide6's `QApplication.exec` is monkey-patched to return 0 immediately (so script calls to `app.exec()` don't block)

## Threading model

```
AE main thread          Background thread (py_thread)
──────────────          ──────────────────────────────
onInit() → registers    startPythonThread() →
  menu command            Py_Initialize()
                          import PyFx
                          while running:
                            dequeue code string
                            py::exec(code)
onIdle() → TaskScheduler  processEvents()   ← keeps Qt windows alive
           .ExecuteTask()  sleep(10ms)
```

The C++ side queues Python code strings. The Python thread dequeues and `exec`s them. Qt windows stay responsive because `processEvents()` is called every 10ms in the loop.

## PyFx suite model

The AE SDK exposes functionality through **suites** — collections of function pointers. PyFx wraps each suite as a Python class. You instantiate a suite to get access to its functions:

```python
import PyFx

comp_suite  = PyFx.CompSuite()
layer_suite = PyFx.LayerSuite()

comp  = comp_suite.GetMostRecentlyUsedComp()
n     = layer_suite.GetCompNumLayers(comp)
```

All suite handles are live — they call directly into the AE SDK in the current AE session.

## References

- [After Effects Plug-in SDK Guide](https://ae-plugins.docsforadobe.dev/) — official Adobe documentation for the AEGP C API that both AETK and PyFx wrap

## AETK vs PyFx

| | AETK | PyFx |
|-|------|------|
| Language | C++ | Python (via pybind11) |
| Abstraction | Thin C++ wrapper | Direct suite bindings |
| Use from | C++ plugin code | Python scripts in AE |
| Object model | Classes (App, Layer…) | Suite instances |
