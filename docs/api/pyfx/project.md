# Project & Items

## ProjSuite

Manages open projects.

```python
proj_suite = PyFx.ProjSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GetNumProjects()` | `int` | Number of currently open projects |
| `GetProjectByIndex(index)` | `ProjectH` | Get project by zero-based index |
| `GetProjectName(project)` | `str` | Project name (without extension) |
| `GetProjectPath(project)` | `str` | Full path to the `.aep` file |
| `GetProjectRootFolder(project)` | `ItemH` | Root folder of the project panel |
| `NewProject()` | `ProjectH` | Create a new empty project |
| `OpenProjectFromPath(path)` | `ProjectH` | Open an existing `.aep` |
| `SaveProjectToPath(project, path)` | — | Save project to a path |
| `SaveProjectAs(project, path)` | — | Save as a new file |
| `ProjectIsDirty(project)` | `bool` | Whether the project has unsaved changes |
| `GetProjectBitDepth(project)` | `int` | Bit depth: 8, 16, or 32 |
| `SetProjectBitDepth(project, depth)` | — | Set bit depth |

### Example

```python
import PyFx

suite = PyFx.ProjSuite()
n     = suite.GetNumProjects()
proj  = suite.GetProjectByIndex(0)

print(suite.GetProjectName(proj))   # "my_comp"
print(suite.GetProjectPath(proj))   # "C:/projects/my_comp.aep"
print(suite.ProjectIsDirty(proj))   # True / False
```

---

## ItemSuite

Iterates and modifies project items — compositions, footage, and folders.

```python
item_suite = PyFx.ItemSuite()
```

### Item types

| Type | Description |
|------|-------------|
| `AEGP_ItemType_COMP` | Composition |
| `AEGP_ItemType_FOOTAGE` | Footage (video, image, solid, placeholder) |
| `AEGP_ItemType_FOLDER` | Folder |

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GetFirstProjItem(project)` | `ItemH` | First item in the project panel |
| `GetNextProjItem(project, item)` | `ItemH` | Next item in iteration (returns None at end) |
| `GetActiveItem()` | `ItemH` | Currently selected item |
| `GetItemType(item)` | `ItemType` | Type enum |
| `GetTypeName(type)` | `str` | Human-readable type name |
| `GetItemName(item)` | `str` | Item name |
| `SetItemName(item, name)` | — | Rename an item |
| `GetItemID(item)` | `int` | Unique persistent ID |
| `IsItemSelected(item)` | `bool` | Selection state |
| `SelectItem(item, select, deselectOthers)` | — | Change selection |
| `GetItemParentFolder(item)` | `ItemH` | Parent folder |
| `SetItemParentFolder(item, folder)` | — | Move to folder |
| `GetItemDuration(item)` | `A_Time` | Duration |
| `GetItemDimensions(item)` | `(int, int)` | Width, height |
| `GetItemPixelAspectRatio(item)` | `float` | Pixel aspect ratio |
| `DeleteItem(item)` | — | Remove from project |
| `CreateNewFolder(name, parentFolder)` | `ItemH` | Create a folder |
| `GetItemComment(item)` | `str` | Comment/description |
| `SetItemComment(item, comment)` | — | Set comment |
| `GetItemLabel(item)` | `int` | Label color index |
| `SetItemLabel(item, label)` | — | Set label color |

### Example: iterate all items

```python
import PyFx

proj_suite = PyFx.ProjSuite()
item_suite = PyFx.ItemSuite()

proj = proj_suite.GetProjectByIndex(0)
item = item_suite.GetFirstProjItem(proj)

while item is not None:
    name = item_suite.GetItemName(item)
    kind = item_suite.GetItemType(item)
    print(f"{kind}: {name}")
    item = item_suite.GetNextProjItem(proj, item)
```

---

## FootageSuite

Manages source footage — importing, replacing, and querying media.

```python
footage_suite = PyFx.FootageSuite()
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getMainFootageFromItem(item)` | `FootageH` | Footage attached to a project item |
| `getProxyFootageFromItem(item)` | `FootageH` | Proxy footage if set |
| `getFootagePath(footage, frame, fileIndex)` | `str` | File path for a given frame |
| `newFootage(path, layerInfo, seqOptions, interpStyle)` | `FootageH` | Import footage |
| `addFootageToProject(footage, folder)` | `ItemH` | Add to the project panel |
| `replaceItemMainFootage(footage, item)` | — | Replace footage on an existing item |
| `newSolidFootage(name, width, height, color)` | `FootageH` | Create a solid |
| `getSolidFootageColor(item, proxy)` | `color` | Get solid color |
| `setSolidFootageColor(item, proxy, color)` | — | Set solid color |
| `getFootageInterpretation(item, proxy)` | `InterpH` | Get interpretation settings |
| `setFootageInterpretation(item, proxy, interp)` | — | Set interpretation |

### Example: import footage

```python
import PyFx

suite     = PyFx.FootageSuite()
proj_item = PyFx.ItemSuite()
root      = PyFx.ProjSuite().GetProjectRootFolder(proj)

footage = suite.newFootage(
    r"C:\footage\plate.exr",
    None, None, 0
)
suite.addFootageToProject(footage, root)
```
