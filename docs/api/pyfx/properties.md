# Properties & Keyframes

## StreamSuite

Access layer properties (streams) by their built-in type.

```python
stream_suite = PyFx.StreamSuite()
```

### Built-in stream types

Common `whichStream` constants (`AEGP_LayerStream_*`):

| Constant | Property |
|----------|---------|
| `AEGP_LayerStream_ANCHORPOINT` | Anchor Point |
| `AEGP_LayerStream_POSITION` | Position |
| `AEGP_LayerStream_SCALE` | Scale |
| `AEGP_LayerStream_ROTATION` | Rotation (2D) |
| `AEGP_LayerStream_ROTATE_X/Y/Z` | 3D rotations |
| `AEGP_LayerStream_OPACITY` | Opacity |
| `AEGP_LayerStream_AUDIO_LEVELS` | Audio levels |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GetNewLayerStream(layer, whichStream)` | `StreamRefH` | Get a named layer property |
| `GetLayerStreamValue(layer, stream, mode, time, preExpr)` | `value` | Get value at a time |
| `GetStreamType(stream)` | `StreamType` | Value type (float, 2D, 3D, color…) |
| `IsStreamTimevarying(stream)` | `bool` | True if the property is animated |
| `CanVaryOverTime(stream)` | `bool` | True if the property can be animated |
| `GetStreamName(stream, forceEnglish)` | `str` | Property name |
| `SetStreamValue(stream, value)` | — | Set value (non-animated) |

### Example: get/set opacity

```python
import PyFx

ls   = PyFx.LayerSuite()
ss   = PyFx.StreamSuite()
comp = PyFx.CompSuite().GetMostRecentlyUsedComp()
layer = ls.GetCompLayerByIndex(comp, 0)

stream = ss.GetNewLayerStream(layer, PyFx.AEGP_LayerStream_OPACITY)
value  = ss.GetLayerStreamValue(layer, PyFx.AEGP_LayerStream_OPACITY,
                                 PyFx.AEGP_LTimeMode_CompTime, 0, False)
print(f"Opacity: {value}")
```

---

## DynamicStreamSuite

Navigate and modify the full property tree (including effect parameters, groups, and expressions).

```python
dyn = PyFx.DynamicStreamSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GetNewStreamRefForLayer(layer)` | `StreamRefH` | Root property group for a layer |
| `GetNumStreamsInGroup(group)` | `int` | Number of child properties |
| `GetNewStreamRefByIndex(group, index)` | `StreamRefH` | Get child property by index |
| `GetNewStreamRefByMatchname(group, matchName)` | `StreamRefH` | Get property by match name |
| `GetMatchname(stream)` | `str` | ADBE match name (e.g. `"ADBE Position"`) |
| `GetStreamGroupingType(stream)` | `GroupType` | Named, indexed, leaf, etc. |
| `GetStreamDepth(stream)` | `int` | Nesting depth in property tree |
| `GetNewParentStreamRef(stream)` | `StreamRefH` | Parent property group |
| `AddStream(group, matchName)` | `StreamRefH` | Add dynamic property |
| `DeleteStream(stream)` | — | Remove dynamic property |
| `SetStreamName(stream, name)` | — | Rename property |
| `IsSeparationLeader(stream)` | `bool` | Is position/scale separator |
| `AreDimensionsSeparated(leader)` | `bool` | Are X/Y/Z linked or separate |
| `SetDimensionsSeparated(leader, separated)` | — | Separate or link dimensions |

### Example: find a property by match name

```python
import PyFx

layer = PyFx.LayerSuite().GetCompLayerByIndex(
    PyFx.CompSuite().GetMostRecentlyUsedComp(), 0
)
dyn   = PyFx.DynamicStreamSuite()
root  = dyn.GetNewStreamRefForLayer(layer)

position = dyn.GetNewStreamRefByMatchname(root, "ADBE Position")
print(dyn.GetMatchname(position))  # "ADBE Position"
```

---

## KeyframeSuite

Insert, delete, and modify keyframes on any animated property.

```python
kf = PyFx.KeyframeSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GetStreamNumKFs(stream)` | `int` | Number of keyframes |
| `GetKeyframeTime(stream, index, mode)` | `A_Time` | Keyframe time |
| `InsertKeyframe(stream, mode, time)` | `int` | Add keyframe, returns index |
| `DeleteKeyframe(stream, index)` | — | Remove keyframe |
| `GetNewKeyframeValue(stream, index)` | `value` | Get keyframe value |
| `SetKeyframeValue(stream, index, value)` | — | Set keyframe value |
| `GetKeyframeInterpolation(stream, index)` | `(in, out)` | Interpolation type |
| `SetKeyframeInterpolation(stream, index, in, out)` | — | Set interpolation |
| `GetKeyframeTemporalEase(stream, index, dim)` | `(in, out)` | Easing values |
| `SetKeyframeTemporalEase(stream, index, dim, in, out)` | — | Set easing |
| `GetKeyframeFlags(stream, index)` | `int` | Keyframe flags |
| `SetKeyframeFlag(stream, index, flag, value)` | — | Set a keyframe flag |
| `GetKeyframeLabelColorIndex(stream, index)` | `int` | Keyframe color label |
| `SetKeyframeLabelColorIndex(stream, index, label)` | — | Set keyframe color |

### Interpolation types

| Constant | Meaning |
|----------|---------|
| `AEGP_KeyInterp_NO_INTERP` | No interpolation |
| `AEGP_KeyInterp_HOLD` | Hold |
| `AEGP_KeyInterp_LINEAR` | Linear |
| `AEGP_KeyInterp_BEZIER` | Bezier (default) |

### Example: add opacity keyframes

```python
import PyFx

util  = PyFx.UtilitySuite()
ss    = PyFx.StreamSuite()
kf    = PyFx.KeyframeSuite()
comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()
layer = PyFx.LayerSuite().GetCompLayerByIndex(comp, 0)

stream = ss.GetNewLayerStream(layer, PyFx.AEGP_LayerStream_OPACITY)

util.startUndoGroup("opacity keyframes")

t0 = PyFx.A_Time(0, 1)            # frame 0
t1 = PyFx.A_Time(25, 1)           # frame 25

i0 = kf.InsertKeyframe(stream, PyFx.AEGP_LTimeMode_CompTime, t0)
kf.SetKeyframeValue(stream, i0, 0.0)

i1 = kf.InsertKeyframe(stream, PyFx.AEGP_LTimeMode_CompTime, t1)
kf.SetKeyframeValue(stream, i1, 100.0)

util.endUndoGroup()
```
