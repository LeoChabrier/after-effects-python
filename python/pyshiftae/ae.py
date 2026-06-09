"""PyShiftAE high-level API for Adobe After Effects.

Provides Pythonic wrappers around the low-level `PyFx` C++ bindings,
exposing After Effects projects, compositions, layers, properties, effects
and masks as idiomatic Python objects.

Examples:
    >>> from pyshiftae import ae
    >>> project = ae.Project()
    >>> comp = project.items["My Comp"]
    >>> for layer in comp.layers:
    ...     print(layer.name)
"""

import operator
import PyFx  # type: ignore
import os
from typing import Any, Iterator, List, Tuple, Union


class AssetManager:
    """Manage importing and replacing footage assets in After Effects.

    Examples:
        >>> manager = AssetManager()
        >>> item = manager.import_asset("C:/assets/plate.exr", "plate")
    """

    def __init__(self) -> None:
        pass

    def import_asset(self, file_path: str, name: str) -> PyFx.ItemPtr:
        """Import a file or image sequence into the current project.

        Determines whether the path points to a single file or a directory
        (image sequence) and creates the appropriate footage item.

        Args:
            file_path: Absolute path to the file or sequence directory.
            name: Display name for the imported footage item.

        Returns:
            The newly created project item pointer.

        Raises:
            Exception: If `file_path` is neither a file nor a directory.

        Examples:
            >>> manager = AssetManager()
            >>> item = manager.import_asset("C:/assets/plate.exr", "plate")
            >>>
            >>> # Import an image sequence from a directory
            >>> seq = manager.import_asset("C:/assets/seq/", "beauty_pass")
        """
        suite = PyFx.FootageSuite()
        item = None
        footage = None
        if os.path.splitext(file_path)[1]:  # This is a single file
            footage = suite.newFootage(
                file_path,
                PyFx.FootageLayerKey(nameAC=name),
                None,
                PyFx.InterpretationStyle.NO_DIALOG_NO_GUESS,
            )
        elif os.path.isdir(file_path):  # This is a sequence
            footage = suite.newFootage(
                file_path,
                PyFx.FootageLayerKey(nameAC=name),
                PyFx.FileSequenceImportOptions().sequence(),
                PyFx.InterpretationStyle.NO_DIALOG_NO_GUESS,
            )
        else:
            raise Exception("Invalid file path")
        if footage:
            item = suite.addFootageToProject(
                footage,
                PyFx.ProjSuite().GetProjectRootFolder(
                    PyFx.ProjSuite().GetProjectByIndex(0)
                ),
            )
        return item

    def replace_asset(
        self, old_asset: PyFx.ItemPtr, new_file_path: str
    ) -> None:
        """Replace an existing footage item's source with a new file.

        Args:
            old_asset: The project item whose footage will be replaced.
            new_file_path: Absolute path to the replacement file.

        Raises:
            Exception: If the new footage cannot be imported.

        Examples:
            >>> manager = AssetManager()
            >>> manager.replace_asset(old_item, "C:/assets/plate_v002.exr")
        """
        suite = PyFx.FootageSuite()
        new_footage = self.import_asset(new_file_path, "")
        if new_footage:
            suite.replaceItemMainFootage(
                suite.getMainFootageFromItem(old_asset), new_footage
            )
        else:
            raise Exception("Failed to import new footage")


class App:
    """Interface to After Effects application-level utilities.

    Examples:
        >>> app = App()
        >>> app.report_info("Script finished successfully")
    """

    _suite = PyFx.UtilitySuite()

    def __init__(self) -> None:
        pass

    def report_info(self, message: str) -> None:
        """Display an informational message in the After Effects info bar.

        Args:
            message: Text to display.

        Examples:
            >>> App().report_info("Processing complete")
        """
        self._suite.reportInfo(message)


class Item:
    """Base class for all After Effects project items.

    Wraps a raw ``PyFx.ItemPtr`` and exposes common item properties
    such as name, duration, dimensions, selection state and flags.

    Args:
        item: Raw item pointer from the AE SDK.

    Examples:
        >>> item = Item.active_item()
        >>> print(item.name, item.type)
        >>>
        >>> item.name = "Renamed Item"
        >>> item.selected = True
    """

    _suite = PyFx.ItemSuite()

    def __init__(self, item: PyFx.ItemPtr) -> None:
        self.item = item

    @staticmethod
    def active_item() -> Union["Item", "CompItem", "FootageItem", None]:
        """Return the currently active (selected) item in the project panel.

        Returns:
            The active item as the appropriate typed subclass, or `None`
            if no item is selected.

        Examples:
            >>> item = Item.active_item()
            >>> if item:
            ...     print(item.name)
        """
        item_ptr = PyFx.ItemSuite().GetActiveItem()
        if item_ptr:
            return ItemFactory.create_item(item_ptr)

    @property
    def name(self) -> str:
        """str: Display name of the item."""
        try:
            name = self._suite.GetItemName(self.item)
        except Exception as e:
            raise e
        return name

    @name.setter
    def name(self, value: str) -> None:
        self._suite.SetItemName(self.item, value)

    @property
    def type(self) -> PyFx.ItemType:
        """PyFx.ItemType: Item type (``FOLDER``, ``COMP``, or ``FOOTAGE``)."""
        return self._suite.GetItemType(self.item)

    @property
    def parent_folder(self) -> "FolderItem":
        """FolderItem: Folder containing this item."""
        return FolderItem(self._suite.GetItemParentFolder(self.item))

    @parent_folder.setter
    def parent_folder(self, folder: "FolderItem") -> None:
        self._suite.SetItemParentFolder(self.item, folder.item)

    @property
    def duration(self) -> float:
        """float: Duration of the item in seconds."""
        return self._suite.GetItemDuration(self.item)

    @property
    def current_time(self) -> float:
        """float: Current time indicator position in seconds."""
        return self._suite.GetItemCurrentTime(self.item)

    @current_time.setter
    def current_time(self, value: float) -> None:
        self._suite.SetItemCurrentTime(self.item, value)

    @property
    def comment(self) -> str:
        """str: User comment attached to the item."""
        return self._suite.GetItemComment(self.item)

    @comment.setter
    def comment(self, value: str) -> None:
        self._suite.SetItemComment(self.item, value)

    @property
    def label(self) -> int:
        """int: Label color index (0-15)."""
        return self._suite.GetItemLabel(self.item)

    @label.setter
    def label(self, value: int) -> None:
        self._suite.SetItemLabel(self.item, value)

    @property
    def dimensions(self) -> tuple[int, int]:
        """tuple[int, int]: Width and height in pixels."""
        return self._suite.GetItemDimensions(self.item)

    @property
    def pixel_aspect(self) -> float:
        """float: Pixel aspect ratio."""
        return self._suite.GetItemPixelAspectRatio(self.item)

    @property
    def selected(self) -> bool:
        """bool: Whether the item is selected in the project panel."""
        return self._suite.IsItemSelected(self.item)

    @selected.setter
    def selected(self, value: bool) -> None:
        self._suite.SelectItem(self.item, value)

    @property
    def missing(self) -> bool:
        """bool: Whether the item's source footage is missing."""
        return self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.MISSING

    @property
    def has_proxy(self) -> bool:
        """bool: Whether the item has a proxy assigned."""
        return self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.HAS_PROXY

    @property
    def using_proxy(self) -> bool:
        """bool: Whether the item is currently using its proxy."""
        return self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.USING_PROXY

    @using_proxy.setter
    def use_proxy(self, value: bool) -> None:
        self._suite.SetItemUseProxy(self.item, value)

    @property
    def missing_proxy(self) -> bool:
        """bool: Whether the item's proxy footage is missing."""
        return self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.MISSING_PROXY

    @property
    def has_video(self) -> bool:
        """bool: Whether the item contains video data."""
        return self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.HAS_VIDEO

    @property
    def has_audio(self) -> bool:
        """bool: Whether the item contains audio data."""
        return self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.HAS_AUDIO

    @property
    def still(self) -> bool:
        """bool: Whether the item is a still image (single frame)."""
        return self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.STILL

    @property
    def has_active_audio(self) -> bool:
        """bool: Whether the item has active (unmuted) audio."""
        return (
            self._suite.GetItemFlags(self.item) & PyFx.ItemFlag.HAS_ACTIVE_AUDIO
        )

    @use_proxy.setter
    def use_proxy(self, value: bool) -> None:
        self._suite.SetItemUseProxy(self.item, value)

    def delete(self) -> None:
        """Remove this item from the project."""
        self._suite.DeleteItem(self.item)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: "Item") -> bool:
        return self.item == other.item

    def __ne__(self, other: "Item") -> bool:
        return self.item != other.item

    # override python garbage collection, ensuring nothing happens.
    def __del__(self) -> None:
        pass


class FolderItem(Item):
    """A folder in the After Effects project panel.

    Folders contain other items (compositions, footage, sub-folders)
    accessible via the :attr:`children` collection.

    Args:
        item: Raw item pointer for a folder.

    Examples:
        >>> project = Project()
        >>> root = project.items
        >>> folder = root.get_item(name="Assets")
        >>> for child in folder.children:
        ...     print(child.name)
    """

    def __init__(self, item: PyFx.ItemPtr) -> None:
        super().__init__(item)

    @property
    def children(self) -> "ItemCollection":
        """ItemCollection: All items directly inside this folder."""
        return ItemCollection.create(self.item)

    def add_item(self, item: Item) -> None:
        """Move an item into this folder.

        Args:
            item: The item to move.

        Examples:
            >>> folder.add_item(comp_item)
        """
        self._suite.SetItemParentFolder(item.item, self.item)

    def remove_item(self, item: Item) -> None:
        """Remove an item from this folder (moves it to the project root).

        Args:
            item: The item to remove.
        """
        self._suite.SetItemParentFolder(item.item, None)


