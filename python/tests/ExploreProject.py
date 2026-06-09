# Third-Party
import PyFx


proj_suite  = PyFx.ProjSuite()
item_suite  = PyFx.ItemSuite()
comp_suite  = PyFx.CompSuite()
layer_suite = PyFx.LayerSuite()

project = proj_suite.GetProjectByIndex(0)
print(f"Project : {proj_suite.GetProjectPath(project)}")


item = item_suite.GetFirstProjItem(project)
first_comp = None

while item is not None:
    try:
        name = item_suite.GetItemName(item)
        kind = str(item_suite.GetItemType(item))
        print(f"  {kind:<20} {name}")
        if first_comp is None and 'COMP' in kind.upper():
            first_comp = item
        item = item_suite.GetNextProjItem(project, item)
    except Exception:
        break

if first_comp is not None:
    comp_name = item_suite.GetItemName(first_comp)
    comp      = comp_suite.GetCompFromItem(first_comp)
    n_layers  = layer_suite.GetCompNumLayers(comp)
    print(f"\nComp '{comp_name}' — {n_layers} layer(s)")
    for i in range(n_layers):
        layer = layer_suite.GetCompLayerByIndex(comp, i)
        name  = layer_suite.GetLayerName(layer)
        kind  = str(layer_suite.GetLayerObjectType(layer))
        print(f"  [{i}] {kind:<16} {name}")
else:
    print("\nNo comp found in current project.")
