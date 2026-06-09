# Render

## RenderSuite

Renders individual frames on demand (outside the render queue).

```python
render_suite = PyFx.RenderSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `renderAndCheckoutFrame(options)` | `ReceiptH` | Render a frame and return a receipt |
| `renderAndCheckoutLayerFrame(options)` | `ReceiptH` | Render a single layer's frame |
| `getReceiptWorld(receipt)` | `WorldH` | Get the rendered image buffer |
| `getRenderedRegion(receipt)` | `rect` | The region that was rendered |
| `getCurrentTimestamp()` | `timestamp` | Current AE render timestamp |
| `checkinRenderedFrame(options, stamp, ticks, world)` | — | Return a rendered frame to AE's cache |
| `cancelAsyncRequest(id)` | — | Cancel an async render request |

### Example: render current frame

```python
import PyFx

comp   = PyFx.CompSuite().GetMostRecentlyUsedComp()
time   = PyFx.CompSuite().GetCompWorkAreaStart(comp)

opts   = PyFx.RenderOptionsSuite().newFromItem(
    PyFx.CompSuite().GetItemFromComp(comp)
)
PyFx.RenderOptionsSuite().setTime(opts, time)

rs      = PyFx.RenderSuite()
receipt = rs.renderAndCheckoutFrame(opts)
world   = rs.getReceiptWorld(receipt)

w, h    = PyFx.WorldSuite().getSize(world)
print(f"Rendered: {w}x{h}")
```

---

## RenderOptionsSuite

Configure what and how to render before calling `RenderSuite`.

```python
opts = PyFx.RenderOptionsSuite()
```

| Method | Description |
|--------|-------------|
| `newFromItem(item)` | Create render options for a comp or footage item |
| `duplicate(options)` | Clone render options |
| `setTime(options, time)` | Set render time |
| `getTime(options)` | Get render time |
| `setDownsampleFactor(options, factor)` | Set resolution (1 = full, 2 = half, etc.) |
| `getDownsampleFactor(options)` | Get resolution |
| `setWorldType(options, type)` | Set pixel format (`BYTE`, `WORD`, `FLOAT`) |
| `getWorldType(options)` | Get pixel format |
| `setFieldRender(options, mode)` | Enable/disable field rendering |
| `setRegionOfInterest(options, rect)` | Render a sub-region |

---

## RenderQueueSuite

Manage the AE render queue.

```python
rq = PyFx.RenderQueueSuite()
```

| Method | Description |
|--------|-------------|
| `addCompToRenderQueue(comp, path)` | Add comp to queue with output path |
| `setRenderQueueState(state)` | Start (`RENDERING`) or stop the queue |
| `getRenderQueueState()` | Current state of the render queue |

### Render queue states

| Constant | Meaning |
|----------|---------|
| `AEGP_RenderQueueState_STOPPED` | Idle |
| `AEGP_RenderQueueState_PAUSED` | Paused |
| `AEGP_RenderQueueState_RENDERING` | Actively rendering |

---

## RenderQueueItemSuite

Query and modify individual render queue entries.

```python
rqi = PyFx.RenderQueueItemSuite()
```

| Method | Description |
|--------|-------------|
| `getNumRQItems()` | Total items in queue |
| `getRQItemByIndex(index)` | Get item by index |
| `getNextRQItem(item)` | Iterate the queue |
| `getRenderState(item)` | Current render state |
| `setRenderState(item, state)` | Enable/disable rendering |
| `getCompFromRQItem(item)` | Get composition |
| `getComment(item)` | Get comment |
| `setComment(item, text)` | Set comment |
| `deleteRQItem(item)` | Remove from queue |

---

## OutputModuleSuite

Configure output modules on render queue items.

```python
om = PyFx.OutputModuleSuite()
```

| Method | Description |
|--------|-------------|
| `getOutputModuleByIndex(rqItem, index)` | Get output module |
| `getOutputFilePath(rqItem, outmod)` | Get output file path |
| `setOutputFilePath(rqItem, outmod, path)` | Set output path |
| `addDefaultOutputModule(rqItem)` | Add a default output module |
| `getEnabledOutputs(rqItem, outmod)` | Get enabled output types |
| `setEnabledOutputs(rqItem, outmod, types)` | Set output types |
| `getSoundFormatInfo(rqItem, outmod)` | Get audio format settings |
| `setSoundFormatInfo(rqItem, outmod, fmt, enabled)` | Set audio format |

### Example: add comp to render queue

```python
import PyFx

util = PyFx.UtilitySuite()
rq   = PyFx.RenderQueueSuite()
rqi  = PyFx.RenderQueueItemSuite()
om   = PyFx.OutputModuleSuite()
comp = PyFx.CompSuite().GetMostRecentlyUsedComp()

util.startUndoGroup("add to render queue")

rq.addCompToRenderQueue(comp, r"C:\output\frame_[####].exr")

util.endUndoGroup()
print(f"Queue items: {rqi.getNumRQItems()}")
```