class CompItem(Item):
    """An After Effects composition.

    Provides access to layers, comp settings (frame rate, background color,
    downsample factor) and layer creation helpers via :attr:`layers`.

    Can be constructed from either an ``ItemPtr`` or a ``CompPtr``.

    Args:
        item: Raw item or comp pointer.

    Examples:
        >>> comp = CompItem.most_recent()
        >>> print(comp.name, comp.frame_rate, comp.duration)
        >>>
        >>> new_comp = CompItem.create("Precomp", 1920, 1080, 1.0, 10.0, 24.0)
    """

    _compSuite = PyFx.CompSuite()

    def __init__(self, item: Union[PyFx.ItemPtr, PyFx.CompPtr]) -> None:
        self.comp = (
            item
            if isinstance(item, PyFx.CompPtr)
            else PyFx.CompSuite().GetCompFromItem(item)
        )
        super().__init__(
            item
            if isinstance(item, PyFx.ItemPtr)
            else PyFx.CompSuite().GetItemFromComp(item)
        )

    @classmethod
    def most_recent(cls) -> "CompItem":
        """Return the most recently used composition.

        Returns:
            The most recently active comp.

        Examples:
            >>> comp = CompItem.most_recent()
            >>> print(comp.name)
        """
        return cls(PyFx.CompSuite().GetMostRecentlyUsedComp())

    @classmethod
    def create(
        cls,
        name: str,
        width: int,
        height: int,
        pixel_aspect: float,
        duration: float,
        frame_rate: float,
        parent: Item = None,
    ) -> "CompItem":
        """Create a new composition.

        Args:
            name: Composition name.
            width: Width in pixels.
            height: Height in pixels.
            pixel_aspect: Pixel aspect ratio (1.0 for square pixels).
            duration: Duration in seconds.
            frame_rate: Frames per second.
            parent: Optional folder to place the comp in.

        Returns:
            The newly created composition.

        Examples:
            >>> comp = CompItem.create("Main Comp", 1920, 1080, 1.0, 30.0, 24.0)
            >>> print(comp.name)
            'Main Comp'
        """
        comp = PyFx.CompSuite().CreateComp(
            name, width, height, pixel_aspect, duration, frame_rate
        )
        if parent:
            PyFx.ItemSuite().SetItemParentFolder(comp, parent)
        return cls(comp)

    @property
    def layers(self) -> "LayerCollection":
        """LayerCollection: All layers in this composition."""
        return LayerCollection.create(self.comp)

    @property
    def downsample_factor(self) -> PyFx.DownsampleFactor:
        """PyFx.DownsampleFactor: Current downsample (resolution) factor."""
        return self._compSuite.GetCompDownsampleFactor(self.comp)

    @downsample_factor.setter
    def downsample_factor(self, value: PyFx.DownsampleFactor) -> None:
        self._compSuite.SetCompDownsampleFactor(self.comp, value)

    @property
    def background_color(self) -> tuple[float, float, float, float]:
        """tuple[float, float, float, float]: Composition background color (RGBA, 0.0-1.0)."""
        color: PyFx.ColorVal = self._compSuite.GetCompBGColor(self.comp)
        return color.to_tuple()

    @background_color.setter
    def background_color(
        self, value: tuple[float, float, float, float]
    ) -> None:
        PyFx.CompSuite().SetCompBGColor(self.comp, PyFx.ColorVal(value))

    @property
    def show_layer_name_or_source_name(self) -> bool:
        """bool: Whether the timeline shows layer names (`True`) or source names (`False`)."""
        return PyFx.CompSuite().GetShowLayerNameOrSourceName(self.comp)

    @show_layer_name_or_source_name.setter
    def show_layer_name_or_source_name(self, value: bool) -> None:
        PyFx.CompSuite().SetShowLayerNameOrSourceName(self.comp, value)

    @property
    def show_blend_modes(self) -> bool:
        """bool: Whether blend mode columns are visible in the timeline."""
        return PyFx.CompSuite().GetShowBlendModes(self.comp)

    @show_blend_modes.setter
    def show_blend_modes(self, value: bool) -> None:
        PyFx.CompSuite().SetShowBlendModes(self.comp, value)

    @property
    def frame_rate(self) -> float:
        """float: Composition frame rate in frames per second."""
        return PyFx.CompSuite().GetCompFramerate(self.comp)

    @frame_rate.setter
    def frame_rate(self, value: float) -> None:
        PyFx.CompSuite().SetCompFrameRate(self.comp, value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: "CompItem") -> bool:
        return self.comp == other.comp

    def __ne__(self, other: "CompItem") -> bool:
        return self.comp != other.comp


class FootageItem(Item):
    """A footage item in the After Effects project.

    Represents imported media (images, video, sequences) or generated
    items (solids, placeholders).

    Args:
        item: Raw item pointer for a footage item.

    Examples:
        >>> footage = FootageItem.create("C:/assets/plate.exr", "plate")
        >>> print(footage.name, footage.num_files)
        >>>
        >>> solid = FootageItem.create_solid("BG", 1920, 1080, (0.0, 0.0, 0.0, 1.0))
    """

    def __init__(self, item: PyFx.ItemPtr) -> None:
        super().__init__(item)
        self.footage = PyFx.FootageSuite().getMainFootageFromItem(item)

    @classmethod
    def create(cls, path: str, name: str) -> "FootageItem":
        """Import a file as a new footage item.

        Args:
            path: Absolute path to the source file.
            name: Display name for the footage item.

        Returns:
            The imported footage item.

        Examples:
            >>> footage = FootageItem.create("C:/assets/plate.exr", "plate")
        """
        item: PyFx.ItemPtr = AssetManager().import_asset(path, name)
        return ItemFactory.create_item(item)

    @classmethod
    def create_placeholder(
        cls,
        path: str,
        width: int,
        height: int,
        duration: float,
        platform: PyFx.Platform = PyFx.Platform.WIN,
    ) -> "FootageItem":
        """Create a placeholder footage item.

        Useful for setting up a project structure before media is available.

        Args:
            path: Reference path for the placeholder.
            width: Width in pixels.
            height: Height in pixels.
            duration: Duration in seconds.
            platform: Target platform (default `PyFx.Platform.WIN`).

        Returns:
            The placeholder footage item.

        Examples:
            >>> placeholder = FootageItem.create_placeholder(
            ...     "C:/renders/beauty.exr", 1920, 1080, 10.0
            ... )
        """
        footage = PyFx.FootageSuite().newPlaceholderFootage(
            path, width, height, duration, platform
        )
        item = PyFx.FootageSuite().addFootageToProject(
            footage,
            PyFx.ProjSuite().GetProjectRootFolder(
                PyFx.ProjSuite().GetProjectByIndex(0)
            ),
        )
        return cls(item)

    @classmethod
    def create_solid(
        cls,
        name: str,
        width: int,
        height: int,
        color: tuple[float, float, float, float],
    ) -> "FootageItem":
        """Create a solid-color footage item.

        Args:
            name: Display name for the solid.
            width: Width in pixels.
            height: Height in pixels.
            color: RGBA color tuple (0.0-1.0 per channel).

        Returns:
            The solid footage item.

        Examples:
            >>> solid = FootageItem.create_solid("Black Solid", 1920, 1080, (0.0, 0.0, 0.0, 1.0))
        """
        footage = PyFx.FootageSuite().newSolidFootage(
            name, width, height, PyFx.ColorVal(color)
        )
        item = PyFx.FootageSuite().addFootageToProject(
            footage,
            PyFx.ProjSuite().GetProjectRootFolder(
                PyFx.ProjSuite().GetProjectByIndex(0)
            ),
        )
        return cls(item)

    @property
    def num_files(self) -> tuple[int, int]:
        """tuple[int, int]: Number of files and folders in the footage source."""
        return PyFx.FootageSuite().getFootageNumFiles(self.footage)

    def path(self, frame_num: int = 0, index: int = 0) -> str:
        """Get the file path for a specific frame of the footage.

        Args:
            frame_num: Frame number (default 0).
            index: File index for multi-file sources (default 0).

        Returns:
            Absolute file path for the requested frame.

        Examples:
            >>> footage.path()
            'C:/assets/plate.exr'
            >>> footage.path(frame_num=50)
            'C:/assets/seq/plate.0050.exr'
        """
        return PyFx.FootageSuite().getFootagePath(
            self.footage, frame_num, index
        )

    def set_proxy(self, footage: "FootageItem") -> None:
        """Assign a proxy source to this footage item.

        Args:
            footage: The footage item to use as proxy.

        Examples:
            >>> footage.set_proxy(low_res_footage)
        """
        PyFx.FootageSuite().setItemProxyFootage(self.footage, footage.footage)

    def replace_from_path(self, path: str) -> None:
        """Replace this footage item's source with a new file.

        Args:
            path: Absolute path to the replacement file.

        Examples:
            >>> footage.replace_from_path("C:/assets/plate_v002.exr")
        """
        AssetManager().replace_asset(self.item, path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: "FootageItem") -> bool:
        return self.footage == other.footage

    def __ne__(self, other: "FootageItem") -> bool:
        return self.footage != other.footage


class ItemFactory:
    """Factory for creating typed Item subclasses from raw pointers.

    Inspects the item type at runtime and returns the appropriate
    subclass (`FolderItem`, `CompItem`, `FootageItem`, or `Item`).

    Examples:
        >>> item = ItemFactory.create_item(raw_ptr)
        >>> isinstance(item, CompItem)
        True
    """

    @staticmethod
    def create_item(
        item: PyFx.ItemPtr,
    ) -> Union[Item, FolderItem, CompItem, FootageItem]:
        """Create a typed Item wrapper from a raw item pointer.

        Args:
            item: Raw item pointer from the AE SDK.

        Returns:
            The item wrapped as the appropriate subclass.
        """
        type = PyFx.ItemSuite().GetItemType(item)  # get the item type
        if type == PyFx.ItemType.FOLDER:
            return FolderItem(item)
        elif type == PyFx.ItemType.COMP:
            return CompItem(item)
        elif type == PyFx.ItemType.FOOTAGE:
            return FootageItem(item)
        else:
            return Item(item)


