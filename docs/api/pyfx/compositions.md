# Compositions

## CompSuite

Creates and configures compositions.

```python
comp_suite = PyFx.CompSuite()
```

### Getting the active comp

```python
comp = PyFx.CompSuite().GetMostRecentlyUsedComp()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GetMostRecentlyUsedComp()` | `CompH` | The active/focused composition |
| `GetCompFromItem(item)` | `CompH` | Get comp handle from a project item |
| `GetItemFromComp(comp)` | `ItemH` | Get project item from comp handle |
| `CreateComp(folder, name, w, h, par, dur, fps)` | `CompH` | Create a new composition |
| `DuplicateComp(comp)` | `CompH` | Duplicate a composition |
| `GetCompFramerate(comp)` | `float` | Frame rate (fps) |
| `SetCompFrameRate(comp, fps)` | — | Set frame rate |
| `GetCompBGColor(comp)` | `color` | Background color |
| `SetCompBGColor(comp, color)` | — | Set background color |
| `GetCompWorkAreaStart(comp)` | `A_Time` | Work area start time |
| `GetCompWorkAreaDuration(comp)` | `A_Time` | Work area duration |
| `SetCompWorkAreaStartAndDuration(comp, start, dur)` | — | Set work area |
| `GetCompDisplayStartTime(comp)` | `A_Time` | Display start time (offset) |
| `SetCompDisplayStartTime(comp, time)` | — | Set display start time |
| `SetCompDuration(comp, dur)` | — | Set composition duration |
| `SetCompDimensions(comp, w, h)` | — | Resize composition |
| `SetCompPixelAspectRatio(comp, par)` | — | Set PAR |
| `GetCompFrameDuration(comp)` | `A_Time` | Duration of one frame |
| `GetCompDownsampleFactor(comp)` | `(int,int)` | Preview quality factor |
| `SetCompDownsampleFactor(comp, factor)` | — | Set preview quality |
| `GetCompFlags(comp)` | `int` | Composition flags |
| `GetCompMotionBlurAdaptiveSampleLimit(comp)` | `int` | Motion blur max samples |
| `SetCompMotionBlurAdaptiveSampleLimit(comp, n)` | — | Set motion blur max samples |

### Creating layers inside a comp

| Method | Description |
|--------|-------------|
| `CreateSolidInComp(comp, name, w, h, color, dur)` | Add solid layer |
| `CreateCameraInComp(comp, name, center)` | Add camera |
| `CreateLightInComp(comp, name, center)` | Add light |
| `CreateNullInComp(comp, name, dur)` | Add null/adjustment |
| `CreateTextLayerInComp(comp)` | Add text layer |
| `CreateBoxTextLayerInComp(comp, dims)` | Add box text layer |
| `CreateVectorLayerInComp(comp)` | Add shape layer |

### Example

```python
import PyFx

util = PyFx.UtilitySuite()
util.startUndoGroup("create comp")

root = PyFx.ProjSuite().GetProjectRootFolder(
    PyFx.ProjSuite().GetProjectByIndex(0)
)
comp = PyFx.CompSuite().CreateComp(
    root,
    "my_comp",
    1920, 1080,
    1.0,        # square pixels
    125,        # 5 seconds at 25fps (in frames)
    25.0        # fps
)

util.endUndoGroup()
print("Created:", PyFx.ItemSuite().GetItemName(
    PyFx.CompSuite().GetItemFromComp(comp)
))
```

---

## Markers

Composition markers are accessed via the stream API:

```python
marker_stream = PyFx.CompSuite().GetNewCompMarkerStream(comp)
# then use KeyframeSuite to add/query markers
```
