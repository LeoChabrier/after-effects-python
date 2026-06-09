# Utilities

## UtilitySuite

General-purpose utilities: undo groups, error handling, logging, and UI helpers.

```python
util = PyFx.UtilitySuite()
```

### Undo groups

Wrap any operation that modifies the project in an undo group so it can be undone as a single action:

```python
util = PyFx.UtilitySuite()
util.startUndoGroup("my operation")
# ... modifications ...
util.endUndoGroup()
```

| Method | Description |
|--------|-------------|
| `startUndoGroup(name)` | Begin an undoable operation |
| `endUndoGroup()` | End the undoable operation |

### Error handling

| Method | Description |
|--------|-------------|
| `startQuietErrors()` | Suppress AE error dialogs |
| `endQuietErrors(reportQuieted)` | Stop suppressing; optionally report |
| `getLastErrorMessage(bufSize)` | Get the last AE error string |

### Logging

| Method | Description |
|--------|-------------|
| `reportInfo(message)` | Log message to the AE info log |
| `reportInfoUnicode(message)` | Same, Unicode |
| `writeToOSConsole(text)` | Write to the OS console |
| `writeToDebugLog(subsystem, eventType, text)` | Write to AE debug log |

### Color helpers

| Method | Description |
|--------|-------------|
| `getPaintPalForeColor()` | Current foreground paint color |
| `getPaintPalBackColor()` | Current background paint color |
| `setPaintPalForeColor(color)` | Set foreground paint color |
| `setPaintPalBackColor(color)` | Set background paint color |
| `getCharPalFillColor()` | Character panel fill color |
| `getCharPalStrokeColor()` | Character panel stroke color |
| `setCharPalFillColor(color)` | Set character fill color |
| `setCharPalStrokeColor(color)` | Set character stroke color |

### Other

| Method | Description |
|--------|-------------|
| `getMainHWND()` | Get AE main window HWND |
| `getSuppressInteractiveUI()` | Check if UI is suppressed (e.g. render farm) |
| `causeIdleRoutinesToBeCalled()` | Force an idle event |
| `getPluginPath(type)` | Get plugin directory path |

---

## WorldSuite

Create and access raw image buffers.

```python
ws = PyFx.WorldSuite()
```

| Method | Returns | Description |
|--------|---------|-------------|
| `newWorld(type, width, height)` | `WorldH` | Allocate a pixel buffer |
| `getType(world)` | `WorldType` | Pixel format (8, 16, or 32 bit) |
| `getSize(world)` | `(int, int)` | Width and height |
| `getRowBytes(world)` | `int` | Bytes per row (stride) |
| `getBaseAddr8(world)` | `bytes` | Raw 8-bit ARGB pixel data |
| `getBaseAddr16(world)` | `bytes` | Raw 16-bit pixel data |
| `getBaseAddr32(world)` | `bytes` | Raw 32-bit float pixel data |
| `fillOutPFEffectWorld(world)` | `PF_EffectWorld` | Initialize for effect API |
| `fastBlur(radius, mode, quality, world)` | — | Apply a fast blur in-place |
| `newPlatformWorld(type, w, h)` | `PlatformWorldH` | Platform-native world |

### Pixel formats

| Constant | Format |
|----------|--------|
| `AEGP_WorldType_8` | 8 bits per channel ARGB |
| `AEGP_WorldType_16` | 16 bits per channel |
| `AEGP_WorldType_32` | 32-bit float per channel |

---

## MemorySuite

Allocate AE-managed memory (required for some SDK operations that return memory handles).

```python
mem = PyFx.MemorySuite()
```

| Method | Description |
|--------|-------------|
| `NewMemHandle(label, size, flags)` | Allocate a memory handle |
| `FreeMemHandle(handle)` | Release a memory handle |
| `LockMemHandle(handle, ptrPtr)` | Lock and get pointer |
| `UnlockMemHandle(handle)` | Unlock |
| `GetMemHandleSize(handle)` | Get allocated size |
| `ResizeMemHandle(label, newSize, handle)` | Resize allocation |
| `SetMemReportingOn(on)` | Enable memory usage reporting |
| `GetMemStats()` | Get current memory statistics |

---

## MarkerSuite

Create and edit composition or layer markers.

```python
ms = PyFx.MarkerSuite()
```

| Method | Description |
|--------|-------------|
| `getNewMarker()` | Create a new blank marker |
| `duplicateMarker(marker)` | Duplicate a marker |
| `setMarkerFlag(marker, flagType, value)` | Set a marker flag |
| `getMarkerFlag(marker, flagType)` | Get a flag value |
| `getMarkerString(marker, strType)` | Get comment / chapter / URL |
| `setMarkerString(marker, strType, text)` | Set comment / chapter / URL |
| `setMarkerDuration(marker, duration)` | Set marker duration |
| `getMarkerDuration(marker)` | Get marker duration |
| `setMarkerLabel(marker, label)` | Set label color |
| `getMarkerLabel(marker)` | Get label color |
| `countCuePointParams(marker)` | Number of cue point parameters |
| `getIndCuePointParam(marker, index)` | Get a cue point (key, value) pair |
| `setIndCuePointParam(marker, index, key, value)` | Set a cue point |
| `insertCuePointParam(marker, index)` | Insert cue point slot |
| `deleteIndCuePointParam(marker, index)` | Delete cue point |

### Marker string types

| Constant | Content |
|----------|---------|
| `AEGP_MarkerString_COMMENT` | Marker comment text |
| `AEGP_MarkerString_CHAPTER` | Chapter name |
| `AEGP_MarkerString_URL` | Hyperlink URL |
| `AEGP_MarkerString_FRAME_TARGET` | Frame target |
| `AEGP_MarkerString_CUE_POINT_NAME` | Cue point name |