class ItemCollection(list):
    """Ordered collection of project items within a folder.

    Extends `list` with name-based indexing and criteria-based search.
    Mutating the collection (append, remove, clear) also updates the
    After Effects project in place.

    Examples:
        >>> project = Project()
        >>> items = project.items
        >>> comp = items["My Comp"]
        >>>
        >>> # Search by attribute
        >>> footage = items.get_item(name="plate.exr")
        >>> comps = items.get_items(type=PyFx.ItemType.COMP)
    """

    _ROOT_FOLDER = None

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def create(cls, root_folder: PyFx.ItemPtr) -> "ItemCollection":
        """Build a collection from all direct children of a folder.

        Args:
            root_folder: Item pointer for the parent folder.

        Returns:
            Collection populated with typed item wrappers.
        """
        collection = cls()
        current_item = root_folder
        cls._ROOT_FOLDER = root_folder
        proj = PyFx.ProjSuite().GetProjectByIndex(0)
        while current_item:
            if (
                PyFx.ItemSuite().GetItemParentFolder(current_item)
                == root_folder
            ):
                item = ItemFactory.create_item(current_item)
                collection.append(item)
            current_item = PyFx.ItemSuite().GetNextProjItem(proj, current_item)
        return collection

    def __getitem__(self, key: any) -> Item:
        """Get an item by integer index or by name.

        Args:
            key: Integer index or string name.

        Returns:
            The matching item.

        Raises:
            KeyError: If no item with the given name exists.

        Examples:
            >>> items[0]
            CompItem(My Comp)
            >>> items["plate.exr"]
            FootageItem(plate.exr)
        """
        if isinstance(key, int):
            return super().__getitem__(key)
        for item in self:
            if self._suite.GetItemName(item.item) == key:
                return item
        raise KeyError(f"Item with name '{key}' not found")

    def append(self, object: Item) -> None:
        """Add an item to this collection, moving it into the folder if needed.

        Args:
            object: The item to add.
        """
        if self._suite.GetItemParentFolder(object.item) != self._ROOT_FOLDER:
            self._suite.SetItemParentFolder(
                object.item, self._ROOT_FOLDER
            )  # set the parent folder
        super().append(object)  # append the object to the list

    def remove(self, object: Item) -> None:
        """Delete an item from the project and remove it from this collection.

        Args:
            object: The item to delete.
        """
        self._suite.DeleteItem(object.item)  # delete the item
        super().remove(object)

    def clear(self) -> None:
        """Delete all items in this collection from the project."""
        for item in self:
            self._suite.DeleteItem(item.item)
        super().clear()

    def __iter__(self) -> Iterator:
        return super().__iter__()

    def get_item(self, **criteria) -> Item:
        """Retrieve the first item matching all criteria.

        Supports nested attributes via dot notation.

        Args:
            **criteria: Key-value pairs where keys are attribute names
                (or dot-separated paths) and values are expected values.

        Returns:
            The first item matching all criteria.

        Raises:
            KeyError: If no matching item is found.

        Examples:
            >>> items.get_item(name="My Comp")
            CompItem(My Comp)
            >>>
            >>> items.get_item(type=PyFx.ItemType.FOOTAGE, name="plate.exr")
            FootageItem(plate.exr)
        """

        def match(item: Item, attr_path: str, value: Any) -> bool:
            attr = operator.attrgetter(attr_path)
            try:
                return attr(item) == value
            except AttributeError:
                return False

        for item in self:
            if all(match(item, key, val) for key, val in criteria.items()):
                return item

        raise KeyError(f"Item with criteria '{criteria}' not found")

    def get_items(self, **criteria) -> "ItemCollection":
        """Retrieve all items matching the given criteria.

        Supports nested attributes via dot notation.

        Args:
            **criteria: Key-value pairs where keys are attribute names
                (or dot-separated paths) and values are expected values.

        Returns:
            A new collection containing only the matching items.

        Examples:
            >>> comps = items.get_items(type=PyFx.ItemType.COMP)
            >>> print(len(comps))
        """

        def match(item: Item, attr_path: str, value: Any) -> bool:
            attr = operator.attrgetter(attr_path)
            try:
                return attr(item) == value
            except AttributeError:
                return False

        items = ItemCollection()
        for item in self:
            if all(match(item, key, val) for key, val in criteria.items()):
                items.append(item)
        return items

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({super().__str__()})"

    def __len__(self) -> int:
        return super().__len__()


class BaseProperty:
    """Base class for all After Effects property (stream) wrappers.

    Provides common operations: naming, lookup by match name or index,
    duplication, reordering, and keyframe count.

    Args:
        property: Raw stream reference pointer.

    Examples:
        >>> prop = layer.get_property(PyFx.LayerStream.OPACITY)
        >>> print(prop.name, prop.match_name)
        >>> print(prop.num_keys())
    """

    _suite = PyFx.StreamSuite()
    _dyn_suite = PyFx.DynamicStreamSuite()

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        self.property = property

    @property
    def name(self) -> str:
        """str: Display name of the property."""
        return self._suite.GetStreamName(self.property)

    @name.setter
    def name(self, value: str) -> None:
        self._dyn_suite.SetStreamName(self.property, value)

    @property
    def type(self) -> PyFx.StreamType:
        """PyFx.StreamType: Data type of this property stream."""
        return self._suite.GetStreamType(self.property)

    @property
    def group_type(self) -> PyFx.StreamGroupingType:
        """PyFx.StreamGroupingType: Grouping type (`LEAF`, `INDEXED_GROUP`, or `NAMED_GROUP`)."""
        return self._dyn_suite.GetStreamGroupingType(self.property)

    @property
    def match_name(self) -> str:
        """str: Internal match name used for scripting (e.g. `ADBE Opacity`)."""
        return self._dyn_suite.GetMatchname(self.property)

    def duplicate(
        self,
    ) -> Union[
        "BaseProperty",
        "PropertyGroup",
        "OneDProperty",
        "TwoDProperty",
        "ThreeDProperty",
        "ColorProperty",
        "MarkerProperty",
        "LayerIDProperty",
        "MaskIDProperty",
        "MaskOutlineProperty",
        "TextDocumentProperty",
    ]:
        """Duplicate this property stream.

        Returns:
            A new typed property wrapper for the duplicate.
        """
        new_stream = self._dyn_suite.DuplicateStream(self.property)
        stream = self._dyn_suite.GetNewStreamRefByIndex(
            self.property, new_stream
        )
        return PropertyFactory.create_property(stream)

    def reorder(self, index: int) -> None:
        """Move this property to a new index within its parent group.

        Args:
            index: Target index position.
        """
        self._dyn_suite.ReorderStream(self.property, index)

    def get_property(self, name: str) -> Union[
        "BaseProperty",
        "PropertyGroup",
        "OneDProperty",
        "TwoDProperty",
        "ThreeDProperty",
        "ColorProperty",
        "MarkerProperty",
        "LayerIDProperty",
        "MaskIDProperty",
        "MaskOutlineProperty",
        "TextDocumentProperty",
    ]:
        """Get a child property by match name.

        Args:
            name: Match name of the child property.

        Returns:
            The child property as the appropriate typed subclass.

        Examples:
            >>> group.get_property("ADBE Opacity")
            OneDProperty(Opacity)
        """
        stream = self._dyn_suite.GetNewStreamRefByMatchname(self.property, name)
        return PropertyFactory.create_property(stream)

    def get_property_by_index(self, index: int) -> Union[
        "BaseProperty",
        "PropertyGroup",
        "OneDProperty",
        "TwoDProperty",
        "ThreeDProperty",
        "ColorProperty",
        "MarkerProperty",
        "LayerIDProperty",
        "MaskIDProperty",
        "MaskOutlineProperty",
        "TextDocumentProperty",
    ]:
        """Get a child property by its index.

        Args:
            index: Zero-based index of the child property.

        Returns:
            The child property as the appropriate typed subclass.
        """
        stream = self._dyn_suite.GetNewStreamRefByIndex(self.property, index)
        return PropertyFactory.create_property(stream)

    def add_property(self, name: str) -> None:
        """Add a new child property stream by match name.

        Args:
            name: Match name of the property to add.
        """
        if self._dyn_suite.CanAddStream(self.property, name):
            self._dyn_suite.AddStream(self.property, name)

    def remove_property(self, name: str) -> None:
        """Remove a child property by match name.

        Args:
            name: Match name of the property to remove.
        """
        stream = self._dyn_suite.GetNewStreamRefByMatchname(self.property, name)
        if stream:
            self._dyn_suite.DeleteStream(stream)

    def remove_property_by_index(self, index: int) -> None:
        """Remove a child property by index.

        Args:
            index: Zero-based index of the property to remove.
        """
        stream = self._dyn_suite.GetNewStreamRefByIndex(self.property, index)
        if stream:
            self._dyn_suite.DeleteStream(stream)

    def num_keys(self) -> int:
        """Return the number of keyframes on this property.

        Returns:
            Keyframe count.

        Examples:
            >>> layer.opacity.num_keys()
            3
        """
        return PyFx.KeyframeSuite().GetStreamNumKFs(self.property)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        return self.name


