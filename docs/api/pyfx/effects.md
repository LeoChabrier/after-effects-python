# Effects & Masks

## EffectSuite

Apply and manage effects on layers.

```python
effect_suite = PyFx.EffectSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getLayerNumEffects(layer)` | `int` | Number of applied effects |
| `getLayerEffectByIndex(layer, index)` | `EffectRefH` | Get effect by index |
| `getInstalledKeyFromLayerEffect(effect)` | `InstalledKey` | Installed effect identifier |
| `applyEffect(layer, installedKey)` | `EffectRefH` | Apply effect to layer |
| `deleteLayerEffect(effect)` | — | Remove effect |
| `duplicateEffect(effect)` | `EffectRefH` | Duplicate effect |
| `reorderEffect(effect, newIndex)` | — | Change effect order |
| `getEffectFlags(effect)` | `int` | Effect flags (enabled, etc.) |
| `setEffectFlags(effect, mask, flags)` | — | Toggle effect flags |
| `getNumInstalledEffects()` | `int` | Total installed effects in AE |
| `getNextInstalledEffect(key)` | `InstalledKey` | Iterate installed effects |
| `getEffectName(key)` | `str` | Effect display name |
| `getEffectMatchName(key)` | `str` | Effect match name (e.g. `"ADBE Gaussian Blur 2"`) |
| `getEffectCategory(key)` | `str` | Effect category |

### Finding an installed effect

```python
import PyFx

es  = PyFx.EffectSuite()
key = es.getNextInstalledEffect(None)     # start iteration

while key is not None:
    if "Gaussian" in es.getEffectName(key):
        print(es.getEffectMatchName(key))
    key = es.getNextInstalledEffect(key)
```

### Applying an effect

```python
import PyFx

util  = PyFx.UtilitySuite()
es    = PyFx.EffectSuite()
comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()
layer = PyFx.LayerSuite().GetCompLayerByIndex(comp, 0)

# Find Gaussian Blur 2
key = es.getNextInstalledEffect(None)
while key is not None:
    if es.getEffectMatchName(key) == "ADBE Gaussian Blur 2":
        blur_key = key
        break
    key = es.getNextInstalledEffect(key)

util.startUndoGroup("apply blur")
blur_effect = es.applyEffect(layer, blur_key)
util.endUndoGroup()
```

---

## MaskSuite

Create and configure masks on layers.

```python
mask_suite = PyFx.MaskSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getLayerNumMasks(layer)` | `int` | Number of masks on layer |
| `getLayerMaskByIndex(layer, index)` | `MaskRefH` | Get mask by index |
| `createNewMask(layer, index)` | `MaskRefH` | Create new mask |
| `deleteMaskFromLayer(mask)` | — | Delete mask |
| `duplicateMask(mask)` | `MaskRefH` | Duplicate mask |
| `getMaskMode(mask)` | `MaskMode` | Add, Subtract, Intersect, etc. |
| `setMaskMode(mask, mode)` | — | Set blend mode |
| `getMaskInvert(mask)` | `bool` | Inversion state |
| `setMaskInvert(mask, invert)` | — | Set inversion |
| `getMaskID(mask)` | `int` | Unique mask ID |
| `getMaskColor(mask)` | `color` | Mask color (in mask panel) |
| `setMaskColor(mask, color)` | — | Set mask color |
| `getMaskLockState(mask)` | `bool` | Lock state |
| `setMaskLockState(mask, locked)` | — | Lock / unlock mask |
| `getMaskIsRotoBezier(mask)` | `bool` | RotoBezier mode |
| `setMaskIsRotoBezier(mask, value)` | — | Toggle RotoBezier |
| `getMaskFeatherFalloff(mask)` | `falloff` | Feather falloff type |
| `setMaskFeatherFalloff(mask, falloff)` | — | Set feather falloff |

### Mask modes

| Constant | Mode |
|----------|------|
| `AEGP_MaskMode_NONE` | None |
| `AEGP_MaskMode_ADD` | Add |
| `AEGP_MaskMode_SUBTRACT` | Subtract |
| `AEGP_MaskMode_INTERSECT` | Intersect |
| `AEGP_MaskMode_LIGHTEN` | Lighten |
| `AEGP_MaskMode_DARKEN` | Darken |
| `AEGP_MaskMode_DIFFERENCE` | Difference |

---

## MaskOutlineSuite

Edit mask path vertices.

```python
outline_suite = PyFx.MaskOutlineSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getMaskOutlineNumSegments(outline)` | `int` | Number of vertices |
| `getMaskOutlineVertexInfo(outline, index)` | `vertex` | Get vertex (position + tangents) |
| `setMaskOutlineVertexInfo(outline, index, vertex)` | — | Set vertex |
| `createVertex(outline, insertAt)` | — | Add a vertex |
| `deleteVertex(outline, index)` | — | Remove a vertex |
| `isMaskOutlineOpen(outline)` | `bool` | Open path vs. closed |
| `setMaskOutlineOpen(outline, open)` | — | Toggle open/closed |
| `getMaskOutlineNumFeathers(outline)` | `int` | Number of feather points |
| `getMaskOutlineFeatherInfo(outline, index)` | `feather` | Get feather point |
| `setMaskOutlineFeatherInfo(outline, index, feather)` | — | Set feather point |

### Example: create a rectangle mask

```python
import PyFx

util  = PyFx.UtilitySuite()
ms    = PyFx.MaskSuite()
mos   = PyFx.MaskOutlineSuite()
comp  = PyFx.CompSuite().GetMostRecentlyUsedComp()
layer = PyFx.LayerSuite().GetCompLayerByIndex(comp, 0)

util.startUndoGroup("add rect mask")

mask    = ms.createNewMask(layer, 0)
# Access the mask's outline via the stream API, then edit vertices
# (outline handle obtained via DynamicStreamSuite / MaskStream)

util.endUndoGroup()
```

!!! note
    Mask outline handles are obtained via `StreamSuite.GetNewMaskStream()` or `DynamicStreamSuite` — not directly from `MaskSuite`.
