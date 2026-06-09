# Layers

## LayerSuite

All layer operations — querying, modifying, adding, and removing layers.

```python
layer_suite = PyFx.LayerSuite()
```

### Accessing layers

```python
comp        = PyFx.CompSuite().GetMostRecentlyUsedComp()
layer_suite = PyFx.LayerSuite()

n           = layer_suite.GetCompNumLayers(comp)
first_layer = layer_suite.GetCompLayerByIndex(comp, 0)
active      = layer_suite.GetActiveLayer()
```

| Method | Returns | Description |
|--------|---------|-------------|
| `GetCompNumLayers(comp)` | `int` | Number of layers in composition |
| `GetCompLayerByIndex(comp, index)` | `LayerH` | Get layer by index (0 = top) |
| `GetActiveLayer()` | `LayerH` | Currently selected layer |
| `GetLayerFromLayerID(comp, id)` | `LayerH` | Get layer by persistent ID |

### Layer properties

| Method | Returns | Description |
|--------|---------|-------------|
| `GetLayerName(layer)` | `str` | Layer name |
| `SetLayerName(layer, name)` | — | Rename layer |
| `GetLayerIndex(layer)` | `int` | Stack position (0 = top) |
| `GetLayerID(layer)` | `int` | Unique persistent ID |
| `GetLayerObjectType(layer)` | `LayerType` | AV, camera, light, text |
| `IsLayer3D(layer)` | `bool` | 3D layer flag |
| `GetLayerParentComp(layer)` | `CompH` | Containing composition |
| `GetLayerSourceItem(layer)` | `ItemH` | Source footage or pre-comp |
| `GetLayerParent(layer)` | `LayerH` | Parent layer (for parenting) |
| `SetLayerParent(layer, parent)` | — | Set parent layer |
| `GetLayerLabel(layer)` | `int` | Label color index |
| `SetLayerLabel(layer, label)` | — | Set label color |

### Visibility & audio

| Method | Returns | Description |
|--------|---------|-------------|
| `GetLayerFlags(layer)` | `int` | Packed flags (video, audio, solo, etc.) |
| `SetLayerFlag(layer, flag, value)` | — | Toggle a single flag |
| `IsLayerVideoReallyOn(layer)` | `bool` | Effective video state |
| `IsLayerAudioReallyOn(layer)` | `bool` | Effective audio state |

### Timing

| Method | Returns | Description |
|--------|---------|-------------|
| `GetLayerInPoint(layer, timeMode)` | `A_Time` | Layer in-point |
| `GetLayerDuration(layer, timeMode)` | `A_Time` | Layer duration |
| `SetLayerInPointAndDuration(layer, mode, in, dur)` | — | Trim layer |
| `GetLayerOffset(layer)` | `A_Time` | Layer start offset in comp time |
| `SetLayerOffset(layer, offset)` | — | Move layer in time |
| `GetLayerStretch(layer)` | `float` | Time-stretch ratio |
| `SetLayerStretch(layer, stretch)` | — | Set time stretch |
| `ConvertCompToLayerTime(layer, compTime)` | `A_Time` | Convert comp time → layer time |
| `ConvertLayerToCompTime(layer, layerTime)` | `A_Time` | Convert layer time → comp time |

### Adding / removing / reordering

| Method | Returns | Description |
|--------|---------|-------------|
| `IsAddLayerValid(item, comp)` | `bool` | Check if item can be added as layer |
| `AddLayer(item, comp)` | `LayerH` | Add an item as a new layer |
| `DuplicateLayer(layer)` | `LayerH` | Duplicate a layer |
| `DeleteLayer(layer)` | — | Remove layer from composition |
| `ReorderLayer(layer, newIndex)` | — | Move layer in stack |

### Blend modes & track mattes

| Method | Returns | Description |
|--------|---------|-------------|
| `GetLayerTransferMode(layer)` | `TransferMode` | Blend mode |
| `SetLayerTransferMode(layer, flags, matte)` | — | Set blend mode and track matte |
| `GetTrackMatteLayer(layer)` | `LayerH` | Track matte source |
| `SetTrackMatte(layer, matteLayer, type)` | — | Apply track matte |
| `RemoveTrackMatte(layer)` | — | Remove track matte |

### Spatial transforms

| Method | Returns | Description |
|--------|---------|-------------|
| `GetLayerToWorldXform(layer, time)` | `matrix` | 4x4 world transform at comp time |
| `GetLayerMaskedBounds(layer, mode, time)` | `rect` | Visible bounds |

### Example: rename all layers

```python
import PyFx

util  = PyFx.UtilitySuite()
ls    = PyFx.LayerSuite()
comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()

util.startUndoGroup("rename layers")

for i in range(ls.GetCompNumLayers(comp)):
    layer = ls.GetCompLayerByIndex(comp, i)
    ls.SetLayerName(layer, f"Layer_{i+1:03d}")

util.endUndoGroup()
print("Done.")
```

### Example: add a null layer

```python
import PyFx

util  = PyFx.UtilitySuite()
comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()
dur   = PyFx.CompSuite().GetCompWorkAreaDuration(comp)

util.startUndoGroup("add null")
null  = PyFx.CompSuite().CreateNullInComp(comp, "Control", dur)
util.endUndoGroup()
```