class PropertyGroup(BaseProperty):
    """A group of properties (e.g. Transform, Effects, Masks).

    Supports iteration, indexing by int or match name, and list-like
    mutation (append, insert, remove, clear).

    Args:
        property: Raw stream reference pointer for the group.

    Examples:
        >>> transform = layer["ADBE Transform Group"]
        >>> for prop in transform:
        ...     print(prop.name)
        >>>
        >>> opacity = transform["ADBE Opacity"]
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def num_properties(self) -> int:
        """Return the number of child properties in this group.

        Returns:
            Child property count.
        """
        return self._dyn_suite.GetNumStreamsInGroup(self.property)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self) -> str:
        return self.name

    def __getitem__(self, key: Union[int, str]) -> Union[
        "BaseProperty",
        "PropertyGroup",
        "OneDProperty",
        "TwoDProperty",
        "ThreeDProperty",
        "ColorProperty",
        "MarkerProperty",
        "LayerIDProperty",
        "MaskIDProperty",
        "MaskOutlineProperty",
        "TextDocumentProperty",
    ]:
        """Get a child property by index or match name.

        Args:
            key: Integer index or string match name.

        Returns:
            The child property.

        Raises:
            TypeError: If key is neither int nor str.

        Examples:
            >>> group[0]
            OneDProperty(Anchor Point)
            >>> group["ADBE Opacity"]
            OneDProperty(Opacity)
        """
        if isinstance(key, int):
            return self.get_property_by_index(key)
        elif isinstance(key, str):
            return self.get_property(key)
        else:
            raise TypeError("Key must be an int or a str")

    def __iter__(self):
        for i in range(self.num_properties()):
            yield self.get_property_by_index(i)

    def __len__(self) -> int:
        return self.num_properties()

    def __contains__(
        self,
        item: Union[
            "BaseProperty",
            "PropertyGroup",
            "OneDProperty",
            "TwoDProperty",
            "ThreeDProperty",
            "ColorProperty",
            "MarkerProperty",
            "LayerIDProperty",
            "MaskIDProperty",
            "MaskOutlineProperty",
            "TextDocumentProperty",
        ],
    ) -> bool:
        for i in range(self.num_properties()):
            if self.get_property_by_index(i) == item:
                return True
        return False

    def append(
        self,
        item: Union[
            "BaseProperty",
            "PropertyGroup",
            "OneDProperty",
            "TwoDProperty",
            "ThreeDProperty",
            "ColorProperty",
            "MarkerProperty",
            "LayerIDProperty",
            "MaskIDProperty",
            "MaskOutlineProperty",
            "TextDocumentProperty",
        ],
    ) -> None:
        """Add a property to the end of this group.

        Args:
            item: The property to add (uses its name as match name).
        """
        self.add_property(item.name)

    def insert(
        self,
        index: int,
        item: Union[
            "BaseProperty",
            "PropertyGroup",
            "OneDProperty",
            "TwoDProperty",
            "ThreeDProperty",
            "ColorProperty",
            "MarkerProperty",
            "LayerIDProperty",
            "MaskIDProperty",
            "MaskOutlineProperty",
            "TextDocumentProperty",
        ],
    ) -> None:
        """Add a property at a specific index.

        Args:
            index: Target index position.
            item: The property to add.
        """
        self.add_property(item.name)
        self.reorder(index)

    def remove(
        self,
        item: Union[
            "BaseProperty",
            "PropertyGroup",
            "OneDProperty",
            "TwoDProperty",
            "ThreeDProperty",
            "ColorProperty",
            "MarkerProperty",
            "LayerIDProperty",
            "MaskIDProperty",
            "MaskOutlineProperty",
            "TextDocumentProperty",
        ],
    ) -> None:
        """Remove a property from this group.

        Args:
            item: The property to remove.
        """
        self.remove_property(item.name)

    def clear(self) -> None:
        """Remove all properties from this group."""
        for i in range(self.num_properties()):
            self.remove_property_by_index(i)

    def reverse(self) -> None:
        """Reverse the order of properties in this group."""
        for i in range(self.num_properties()):
            self.reorder(i)

    def sort(self, key=None, reverse=False) -> None:
        """Sort properties in this group."""
        for i in range(self.num_properties()):
            self.reorder(i)


class OneDProperty(BaseProperty):
    """A single-dimensional (scalar) property such as Opacity or Rotation.

    Supports bracket syntax for reading values at a given comp time.

    Args:
        property: Raw stream reference pointer.

    Examples:
        >>> opacity = layer.opacity
        >>> opacity.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        100.0
        >>>
        >>> # Bracket shorthand (reads at comp time, post-expression)
        >>> opacity[2.5]
        75.0
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> float:
        """Get the property value at a given time.

        Args:
            time_mode: Time interpretation mode (`CompTime` or `LayerTime`).
            time: Time in seconds.
            pre_expression: If `True`, return the value before expressions.

        Returns:
            The scalar value at the specified time.

        Examples:
            >>> layer.opacity.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
            100.0
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        return val.value()

    def set_value(self, value: float) -> None:
        """Set the static (non-keyframed) value of this property.

        Args:
            value: The new scalar value.

        Examples:
            >>> layer.opacity.set_value(50.0)
        """
        self._suite.SetStreamValue(
            self.property, PyFx.StreamValue2(self.property, value)
        )

    def __getitem__(self, time: float) -> float:
        return self.get_value(PyFx.LTimeMode.CompTime, time, False)

    def __setitem__(self, time: float, value: float) -> None:
        self.set_value(value)


class TwoDProperty(BaseProperty):
    """A two-dimensional property such as Position (2D) or Feather.

    Values are `(x, y)` tuples.

    Args:
        property: Raw stream reference pointer.

    Examples:
        >>> pos = layer.get_property(PyFx.LayerStream.POSITION)
        >>> pos.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        (960.0, 540.0)
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> tuple[float, float]:
        """Get the 2D value at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            An `(x, y)` tuple.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        two_d: PyFx.TwoDVal = val.value()
        return two_d.to_tuple()

    def set_value(self, value: tuple[float, float]) -> None:
        """Set the static 2D value.

        Args:
            value: An `(x, y)` tuple.
        """
        self._suite.SetStreamValue(
            self.property, PyFx.StreamValue2(self.property, value)
        )

    def __getitem__(self, time: float) -> tuple[float, float]:
        return self.get_value(PyFx.LTimeMode.CompTime, time, False)

    def __setitem__(self, time: float, value: tuple[float, float]) -> None:
        self.set_value(value)


class ThreeDProperty(BaseProperty):
    """A three-dimensional property such as Position (3D) or Scale.

    Values are `(x, y, z)` tuples.

    Args:
        property: Raw stream reference pointer.

    Examples:
        >>> layer.position.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        (960.0, 540.0, 0.0)
        >>>
        >>> layer.scale.set_value((50.0, 50.0, 50.0))
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> tuple[float, float, float]:
        """Get the 3D value at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            An `(x, y, z)` tuple.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        three_d_tuple = val.value()
        return three_d_tuple

    def set_value(self, value: tuple[float, float, float]) -> None:
        """Set the static 3D value.

        Args:
            value: An `(x, y, z)` tuple.
        """
        self._suite.SetStreamValue(
            self.property, PyFx.StreamValue2(self.property, value)
        )

    def __getitem__(self, time: float) -> tuple[float, float, float]:
        return self.get_value(PyFx.LTimeMode.CompTime, time, False)

    def __setitem__(
        self, time: float, value: tuple[float, float, float]
    ) -> None:
        self.set_value(value)


class ColorProperty(BaseProperty):
    """An RGBA color property.

    Values are `(r, g, b, a)` tuples with components in the 0.0-1.0 range.

    Args:
        property: Raw stream reference pointer.

    Examples:
        >>> light.color().get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        (1.0, 1.0, 1.0, 1.0)
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> tuple[float, float, float, float]:
        """Get the RGBA color value at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            An `(r, g, b, a)` tuple.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        color: PyFx.ColorVal = val.value()
        return color.to_tuple()

    def set_value(self, value: tuple[float, float, float, float]) -> None:
        """Set the static RGBA color value.

        Args:
            value: An `(r, g, b, a)` tuple (0.0-1.0 per channel).
        """
        self._suite.SetStreamValue(
            self.property, PyFx.StreamValue2(self.property, value)
        )


class MarkerProperty(BaseProperty):
    """A marker property stream on a layer or composition.

    Provides access to existing markers and allows adding new ones.

    Args:
        property: Raw stream reference pointer.

    Examples:
        >>> markers = layer.marker
        >>> marker = markers.add_marker(2.0)
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> "PyFx.Marker":
        """Get the marker at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            The marker object at the specified time.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        return PyFx.Marker(val.value())

    def add_marker(self, time: float) -> "PyFx.Marker":
        """Insert a new marker at the given comp time.

        Args:
            time: Time in seconds at which to place the marker.

        Returns:
            The newly created marker.

        Examples:
            >>> marker = layer.marker.add_marker(5.0)
        """
        idx = PyFx.KeyframeSuite().InsertKeyframe(
            self.property, PyFx.LTimeMode.CompTime, PyFx.Time(time)
        )
        marker = PyFx.MarkerSuite().getNewMarker()
        val = PyFx.StreamValue2(self.property, marker)
        PyFx.KeyframeSuite().SetKeyframeValue(self.property, idx, val)
        return PyFx.Marker(marker)

    def __getitem__(self, time: float) -> "PyFx.Marker":
        return self.get_value(PyFx.LTimeMode.CompTime, time, False)


class LayerIDProperty(BaseProperty):
    """A property that holds a layer ID reference.

    Args:
        property: Raw stream reference pointer.
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> int:
        """Get the referenced layer ID at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            The layer ID as an integer.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        return val.value()


class MaskIDProperty(BaseProperty):
    """A property that holds a mask ID reference.

    Args:
        property: Raw stream reference pointer.
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> int:
        """Get the referenced mask ID at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            The mask ID as an integer.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        return val.value()


class MaskOutlineProperty(BaseProperty):
    """A property representing a mask outline (path shape).

    Args:
        property: Raw stream reference pointer.
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> "PyFx.MaskOutline":
        """Get the mask outline at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            The mask outline object.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        return PyFx.MaskOutline(val.value())


class TextDocumentProperty(BaseProperty):
    """A property representing a text layer's source text document.

    Args:
        property: Raw stream reference pointer.

    Examples:
        >>> text_prop = layer.text
        >>> doc = text_prop.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
    """

    def __init__(self, property: PyFx.StreamRefPtr) -> None:
        super().__init__(property)

    def get_value(
        self, time_mode: PyFx.LTimeMode, time: float, pre_expression: bool
    ) -> "PyFx.TextDocument":
        """Get the text document at a given time.

        Args:
            time_mode: Time interpretation mode.
            time: Time in seconds.
            pre_expression: If `True`, return the pre-expression value.

        Returns:
            The text document object.
        """
        val = self._suite.GetNewStreamValue(
            self.property, time_mode, PyFx.Time(time), pre_expression
        )
        return PyFx.TextDocument(val.value())


class PropertyFactory:
    """Factory for creating typed property subclasses from raw stream pointers.

    Inspects the stream grouping type and data type at runtime to return
    the appropriate subclass (`PropertyGroup`, `OneDProperty`, etc.).
    """

    @staticmethod
    def create_property(
        property: PyFx.StreamRefPtr,
    ) -> Union[
        PropertyGroup,
        BaseProperty,
        OneDProperty,
        TwoDProperty,
        ThreeDProperty,
        ColorProperty,
        MarkerProperty,
        LayerIDProperty,
        MaskIDProperty,
        MaskOutlineProperty,
        TextDocumentProperty,
    ]:
        """Create a typed property wrapper from a raw stream pointer.

        Args:
            property: Raw stream reference pointer.

        Returns:
            The property wrapped as the appropriate subclass, or `None`
            if the stream type is unrecognized.
        """
        group_type = PyFx.DynamicStreamSuite().GetStreamGroupingType(property)
        if (
            group_type == PyFx.StreamGroupingType.INDEXED_GROUP
            or group_type == PyFx.StreamGroupingType.NAMED_GROUP
        ):
            return PropertyGroup(property)
        elif group_type == PyFx.StreamGroupingType.LEAF:
            stream_type = PyFx.StreamSuite().GetStreamType(property)
            if stream_type == PyFx.StreamType.OneD:
                return OneDProperty(property)
            elif (
                stream_type == PyFx.StreamType.TwoD
                or stream_type == PyFx.StreamType.TwoD_SPATIAL
            ):
                return TwoDProperty(property)
            elif (
                stream_type == PyFx.StreamType.ThreeD
                or stream_type == PyFx.StreamType.ThreeD_SPATIAL
            ):
                return ThreeDProperty(property)
            elif stream_type == PyFx.StreamType.COLOR:
                return ColorProperty(property)
            elif stream_type == PyFx.StreamType.MARKER:
                return MarkerProperty(property)
            elif stream_type == PyFx.StreamType.LAYER_ID:
                return LayerIDProperty(property)
            elif stream_type == PyFx.StreamType.MASK_ID:
                return MaskIDProperty(property)
            elif stream_type == PyFx.StreamType.MASK:
                return MaskOutlineProperty(property)
            elif stream_type == PyFx.StreamType.TEXT_DOCUMENT:
                return TextDocumentProperty(property)
            else:
                return BaseProperty(property)
        return None


class Layer(PropertyGroup):
    """Base class for all After Effects layers.

    Extends `PropertyGroup`, so a layer is itself a traversable property
    tree. Provides access to transform properties, timing, flags,
    parenting, effects, and layer-level operations.

    Args:
        layer: Raw layer pointer from the AE SDK.

    Examples:
        >>> layer = Layer.active_layer()
        >>> print(layer.name, layer.index, layer.type)
        >>>
        >>> # Access transform properties
        >>> pos = layer.position.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        >>> print(pos)
        (960.0, 540.0, 0.0)
    """

    _Lsuite = PyFx.LayerSuite()

    def __init__(self, layer: PyFx.LayerPtr) -> None:
        super().__init__(self._dyn_suite.GetNewStreamRefForLayer(layer))
        self.layer = layer

    @staticmethod
    def active_layer() -> Union[
        "Layer",
        "AVLayer",
        "CameraLayer",
        "LightLayer",
        "TextLayer",
        "VectorLayer",
        None,
    ]:
        """Return the currently active (selected) layer.

        Returns:
            The active layer as the appropriate typed subclass, or `None`
            if no layer is selected.

        Examples:
            >>> layer = Layer.active_layer()
            >>> if layer:
            ...     print(layer.name)
        """
        layer_ptr = PyFx.LayerSuite().GetActiveLayer()
        if layer_ptr:
            return LayerFactory.create_layer(layer_ptr)

    @property
    def name(self) -> str:
        """str: Display name of the layer."""
        return self._Lsuite.GetLayerName(self.layer)

    @name.setter
    def name(self, value: str) -> None:
        self._Lsuite.SetLayerName(self.layer, value)

    @property
    def index(self) -> int:
        """int: Zero-based index of the layer in its parent comp."""
        return self._Lsuite.GetLayerIndex(self.layer)

    @index.setter
    def index(self, value: int) -> None:
        self._Lsuite.ReorderLayer(self.layer, value)

    @property
    def source_item(self) -> Item:
        """Item: The project item that is this layer's source."""
        return ItemFactory.create_item(
            self._Lsuite.GetLayerSourceItem(self.layer)
        )

    @property
    def parent_comp(self) -> CompItem:
        """CompItem: The composition this layer belongs to."""
        return CompItem(self._Lsuite.GetLayerParentComp(self.layer))

    @property
    def quality(self) -> PyFx.LayerQual:
        """PyFx.LayerQual: Render quality setting for this layer."""
        return self._Lsuite.GetLayerQuality(self.layer)

    @quality.setter
    def quality(self, value: PyFx.LayerQual) -> None:
        self._Lsuite.SetLayerQuality(self.layer, value)

    @property
    def video_active(self) -> bool:
        """bool: Whether the layer's video (eye icon) is enabled."""
        return (
            self._Lsuite.GetLayerFlags(self.layer) & PyFx.LayerFlag.VIDEO_ACTIVE
        )

    @property
    def audio_active(self) -> bool:
        """bool: Whether the layer's audio is enabled."""
        return (
            self._Lsuite.GetLayerFlags(self.layer) & PyFx.LayerFlag.AUDIO_ACTIVE
        )

    @property
    def current_time(self) -> float:
        """float: Current time of the layer in seconds."""
        return self._Lsuite.GetLayerCurrentTime(self.layer)

    @property
    def duration(self) -> float:
        """float: Duration of the layer in seconds."""
        return self._Lsuite.GetLayerDuration(self.layer)

    @property
    def offset(self) -> float:
        """float: Layer start time offset in seconds."""
        return self._Lsuite.GetLayerOffset(self.layer)

    @offset.setter
    def offset(self, value: float) -> None:
        self._Lsuite.SetLayerOffset(self.layer, value)

    @property
    def in_point(self) -> float:
        """float: Layer in-point in seconds."""
        return self._Lsuite.GetLayerInPoint(self.layer)

    @in_point.setter
    def in_point(self, value: float) -> None:
        self._Lsuite.SetLayerInPointAndDuration(
            self.layer, value, self.duration
        )

    @property
    def stretch(self) -> float:
        """float: Time stretch factor."""
        return self._Lsuite.GetLayerStretch(self.layer)

    @stretch.setter
    def stretch(self, value: float) -> None:
        self._Lsuite.SetLayerStretch(self.layer, value)

    @property
    def flag(self) -> PyFx.LayerFlag:
        """PyFx.LayerFlag: Layer flags bitmask."""
        return self._Lsuite.GetLayerFlags(self.layer)

    @flag.setter
    def flag(self, value: PyFx.LayerFlag) -> None:
        self._Lsuite.SetLayerFlag(self.layer, value)

    @property
    def is_3d(self) -> bool:
        """bool: Whether this is a 3D layer."""
        return self._Lsuite.IsLayer3D(self.layer)

    @property
    def is_2d(self) -> bool:
        """bool: Whether this is a 2D layer."""
        return not self.is_3d()

    @property
    def parent(self) -> "Layer":
        """Layer: The parent layer (for parenting/pick-whip)."""
        return LayerFactory.create_layer(
            self._Lsuite.GetLayerParent(self.layer)
        )

    @parent.setter
    def parent(self, value: "Layer") -> None:
        self._Lsuite.SetLayerParent(self.layer, value.layer)

    @property
    def sampling_quality(self) -> PyFx.LayerSamplingQual:
        """PyFx.LayerSamplingQual: Sampling quality (bilinear/bicubic)."""
        return self._Lsuite.GetLayerSamplingQuality(self.layer)

    @sampling_quality.setter
    def sampling_quality(self, value: PyFx.LayerSamplingQual) -> None:
        self._Lsuite.SetLayerSamplingQuality(self.layer, value)

    def duplicate(self) -> "Layer":
        """Duplicate this layer within the same composition.

        Returns:
            The duplicated layer.

        Examples:
            >>> copy = layer.duplicate()
            >>> copy.name = "Layer Copy"
        """
        return LayerFactory.create_layer(
            self._Lsuite.DuplicateLayer(self.layer)
        )

    def delete(self) -> None:
        """Delete this layer from its composition."""
        self._Lsuite.DeleteLayer(self.layer)

    def num_effects(self) -> int:
        """Return the number of effects applied to this layer.

        Returns:
            Effect count.
        """
        return PyFx.EffectSuite().getLayerNumEffects(self.layer)

    def get_property(self, stream: PyFx.LayerStream) -> Union[
        BaseProperty,
        OneDProperty,
        TwoDProperty,
        ThreeDProperty,
        ColorProperty,
        MarkerProperty,
        LayerIDProperty,
        MaskIDProperty,
        MaskOutlineProperty,
        TextDocumentProperty,
    ]:
        """Get a built-in layer property by its stream constant.

        Args:
            stream: A `PyFx.LayerStream` enum value.

        Returns:
            The property as the appropriate typed subclass.

        Examples:
            >>> opacity = layer.get_property(PyFx.LayerStream.OPACITY)
            >>> opacity.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
            100.0
        """
        return PropertyFactory.create_property(
            self._suite.GetNewLayerStream(self.layer, stream)
        )

    @property
    def anchor_point(self) -> ThreeDProperty:
        """ThreeDProperty: Anchor point (pivot) of the layer."""
        return self.get_property(PyFx.LayerStream.ANCHORPOINT)

    @property
    def position(self) -> ThreeDProperty:
        """ThreeDProperty: Position of the layer."""
        return self.get_property(PyFx.LayerStream.POSITION)

    @property
    def rotation(self) -> ThreeDProperty:
        """ThreeDProperty: Rotation of the layer."""
        return self.get_property(PyFx.LayerStream.ROTATION)

    @property
    def marker(self) -> MarkerProperty:
        """MarkerProperty: Layer markers."""
        return self.get_property(PyFx.LayerStream.MARKER)

    @property
    def scale(self) -> ThreeDProperty:
        """ThreeDProperty: Scale of the layer (percentage)."""
        return self.get_property(PyFx.LayerStream.SCALE)

    @property
    def opacity(self) -> OneDProperty:
        """OneDProperty: Opacity of the layer (0-100)."""
        return self.get_property(PyFx.LayerStream.OPACITY)

    @property
    def rotation_x(self) -> OneDProperty:
        """OneDProperty: X-axis rotation (3D layers only)."""
        return self.get_property(PyFx.LayerStream.ROTATE_X)

    @property
    def rotation_y(self) -> OneDProperty:
        """OneDProperty: Y-axis rotation (3D layers only)."""
        return self.get_property(PyFx.LayerStream.ROTATE_Y)

    @property
    def rotation_z(self) -> OneDProperty:
        """OneDProperty: Z-axis rotation."""
        return self.get_property(PyFx.LayerStream.ROTATE_Z)

    @property
    def text(self) -> TextDocumentProperty:
        """TextDocumentProperty: Source text property (text layers only)."""
        return self.get_property(PyFx.LayerStream.TEXT)

    @property
    def type(self) -> PyFx.ObjectType:
        """PyFx.ObjectType: Object type (`AV`, `CAMERA`, `LIGHT`, `TEXT`, `VECTOR`)."""
        return self._Lsuite.GetLayerObjectType(self.layer)

    def copy_to_comp(self, comp: CompItem) -> "Layer":
        """Copy this layer into another composition.

        Args:
            comp: Target composition.

        Returns:
            The new layer in the target comp.

        Examples:
            >>> new_layer = layer.copy_to_comp(other_comp)
        """
        if self._Lsuite.IsAddLayerValid(self.source_item.item, comp.comp):
            return LayerFactory.create_layer(
                self._Lsuite.AddLayer(self.source_item.item, comp.comp)
            )


