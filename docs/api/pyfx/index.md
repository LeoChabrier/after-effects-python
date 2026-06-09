# PyFx

`PyFx` is a pybind11 Python extension compiled as part of the `PyAE.aex` plugin. It is importable only inside an After Effects process where the plugin is loaded.

## Suite model

The AE SDK organizes its API into **suites** — groups of related functions accessed through function-pointer tables. `PyFx` wraps each suite as a Python class:

```python
import PyFx

# Instantiate a suite
layer_suite = PyFx.LayerSuite()

# Use its methods
comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()
n     = layer_suite.GetCompNumLayers(comp)
layer = layer_suite.GetCompLayerByIndex(comp, 0)
print(layer_suite.GetLayerName(layer))
```

## Available suites

| Suite class | Purpose |
|-------------|---------|
| `PyFx.MemorySuite` | Allocate/free AE-managed memory |
| `PyFx.ProjSuite` | Open, save, iterate projects |
| `PyFx.ItemSuite` | Project items (footage, comps, folders) |
| `PyFx.CompSuite` | Composition creation and settings |
| `PyFx.LayerSuite` | Layer operations |
| `PyFx.StreamSuite` | Property access by stream type |
| `PyFx.DynamicStreamSuite` | Dynamic property tree navigation |
| `PyFx.KeyframeSuite` | Keyframe insert/delete/edit |
| `PyFx.EffectSuite` | Apply and manage effects |
| `PyFx.MaskSuite` | Mask operations |
| `PyFx.MaskOutlineSuite` | Mask path vertices |
| `PyFx.FootageSuite` | Footage import and interpretation |
| `PyFx.SoundDataSuite` | Audio data access |
| `PyFx.TextDocumentSuite` | Text layer content |
| `PyFx.TextLayerSuite` | Text outline paths |
| `PyFx.MarkerSuite` | Comp and layer markers |
| `PyFx.WorldSuite` | Image buffer creation and pixel access |
| `PyFx.RenderSuite` | Render frames on demand |
| `PyFx.RenderOptionsSuite` | Render settings |
| `PyFx.LayerRenderOptionsSuite` | Per-layer render settings |
| `PyFx.RenderQueueSuite` | Render queue management |
| `PyFx.RenderQueueItemSuite` | Individual render queue items |
| `PyFx.OutputModuleSuite` | Output module settings |
| `PyFx.CollectionSuite` | Generic item collections |
| `PyFx.CommandSuite` | Menu command registration |
| `PyFx.RegisterSuite` | Hook registration |
| `PyFx.UtilitySuite` | Undo groups, logging, error handling |

## Utility functions

```python
PyFx.ConvertUTF8ToUTF16(text)    # str  → UTF-16 bytes
PyFx.ConvertUTF16ToUTF8(data)    # bytes → str
PyFx.memHandleToString(handle)   # AE memory handle → str
```