class AVLayer(Layer):
    """An audio/video layer (footage, solid, precomp, etc.).

    Provides access to 3D material properties such as shadows, lighting
    coefficients, reflections, and extrusion settings.

    Args:
        layer: Raw layer pointer.

    Examples:
        >>> layer = comp.layers[0]
        >>> isinstance(layer, AVLayer)
        True
        >>> layer.casts_shadows().get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        1.0
    """

    def __init__(self, layer: PyFx.LayerPtr) -> None:
        super().__init__(layer)

    def getObjectType(self) -> PyFx.ObjectType:
        """Return the object type constant for AV layers."""
        return PyFx.ObjectType.AV

    def casts_shadows(self) -> OneDProperty:
        """OneDProperty: Whether the layer casts shadows (3D only)."""
        return self.get_property(PyFx.LayerStream.CASTS_SHADOWS)

    def accepts_lights(self) -> OneDProperty:
        """OneDProperty: Whether the layer accepts lights (3D only)."""
        return self.get_property(PyFx.LayerStream.ACCEPTS_LIGHTS)

    def ambient_coeff(self) -> OneDProperty:
        """OneDProperty: Ambient light coefficient (3D material)."""
        return self.get_property(PyFx.LayerStream.AMBIENT_COEFF)

    def diffuse_coeff(self) -> OneDProperty:
        """OneDProperty: Diffuse light coefficient (3D material)."""
        return self.get_property(PyFx.LayerStream.DIFFUSE_COEFF)

    def specular_intensity(self) -> OneDProperty:
        """OneDProperty: Specular highlight intensity (3D material)."""
        return self.get_property(PyFx.LayerStream.SPECULAR_INTENSITY)

    def specular_shininess(self) -> OneDProperty:
        """OneDProperty: Specular highlight shininess (3D material)."""
        return self.get_property(PyFx.LayerStream.SPECULAR_SHININESS)

    def light_transmission(self) -> OneDProperty:
        """OneDProperty: Light transmission amount (3D material)."""
        return self.get_property(PyFx.LayerStream.LIGHT_TRANSMISSION)

    def metal(self) -> OneDProperty:
        """OneDProperty: Metal appearance amount (3D material)."""
        return self.get_property(PyFx.LayerStream.METAL)

    def reflection_intensity(self) -> OneDProperty:
        """OneDProperty: Environment reflection intensity (3D material)."""
        return self.get_property(PyFx.LayerStream.REFLECTION_INTENSITY)

    def reflection_sharpness(self) -> OneDProperty:
        """OneDProperty: Environment reflection sharpness (3D material)."""
        return self.get_property(PyFx.LayerStream.REFLECTION_SHARPNESS)

    def reflection_rolloff(self) -> OneDProperty:
        """OneDProperty: Environment reflection rolloff (3D material)."""
        return self.get_property(PyFx.LayerStream.REFLECTION_ROLLOFF)

    def transparency_coeff(self) -> OneDProperty:
        """OneDProperty: Transparency coefficient (3D material)."""
        return self.get_property(PyFx.LayerStream.TRANSPARENCY_COEFF)

    def transparency_rolloff(self) -> OneDProperty:
        """OneDProperty: Transparency rolloff (3D material)."""
        return self.get_property(PyFx.LayerStream.TRANSPARENCY_ROLLOFF)

    def index_of_refraction(self) -> OneDProperty:
        """OneDProperty: Index of refraction (3D material)."""
        return self.get_property(PyFx.LayerStream.INDEX_OF_REFRACTION)

    def extrusion_bevel_style(self) -> OneDProperty:
        """OneDProperty: Bevel style for 3D extrusion."""
        return self.get_property(PyFx.LayerStream.EXTRUSION_BEVEL_STYLE)

    def extrusion_bevel_direction(self) -> OneDProperty:
        """OneDProperty: Bevel direction for 3D extrusion."""
        return self.get_property(PyFx.LayerStream.EXTRUSION_BEVEL_DIRECTION)

    def extrusion_bevel_depth(self) -> OneDProperty:
        """OneDProperty: Bevel depth for 3D extrusion."""
        return self.get_property(PyFx.LayerStream.EXTRUSION_BEVEL_DEPTH)

    def extrusion_hole_bevel_depth(self) -> OneDProperty:
        """OneDProperty: Hole bevel depth for 3D extrusion."""
        return self.get_property(PyFx.LayerStream.EXTRUSION_HOLE_BEVEL_DEPTH)

    def extrusion_depth(self) -> OneDProperty:
        """OneDProperty: Extrusion depth for 3D layers."""
        return self.get_property(PyFx.LayerStream.EXTRUSION_DEPTH)

    def plane_curvature(self) -> OneDProperty:
        """OneDProperty: Plane curvature for 3D layers."""
        return self.get_property(PyFx.LayerStream.PLANE_CURVATURE)

    def plane_subdivision(self) -> OneDProperty:
        """OneDProperty: Plane subdivision for 3D layers."""
        return self.get_property(PyFx.LayerStream.PLANE_SUBDIVISION)


class CameraLayer(Layer):
    """A camera layer providing 3D camera controls.

    Exposes zoom, depth-of-field, aperture, and iris properties.

    Args:
        layer: Raw layer pointer.

    Examples:
        >>> camera = comp.layers.add_camera("Main Camera", (960.0, 540.0))
        >>> camera.zoom().get_value(PyFx.LTimeMode.CompTime, 0.0, False)
    """

    def __init__(self, layer: PyFx.LayerPtr) -> None:
        super().__init__(layer)

    def getObjectType(self) -> PyFx.ObjectType:
        """Return the object type constant for camera layers."""
        return PyFx.ObjectType.CAMERA

    def zoom(self) -> OneDProperty:
        """OneDProperty: Camera zoom value."""
        return self.get_property(PyFx.LayerStream.ZOOM)

    def depth_of_field(self) -> OneDProperty:
        """OneDProperty: Depth of field toggle."""
        return self.get_property(PyFx.LayerStream.DEPTH_OF_FIELD)

    def focus_distance(self) -> OneDProperty:
        """OneDProperty: Focus distance in pixels."""
        return self.get_property(PyFx.LayerStream.FOCUS_DISTANCE)

    def aperture(self) -> OneDProperty:
        """OneDProperty: Lens aperture value."""
        return self.get_property(PyFx.LayerStream.APERTURE)

    def blur_level(self) -> OneDProperty:
        """OneDProperty: Blur level percentage."""
        return self.get_property(PyFx.LayerStream.BLUR_LEVEL)

    def iris_shape(self) -> OneDProperty:
        """OneDProperty: Iris shape (number of blades)."""
        return self.get_property(PyFx.LayerStream.IRIS_SHAPE)

    def iris_rotation(self) -> OneDProperty:
        """OneDProperty: Iris rotation in degrees."""
        return self.get_property(PyFx.LayerStream.IRIS_ROTATION)

    def iris_roundness(self) -> OneDProperty:
        """OneDProperty: Iris roundness percentage."""
        return self.get_property(PyFx.LayerStream.IRIS_ROUNDNESS)

    def iris_aspect_ratio(self) -> OneDProperty:
        """OneDProperty: Iris aspect ratio."""
        return self.get_property(PyFx.LayerStream.IRIS_ASPECT_RATIO)

    def iris_diffraction_fringe(self) -> OneDProperty:
        """OneDProperty: Iris diffraction fringe amount."""
        return self.get_property(PyFx.LayerStream.IRIS_DIFFRACTION_FRINGE)

    def iris_highlight_gain(self) -> OneDProperty:
        """OneDProperty: Iris highlight gain."""
        return self.get_property(PyFx.LayerStream.IRIS_HIGHLIGHT_GAIN)

    def iris_highlight_threshold(self) -> OneDProperty:
        """OneDProperty: Iris highlight threshold."""
        return self.get_property(PyFx.LayerStream.IRIS_HIGHLIGHT_THRESHOLD)

    def iris_highlight_saturation(self) -> OneDProperty:
        """OneDProperty: Iris highlight saturation."""
        return self.get_property(PyFx.LayerStream.IRIS_HIGHLIGHT_SATURATION)


class LightLayer(Layer):
    """A light layer providing 3D lighting controls.

    Exposes color, intensity, cone, shadow, and falloff properties.

    Args:
        layer: Raw layer pointer.

    Examples:
        >>> light = comp.layers.add_light("Key Light", (960.0, 540.0))
        >>> light.intensity().get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        100.0
    """

    def __init__(self, layer: PyFx.LayerPtr) -> None:
        super().__init__(layer)

    def getObjectType(self) -> PyFx.ObjectType:
        """Return the object type constant for light layers."""
        return PyFx.ObjectType.LIGHT

    def color(self) -> ColorProperty:
        """ColorProperty: Light color (RGBA)."""
        return self.get_property(PyFx.LayerStream.COLOR)

    def intensity(self) -> OneDProperty:
        """OneDProperty: Light intensity percentage."""
        return self.get_property(PyFx.LayerStream.INTENSITY)

    def cone_angle(self) -> OneDProperty:
        """OneDProperty: Spot light cone angle in degrees."""
        return self.get_property(PyFx.LayerStream.CONE_ANGLE)

    def cone_feather(self) -> OneDProperty:
        """OneDProperty: Spot light cone feather percentage."""
        return self.get_property(PyFx.LayerStream.CONE_FEATHER)

    def shadow_darkness(self) -> OneDProperty:
        """OneDProperty: Shadow darkness percentage."""
        return self.get_property(PyFx.LayerStream.SHADOW_DARKNESS)

    def shadow_diffusion(self) -> OneDProperty:
        """OneDProperty: Shadow diffusion amount."""
        return self.get_property(PyFx.LayerStream.SHADOW_DIFFUSION)

    def light_falloff_type(self) -> OneDProperty:
        """OneDProperty: Light falloff type."""
        return self.get_property(PyFx.LayerStream.LIGHT_FALLOFF_TYPE)

    def light_falloff_start(self) -> OneDProperty:
        """OneDProperty: Distance at which falloff begins."""
        return self.get_property(PyFx.LayerStream.LIGHT_FALLOFF_START)

    def light_falloff_distance(self) -> OneDProperty:
        """OneDProperty: Distance over which light falls off."""
        return self.get_property(PyFx.LayerStream.LIGHT_FALLOFF_DISTANCE)


class TextLayer(Layer):
    """A text layer.

    Inherits all `Layer` properties. Access the source text via the
    `text` property.

    Args:
        layer: Raw layer pointer.

    Examples:
        >>> text_layer = comp.layers[0]
        >>> doc = text_layer.text.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
    """

    def __init__(self, layer: PyFx.LayerPtr) -> None:
        super().__init__(layer)

    def getObjectType(self) -> PyFx.ObjectType:
        """Return the object type constant for text layers."""
        return PyFx.ObjectType.TEXT


class VectorLayer(Layer):
    """A shape (vector) layer.

    Inherits all `Layer` properties.

    Args:
        layer: Raw layer pointer.
    """

    def __init__(self, layer: PyFx.LayerPtr) -> None:
        super().__init__(layer)

    def getObjectType(self) -> PyFx.ObjectType:
        """Return the object type constant for vector layers."""
        return PyFx.ObjectType.VECTOR


class LayerFactory:
    """Factory for creating typed Layer subclasses from raw pointers.

    Inspects the layer object type at runtime and returns the appropriate
    subclass (`AVLayer`, `CameraLayer`, `LightLayer`, `TextLayer`,
    `VectorLayer`, or `Layer`).
    """

    @staticmethod
    def create_layer(
        layer: PyFx.LayerPtr,
    ) -> Union[Layer, AVLayer, CameraLayer, LightLayer, TextLayer, VectorLayer]:
        """Create a typed Layer wrapper from a raw layer pointer.

        Args:
            layer: Raw layer pointer from the AE SDK.

        Returns:
            The layer wrapped as the appropriate subclass.
        """
        type = PyFx.LayerSuite().GetLayerObjectType(layer)
        if type == PyFx.ObjectType.AV:
            return AVLayer(layer)
        elif type == PyFx.ObjectType.CAMERA:
            return CameraLayer(layer)
        elif type == PyFx.ObjectType.LIGHT:
            return LightLayer(layer)
        elif type == PyFx.ObjectType.TEXT:
            return TextLayer(layer)
        elif type == PyFx.ObjectType.VECTOR:
            return VectorLayer(layer)
        else:
            return Layer(layer)


class LayerCollection(list):
    """Ordered collection of layers within a composition.

    Extends `list` with name-based indexing, layer creation helpers
    (null, solid, camera, light), and criteria-based search. Mutating
    the collection also updates the After Effects composition.

    Examples:
        >>> comp = CompItem.most_recent()
        >>> layers = comp.layers
        >>> print(len(layers))
        >>>
        >>> # Access by name
        >>> bg = layers["Background"]
        >>>
        >>> # Create layers
        >>> null = layers.add_null("Controller")
        >>> solid = layers.add_solid("BG", (0.0, 0.0, 0.0, 1.0), 1920, 1080)
    """

    _base_comp: PyFx.CompPtr = None

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def create(cls, base_comp: PyFx.CompPtr) -> "LayerCollection":
        """Build a collection from all layers in a composition.

        Args:
            base_comp: Comp pointer to enumerate layers from.

        Returns:
            Collection populated with typed layer wrappers.
        """
        collection = cls()
        cls._base_comp = base_comp
        suite = PyFx.LayerSuite()
        num_layers = suite.GetCompNumLayers(base_comp)
        for i in range(num_layers):
            layer_ptr = suite.GetCompLayerByIndex(base_comp, i)
            layer = LayerFactory.create_layer(layer_ptr)
            collection.append(layer)
        return collection

    def add_null(self, name: str, duration: float = 0.0) -> Layer:
        """Create a null object layer in the composition.

        Args:
            name: Display name for the null.
            duration: Duration in seconds (0 uses comp duration).

        Returns:
            The newly created null layer.

        Examples:
            >>> null = comp.layers.add_null("Controller")
        """
        if duration < 0:
            duration = self._suite.GetItemDuration(
                PyFx.CompSuite().GetItemFromComp(self._base_comp)
            )
        null = PyFx.CompSuite().CreateNullInComp(
            self._base_comp, name, duration
        )
        layer = LayerFactory.create_layer(null)
        super().append(layer)
        return layer

    def add_solid(
        self,
        name: str,
        color: tuple[float, float, float, float],
        width: int,
        height: int,
        duration: float = 0.0,
    ) -> Layer:
        """Create a solid layer in the composition.

        Args:
            name: Display name for the solid.
            color: RGBA color tuple (0.0-1.0 per channel).
            width: Width in pixels.
            height: Height in pixels.
            duration: Duration in seconds (0 uses comp duration).

        Returns:
            The newly created solid layer.

        Examples:
            >>> solid = comp.layers.add_solid("BG", (0.0, 0.0, 0.0, 1.0), 1920, 1080)
        """
        if duration < 0:
            duration = self._suite.GetItemDuration(
                PyFx.CompSuite().GetItemFromComp(self._base_comp)
            )
        solid = PyFx.CompSuite().CreateSolidInComp(
            self._base_comp,
            name,
            width,
            height,
            PyFx.ColorVal(color),
            PyFx.Time(duration),
        )
        layer = LayerFactory.create_layer(solid)
        super().append(layer)
        return layer

    def add_camera(
        self, name: str, center_point: tuple[float, float] = (0.0, 0.0)
    ) -> Layer:
        """Create a camera layer in the composition.

        Args:
            name: Display name for the camera.
            center_point: Initial center point as `(x, y)`.

        Returns:
            The newly created camera layer.

        Examples:
            >>> camera = comp.layers.add_camera("Main Camera", (960.0, 540.0))
        """
        camera = PyFx.CompSuite().CreateCameraInComp(
            self._base_comp,
            name,
            PyFx.FloatPoint(center_point[0], center_point[1]),
        )
        layer = LayerFactory.create_layer(camera)
        super().append(layer)
        return layer

    def add_light(
        self, name: str, center_point: tuple[float, float] = (0.0, 0.0)
    ) -> Layer:
        """Create a light layer in the composition.

        Args:
            name: Display name for the light.
            center_point: Initial center point as `(x, y)`.

        Returns:
            The newly created light layer.

        Examples:
            >>> light = comp.layers.add_light("Key Light", (960.0, 540.0))
        """
        light = PyFx.CompSuite().CreateLightInComp(
            self._base_comp,
            name,
            PyFx.FloatPoint(center_point[0], center_point[1]),
        )
        layer = LayerFactory.create_layer(light)
        super().append(layer)
        return layer

    def extend(self, layers: "LayerCollection") -> None:
        """Add all layers from another collection into this comp.

        Args:
            layers: Source layer collection to copy from.
        """
        for layer in layers:
            self.append(layer.source_item)
            super().append(layer)

    def insert(self, index: int, layer: Layer) -> None:
        """Insert a layer at a specific index in the comp.

        Args:
            index: Target index position.
            layer: The layer to insert.
        """
        if self._suite.IsAddLayerValid(layer.source_item, self._base_comp):
            new_layer = Layer(
                self._suite.AddLayer(layer.source_item, self._base_comp)
            )
            self._suite.ReorderLayer(new_layer, index)
            super().insert(index, new_layer)

    def remove(self, layer: Layer) -> None:
        """Delete a layer from the composition and this collection.

        Args:
            layer: The layer to delete.
        """
        self._suite.DeleteLayer(layer.layer)
        super().remove(layer)

    def clear(self) -> None:
        """Delete all layers from the composition."""
        for layer in self:
            self._suite.DeleteLayer(layer.layer)
        super().clear()

    def pop(self, index: int) -> Layer:
        """Remove and delete the layer at the given index.

        Args:
            index: Index of the layer to remove.

        Returns:
            The removed layer.
        """
        layer = super().pop(index)
        self._suite.DeleteLayer(layer.layer)
        return layer

    def reverse(self) -> None:
        """Reverse the stacking order of layers in the comp."""
        for i, layer in enumerate(self):
            self._suite.ReorderLayer(layer.layer, len(self) - i)
        super().reverse()

    def sort(self, key=None, reverse=False) -> None:
        """Sort layers and update the comp stacking order."""
        super().sort(key, reverse)
        for i, layer in enumerate(self):
            self._suite.ReorderLayer(layer.layer, i)

    def __getitem__(self, key: any) -> Layer:
        """Get a layer by integer index or by name.

        Args:
            key: Integer index or string name.

        Returns:
            The matching layer.

        Raises:
            KeyError: If no layer with the given name exists.

        Examples:
            >>> layers[0]
            AVLayer(Background)
            >>> layers["Background"]
            AVLayer(Background)
        """
        if isinstance(key, int):
            return super().__getitem__(key)
        for layer in self:
            if self._suite.GetLayerName(layer.layer) == key:
                return layer
        raise KeyError(f"Layer with name '{key}' not found")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({super().__str__()})"

    def __len__(self) -> int:
        return super().__len__()

    def __iter__(self) -> Iterator:
        return super().__iter__()

    def get_layer(self, **criteria) -> Layer:
        """Retrieve the first layer matching all criteria.

        Supports nested attributes via dot notation.

        Args:
            **criteria: Key-value pairs where keys are attribute names
                (or dot-separated paths) and values are expected values.

        Returns:
            The first layer matching all criteria.

        Raises:
            KeyError: If no matching layer is found.

        Examples:
            >>> layers.get_layer(name="Background")
            AVLayer(Background)
            >>>
            >>> layers.get_layer(type=PyFx.ObjectType.CAMERA)
            CameraLayer(Main Camera)
        """

        def match(layer: Layer, attr_path: str, value: Any) -> bool:
            attr = operator.attrgetter(attr_path)
            try:
                return attr(layer) == value
            except AttributeError:
                return False

        for layer in self:
            if all(match(layer, key, val) for key, val in criteria.items()):
                return layer

        raise KeyError(f"Layer with criteria '{criteria}' not found")

    def get_layers(self, **criteria) -> "LayerCollection":
        """Retrieve all layers matching the given criteria.

        Supports nested attributes via dot notation.

        Args:
            **criteria: Key-value pairs where keys are attribute names
                (or dot-separated paths) and values are expected values.

        Returns:
            A new collection containing only the matching layers.

        Examples:
            >>> cameras = layers.get_layers(type=PyFx.ObjectType.CAMERA)
            >>> print(len(cameras))
        """

        def match(layer: Layer, attr_path: str, value: Any) -> bool:
            attr = operator.attrgetter(attr_path)
            try:
                return attr(layer) == value
            except AttributeError:
                return False

        layers = LayerCollection()
        for layer in self:
            if all(match(layer, key, val) for key, val in criteria.items()):
                layers.append(layer)
        return layers


class UndoGroup:
    """Context manager that wraps operations in a single AE undo step.

    All changes made inside the `with` block appear as one undoable
    action in Edit > Undo.

    Args:
        name: Display name shown in the Edit > Undo menu.

    Examples:
        >>> with UndoGroup("Move Layers"):
        ...     layer.position.set_value((100.0, 200.0, 0.0))
        ...     layer.opacity.set_value(50.0)
    """

    def __init__(self, name: str) -> None:
        self.name = name
        PyFx.UtilitySuite().startUndoGroup(name)

    def __enter__(self) -> "UndoGroup":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        PyFx.UtilitySuite().endUndoGroup()


class QuietErrors:
    """Context manager that suppresses AE error dialogs.

    Useful for batch operations where you want to handle errors in
    Python rather than showing modal AE dialogs.

    Examples:
        >>> with QuietErrors():
        ...     # Operations that might trigger AE error popups
        ...     footage.replace_from_path("C:/missing_file.exr")
    """

    def __init__(self) -> None:
        PyFx.UtilitySuite().startQuietErrors()

    def __enter__(self) -> "QuietErrors":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        PyFx.UtilitySuite().endQuietErrors()


def undo_group(name: str):
    """Decorator that wraps a function in an AE undo group.

    Args:
        name: Display name shown in the Edit > Undo menu.

    Returns:
        A decorator that wraps the target function.

    Examples:
        >>> @undo_group("Set Layer Properties")
        ... def setup_layer(layer):
        ...     layer.position.set_value((960.0, 540.0, 0.0))
        ...     layer.opacity.set_value(100.0)
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            with UndoGroup(name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def quiet_errors(func):
    """Decorator that suppresses AE error dialogs during function execution.

    Examples:
        >>> @quiet_errors
        ... def batch_replace(items, new_path):
        ...     for item in items:
        ...         item.replace_from_path(new_path)
    """

    def wrapper(*args, **kwargs):
        with QuietErrors():
            return func(*args, **kwargs)

    return wrapper


class Effect:
    """An effect applied to a layer.

    Provides access to effect parameters and metadata. Effects are
    applied by match name or display name via `Effect.apply()`.

    Args:
        effect: Raw effect reference pointer.

    Examples:
        >>> blur = Effect.apply(layer, "ADBE Gaussian Blur 2")
        >>> print(blur.name, blur.category)
        >>>
        >>> # Access effect parameters
        >>> blurriness = blur.param("Blurriness")
        >>> blurriness.set_value(10.0)
    """

    def __init__(self, effect: PyFx.EffectRefPtr) -> None:
        self.effect = effect

    @classmethod
    def apply(cls, layer: Layer, match_name: str) -> "Effect":
        """Apply an effect to a layer by match name or display name.

        Searches all installed effects for a matching name and applies
        the first match to the given layer.

        Args:
            layer: The layer to apply the effect to.
            match_name: Effect match name (e.g. `ADBE Gaussian Blur 2`)
                or display name (e.g. `Gaussian Blur`).

        Returns:
            The applied effect instance, or `None` if no match was found.

        Examples:
            >>> blur = Effect.apply(layer, "ADBE Gaussian Blur 2")
            >>> glow = Effect.apply(layer, "Glow")
        """
        # check name and match name
        current_key = 0
        num_effects = PyFx.EffectSuite().getNumInstalledEffects()
        #  App().report_info(f"num_effects: {num_effects}")
        first_eff = PyFx.EffectSuite().getNextInstalledEffect(current_key)
        current_key = first_eff
        for i in range(num_effects):
            current_match_name = PyFx.EffectSuite().getEffectMatchName(
                current_key
            )
            current_name = PyFx.EffectSuite().getEffectName(current_key)
            if current_match_name == match_name or current_name == match_name:
                effect_ref = PyFx.EffectSuite().applyEffect(
                    layer.layer, current_key
                )
                return Effect(effect_ref)
            current_key = PyFx.EffectSuite().getNextInstalledEffect(current_key)
        return None

    @property
    def name(self) -> str:
        """str: Display name of the effect."""
        return PyFx.EffectSuite().getEffectName(self.effect)

    @property
    def match_name(self) -> str:
        """str: Internal match name of the effect."""
        return PyFx.EffectSuite().getEffectMatchName(self.effect)

    @property
    def category(self) -> str:
        """str: Effect category (e.g. `Blur & Sharpen`)."""
        return PyFx.EffectSuite().getEffectCategory(self.effect)

    def param(self, name: Union[int, str]) -> Union[
        BaseProperty,
        OneDProperty,
        TwoDProperty,
        ThreeDProperty,
        ColorProperty,
        PropertyGroup,
    ]:
        """Get an effect parameter by index, display name, or match name.

        Args:
            name: Integer index, display name, or match name.

        Returns:
            The parameter as the appropriate typed property, or `None`
            if no matching parameter is found.

        Examples:
            >>> blur.param(0)
            OneDProperty(Blurriness)
            >>> blur.param("Blurriness")
            OneDProperty(Blurriness)
        """
        if isinstance(name, int):
            stream = self._suite.GetNewEffectStreamByIndex(self.effect, name)
            return PropertyFactory.create_property(stream)
        else:
            for i in range(self._suite.GetEffectNumParamStreams(self.effect)):
                current_name = self._suite.GetStreamName(
                    self._suite.GetNewEffectStreamByIndex(self.effect, i), True
                )
                current_match_name = self._dyn_suite.GetMatchname(
                    self._suite.GetNewEffectStreamByIndex(self.effect, i)
                )
                if current_name == name or current_match_name == name:
                    stream = self._suite.GetNewEffectStreamByIndex(
                        self.effect, i
                    )
                    return PropertyFactory.create_property(stream)
            return None

    def duplicate(self) -> "Effect":
        """Duplicate this effect on the same layer.

        Returns:
            The duplicated effect.

        Examples:
            >>> blur_copy = blur.duplicate()
        """
        effect_ref = PyFx.EffectSuite().duplicateEffect(self.effect)
        return Effect(effect_ref)


class Mask:
    """A mask on a layer.

    Provides access to mask path (outline), mode, opacity, feather,
    expansion, color, lock state, and RotoBezier mode.

    Args:
        mask: Raw mask reference pointer.

    Examples:
        >>> mask = Mask.getMask(layer, 0)
        >>> print(mask.mode, mask.id)
        >>> mask.opacity.get_value(PyFx.LTimeMode.CompTime, 0.0, False)
        100.0
    """

    def __init__(self, mask: PyFx.MaskRefPtr) -> None:
        self.mask = mask

    @classmethod
    def getMask(cls, layer: Layer, maskIndex: int) -> "Mask":
        """Get a mask from a layer by its index.

        Args:
            layer: The layer containing the mask.
            maskIndex: Zero-based index of the mask.

        Returns:
            The mask at the given index.

        Examples:
            >>> mask = Mask.getMask(layer, 0)
        """
        maskref = PyFx.MaskSuite().getLayerMaskByIndex(layer.layer, maskIndex)
        return Mask(maskref)

    def invert(self) -> bool:
        """Return whether this mask is inverted.

        Returns:
            `True` if the mask is inverted.
        """
        return PyFx.MaskSuite().getMaskInvert(self.mask)

    def setInvert(self, invert: bool) -> None:
        """Set the mask inversion state.

        Args:
            invert: `True` to invert the mask.
        """
        PyFx.MaskSuite().setMaskInvert(self.mask, invert)

    @property
    def mode(self) -> PyFx.MaskMode:
        """PyFx.MaskMode: Mask blending mode (Add, Subtract, etc.)."""
        return PyFx.MaskSuite().getMaskMode(self.mask)

    @mode.setter
    def mode(self, mode: PyFx.MaskMode) -> None:
        PyFx.MaskSuite().setMaskMode(self.mask, mode)

    @property
    def outline(self) -> MaskOutlineProperty:
        """MaskOutlineProperty: The mask path shape."""
        property = self.getProperty(PyFx.MaskStream.OUTLINE)
        return property

    @property
    def motionBlurState(self) -> PyFx.MaskMBlur:
        """PyFx.MaskMBlur: Motion blur state for this mask."""
        return PyFx.MaskSuite().getMaskMotionBlurState(self.mask)

    @property
    def opacity(self) -> OneDProperty:
        """OneDProperty: Mask opacity (0-100)."""
        property = self.getProperty(PyFx.MaskStream.OPACITY)
        return property

    @property
    def feather(self) -> TwoDProperty:
        """TwoDProperty: Mask feather as `(x, y)` pixels."""
        property = self.getProperty(PyFx.MaskStream.FEATHER)
        return property

    @property
    def expansion(self) -> OneDProperty:
        """OneDProperty: Mask expansion in pixels."""
        property = self.getProperty(PyFx.MaskStream.EXPANSION)
        return property

    @property
    def featherFalloff(self) -> PyFx.MaskFeatherFalloff:
        """PyFx.MaskFeatherFalloff: Feather falloff type."""
        return PyFx.MaskSuite().getMaskFeatherFalloff(self.mask)

    @featherFalloff.setter
    def featherFalloff(self, featherFalloff: PyFx.MaskFeatherFalloff) -> None:
        PyFx.MaskSuite().setMaskFeatherFalloff(self.mask, featherFalloff)

    @property
    def id(self) -> int:
        """int: Unique mask ID within its layer."""
        return PyFx.MaskSuite().getMaskID(self.mask)

    @property
    def color(self) -> tuple[float, float, float, float]:
        """tuple[float, float, float, float]: Mask display color (RGBA, 0.0-1.0)."""
        return PyFx.MaskSuite().getMaskColor(self.mask).to_tuple()

    @color.setter
    def color(self, color: tuple[float, float, float, float]) -> None:
        PyFx.MaskSuite().setMaskColor(self.mask, PyFx.ColorVal(color))

    @property
    def lockState(self) -> bool:
        """bool: Whether the mask is locked."""
        return PyFx.MaskSuite().getMaskLockState(self.mask)

    @lockState.setter
    def lockState(self, lock: bool) -> None:
        PyFx.MaskSuite().setMaskLockState(self.mask, lock)

    @property
    def isRotoBezier(self) -> bool:
        """bool: Whether the mask uses RotoBezier mode."""
        return PyFx.MaskSuite().getMaskIsRotoBezier(self.mask)

    @isRotoBezier.setter
    def isRotoBezier(self, isRotoBezier: bool) -> None:
        PyFx.MaskSuite().setMaskIsRotoBezier(self.mask, isRotoBezier)

    def getProperty(
        self, property: PyFx.MaskStream
    ) -> Union[BaseProperty, MaskOutlineProperty, OneDProperty, TwoDProperty]:
        """Get a mask property stream by its stream constant.

        Args:
            property: A `PyFx.MaskStream` enum value.

        Returns:
            The property as the appropriate typed subclass.
        """
        stream = self._suite.GetNewMaskStream(self.mask, property)
        return PropertyFactory.create_property(stream)


class Project:
    """An After Effects project (.aep file).

    Wraps the AE project suite to provide access to project items,
    settings, and file operations.

    Args:
        proj: Raw project pointer. If `None`, uses the current project.

    Examples:
        >>> project = Project()
        >>> print(project.path, project.bit_depth)
        >>>
        >>> for item in project.items:
        ...     print(item.name, item.type)
    """

    _suite = PyFx.ProjSuite()

    def __init__(self, proj: PyFx.ProjectPtr = None) -> None:
        if proj is None:  # if no project is passed in, get the first project
            proj = self._suite.GetProjectByIndex(0)  # get the first project
        self.proj = proj  # store the project

    @classmethod
    def new(cls, name: str, path: str) -> "Project":
        """Create a new project and optionally save it.

        Args:
            name: Project name.
            path: File path to save to. Pass empty string to skip saving.

        Returns:
            The newly created project.

        Examples:
            >>> project = Project.new("My Project", "C:/projects/my_project.aep")
        """
        proj = PyFx.ProjSuite().NewProject(name)
        if path:
            PyFx.ProjSuite().SaveProjectToPath(proj, path)
        return cls(proj)

    @classmethod
    def open(cls, path: str) -> "Project":
        """Open an existing project from disk.

        Args:
            path: Absolute path to the `.aep` file.

        Returns:
            The opened project.

        Examples:
            >>> project = Project.open("C:/projects/my_project.aep")
        """
        proj = PyFx.ProjSuite().OpenProjectFromPath(path)
        return cls(proj)

    @property
    def path(self) -> str:
        """str: Absolute file path of the project."""
        return self._suite.GetProjectPath(self.proj)

    @property
    def dirty(self) -> bool:
        """bool: Whether the project has unsaved changes."""
        return self._suite.ProjectIsDirty(self.proj)

    @property
    def bit_depth(self) -> PyFx.ProjBitDepth:
        """PyFx.ProjBitDepth: Project color bit depth setting."""
        return self._suite.GetProjectBitDepth(self.proj)

    @bit_depth.setter
    def bit_depth(self, value) -> None:
        self._suite.SetProjectBitDepth(self.proj, value)

    @property
    def items(self) -> ItemCollection:
        """ItemCollection: All items at the root level of the project."""
        return ItemCollection.create(
            self._suite.GetProjectRootFolder(self.proj)
        )

    def save(self, path: str) -> None:
        """Save the project to a file path.

        Args:
            path: Absolute path to save the `.aep` file to.

        Examples:
            >>> project.save("C:/projects/my_project_v002.aep")
        """
        self._suite.SaveProjectToPath(self.proj, path)

    def Import(self, path: str) -> None:
        """Import a file into the project.

        Args:
            path: Absolute path to the file to import.

        Examples:
            >>> project.Import("C:/assets/plate.exr")
        """
        self._suite.ImportFile(self.proj, path)
