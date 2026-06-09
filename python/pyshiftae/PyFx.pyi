"""Type stubs for the PyFx C++ extension module.

Provides type information for the After Effects SDK bindings exposed via
pybind11. Contains enumerations, handle/pointer types, value types, and
suite classes that map to the AEGP C++ API.
"""

from typing import Any, Tuple, Union
from enum import Enum, auto

class MemFlag(Enum):
    """Memory allocation flags for AE memory operations."""

    NONE = auto()  # * No Memory Flag.*#
    CLEAR = auto()  # * Clear Memory Flag.*#
    QUIET = auto()

class Platform(Enum):
    """Operating system platform identifiers."""

    WIN = auto()  # * Windows Platform.*#
    MAC = auto()

class ProjBitDepth(Enum):
    """Project color bit depth settings.

    Examples:
        >>> suite = PyFx.ProjSuite()
        >>> depth = suite.GetProjectBitDepth(project)
        >>> if depth == PyFx.ProjBitDepth._32:
        ...     print("32-bit project")
    """

    _8 = auto()
    _16 = auto()
    _32 = auto()
    NUM_VALID_DEPTHS = auto()

class CameraType(Enum):
    """Camera projection type."""

    NONE = auto()
    PERSPECTIVE = auto()
    ORTHOGRAPHIC = auto()
    NUM_TYPES = auto()

class TimeDisplayType(Enum):
    """Time display format in the AE timeline."""

    TIMECODE = auto()
    FRAMES = auto()
    FEET_AND_FRAMES = auto()

class FilmSizeUnits(Enum):
    """Film size measurement units for camera settings."""

    NONE = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()
    DIAGONAL = auto()

class LightType(Enum):
    """Light layer type in a composition."""

    NONE = auto()
    PARALLEL = auto()
    SPOT = auto()
    POINT = auto()
    AMBIENT = auto()
    RESERVED1 = auto()
    NUM_TYPES = auto()

class FootageSignature(Enum):
    """Footage file signature type."""

    NONE = auto()
    MISSING = auto()
    SOLID = auto()

class LightFalloffType(Enum):
    """Light intensity falloff type."""

    NONE = auto()
    SMOOTH = auto()
    INVERSE_SQUARE_CLAMPED = auto()

class FootageDepth(Enum):
    """Footage color bit depth."""

    _1 = auto()
    _2 = auto()
    _4 = auto()
    _8 = auto()
    _16 = auto()
    _24 = auto()
    _30 = auto()
    _32 = auto()
    GRAY_2 = auto()
    GRAY_4 = auto()
    GRAY_8 = auto()
    _48 = auto()
    _64 = auto()
    GRAY_16 = auto()

class FramesPerFoot(Enum):
    """Film frames per foot for feet+frames time display."""

    _35MM = auto()
    _16MM = auto()

class TimeDisplayMode(Enum):
    """Time display mode (timecode vs frame numbers)."""

    TIMECODE = auto()
    FRAMES = auto()

class SourceTimecodeDisplayMode(Enum):
    """Source footage timecode display mode."""

    ZERO = auto()
    SOURCE_TIMECODE = auto()

class FramesDisplayMode(Enum):
    """Frame numbering display mode."""

    ZERO_BASED = auto()
    ONE_BASED = auto()
    TIMECODE_CONVERSION = auto()

class SoundEncoding(Enum):
    """Audio sample encoding format."""

    UNSIGNED_PCM = auto()
    SIGNED_PCM = auto()
    FLOAT = auto()
    END = auto()
    BEGIN = auto()

class ItemType(Enum):
    """Project item type.

    Examples:
        >>> suite = PyFx.ItemSuite()
        >>> item_type = suite.GetItemType(item)
        >>> if item_type == PyFx.ItemType.COMP:
        ...     print("Item is a composition")
    """

    NONE = auto()
    FOLDER = auto()
    COMP = auto()
    SOLID = auto()
    FOOTAGE = auto()
    NUM_TYPES = auto()

class ItemFlag(Enum):
    """Flags describing item state and capabilities."""

    MISSING = auto()
    HAS_PROXY = auto()
    USING_PROXY = auto()
    MISSING_PROXY = auto()
    HAS_VIDEO = auto()
    HAS_AUDIO = auto()
    STILL = auto()
    HAS_ACTIVE_AUDIO = auto()

class Label(Enum):
    """Item label color index (1-16)."""

    NONE = auto()
    NO_LABEL = auto()
    LABEL_1 = auto()
    LABEL_2 = auto()
    LABEL_3 = auto()
    LABEL_4 = auto()
    LABEL_5 = auto()
    LABEL_6 = auto()
    LABEL_7 = auto()
    LABEL_8 = auto()
    LABEL_9 = auto()
    LABEL_10 = auto()
    LABEL_11 = auto()
    LABEL_12 = auto()
    LABEL_13 = auto()
    LABEL_14 = auto()
    LABEL_15 = auto()
    LABEL_16 = auto()
    NUM_TYPES = auto()

class PersistentType(Enum):
    """Persistent data blob type for storing plugin preferences."""

    MACHINE_SPECIFIC = auto()
    MACHINE_INDEPENDENT = auto()
    MACHINE_INDEPENDENT_RENDER = auto()
    MACHINE_INDEPENDENT_OUTPUT = auto()
    MACHINE_INDEPENDENT_COMPOSITION = auto()
    MACHINE_SPECIFIC_TEXT = auto()
    MACHINE_SPECIFIC_PAINT = auto()
    MACHINE_SPECIFIC_EFFECTS = auto()
    MACHINE_SPECIFIC_EXPRESSION_SNIPPETS = auto()
    MACHINE_SPECIFIC_SCRIPT_SNIPPETS = auto()
    NUM_TYPES = auto()

class CompFlag(Enum):
    """Composition-level flags for display and rendering options."""

    SHOW_ALL_SHY = auto()
    # * Show All Shy.*#
    ENABLE_MOTION_BLUR = auto()
    # * Enable Motion Blur.*#
    ENABLE_TIME_FILTER = auto()
    # * Enable Time Filter.*#
    GRID_TO_FRAMES = auto()
    # * Grid to Frames.*#
    GRID_TO_FIELDS = auto()
    # * Grid to Fields.*#
    USE_LOCAL_DSF = auto()
    # * Use Local DSF.*#
    DRAFT_3D = auto()
    # * Draft 3D.*#
    SHOW_GRAPH = auto()

class TransferFlags(Enum):
    """Layer blending transfer flags."""

    PRESERVE_ALPHA = auto()
    RANDOMIZE_DISSOLVE = auto()

class TrackMatte(Enum):
    """Track matte mode for layer compositing."""

    NO_TRACK_MATTE = auto()
    ALPHA = auto()
    NOT_ALPHA = auto()
    LUMA = auto()
    NOT_LUMA = auto()

class LayerQual(Enum):
    """Layer render quality setting."""

    NONE = auto()
    WIREFRAME = auto()
    DRAFT = auto()
    BEST = auto()

class LayerSamplingQual(Enum):
    """Layer sampling quality for image interpolation."""

    BILINEAR = auto()
    BICUBIC = auto()

class LayerFlag(Enum):
    """Layer state flags (visibility, audio, effects, 3D, etc.).

    Examples:
        >>> suite = PyFx.LayerSuite()
        >>> flags = suite.GetLayerFlags(layer)
        >>> suite.SetLayerFlag(layer, PyFx.LayerFlag.SHY, True)
    """

    NONE = auto()
    VIDEO_ACTIVE = auto()
    AUDIO_ACTIVE = auto()
    EFFECTS_ACTIVE = auto()
    MOTION_BLUR = auto()
    FRAME_BLENDING = auto()
    LOCKED = auto()
    SHY = auto()
    COLLAPSE = auto()
    AUTO_ORIENT_ROTATION = auto()
    ADJUSTMENT_LAYER = auto()
    TIME_REMAPPING = auto()
    LAYER_IS_3D = auto()
    LOOK_AT_CAMERA = auto()
    LOOK_AT_POI = auto()
    SOLO = auto()
    MARKERS_LOCKED = auto()
    NULL_LAYER = auto()
    HIDE_LOCKED_MASKS = auto()
    GUIDE_LAYER = auto()
    ADVANCED_FRAME_BLENDING = auto()
    SUBLAYERS_RENDER_SEPARATELY = auto()
    ENVIRONMENT_LAYER = auto()

class ObjectType(Enum):
    """Layer object type (AV, light, camera, text, vector).

    Examples:
        >>> suite = PyFx.LayerSuite()
        >>> obj_type = suite.GetLayerObjectType(layer)
        >>> if obj_type == PyFx.ObjectType.CAMERA:
        ...     print("Layer is a camera")
    """

    NONE = auto()
    AV = auto()
    LIGHT = auto()
    CAMERA = auto()
    TEXT = auto()
    VECTOR = auto()
    RESERVED1 = auto()
    RESERVED2 = auto()
    RESERVED3 = auto()
    RESERVED4 = auto()
    RESERVED5 = auto()
    NUM_TYPES = auto()

class LTimeMode(Enum):
    """Time reference mode for layer operations.

    Examples:
        >>> stream_suite = PyFx.StreamSuite()
        >>> value = stream_suite.GetNewStreamValue(
        ...     stream, PyFx.LTimeMode.CompTime, time, False
        ... )
    """

    LayerTime = auto()
    CompTime = auto()

class LayerStream(Enum):
    """Built-in layer stream (property) identifiers.

    Streams are grouped by layer type: common streams (anchor point,
    position, scale, etc.), camera-only, light-only, and AV-only streams.

    Examples:
        >>> stream_suite = PyFx.StreamSuite()
        >>> pos_stream = stream_suite.GetNewLayerStream(
        ...     layer, PyFx.LayerStream.POSITION
        ... )
    """

    SOURCE_TEXT = auto()
    ## Valid for all layer types
    ANCHORPOINT = auto()
    POSITION = auto()
    SCALE = auto()
    ROTATION = auto()
    ROTATE_Z = auto()
    OPACITY = auto()
    AUDIO = auto()
    MARKER = auto()
    TIME_REMAP = auto()
    ROTATE_X = auto()
    ROTATE_Y = auto()
    ORIENTATION = auto()
    TEXT = auto()
    ## only valid for AEGP_ObjectType = auto()
    DEPTH_OF_FIELD = auto()
    FOCUS_DISTANCE = auto()
    APERTURE = auto()
    BLUR_LEVEL = auto()
    IRIS_SHAPE = auto()
    IRIS_ROTATION = auto()
    IRIS_ROUNDNESS = auto()
    IRIS_ASPECT_RATIO = auto()
    IRIS_DIFFRACTION_FRINGE = auto()
    IRIS_HIGHLIGHT_GAIN = auto()
    IRIS_HIGHLIGHT_THRESHOLD = auto()
    IRIS_HIGHLIGHT_SATURATION = auto()
    ## only valid for AEGP_ObjectType = auto()
    COLOR = auto()
    CONE_ANGLE = auto()
    CONE_FEATHER = auto()
    SHADOW_DARKNESS = auto()
    SHADOW_DIFFUSION = auto()
    LIGHT_FALLOFF_TYPE = auto()
    LIGHT_FALLOFF_START = auto()
    LIGHT_FALLOFF_DISTANCE = auto()
    ## only valid for AEGP_ObjectType = auto()
    ACCEPTS_LIGHTS = auto()
    AMBIENT_COEFF = auto()
    DIFFUSE_COEFF = auto()
    SPECULAR_INTENSITY = auto()
    SPECULAR_SHININESS = auto()
    CASTS_SHADOWS = auto()
    LIGHT_TRANSMISSION = auto()
    METAL = auto()
    REFLECTION_INTENSITY = auto()
    REFLECTION_SHARPNESS = auto()
    REFLECTION_ROLLOFF = auto()
    TRANSPARENCY_COEFF = auto()
    TRANSPARENCY_ROLLOFF = auto()
    INDEX_OF_REFRACTION = auto()
    EXTRUSION_BEVEL_STYLE = auto()
    EXTRUSION_BEVEL_DIRECTION = auto()
    EXTRUSION_BEVEL_DEPTH = auto()
    EXTRUSION_HOLE_BEVEL_DEPTH = auto()
    EXTRUSION_DEPTH = auto()
    PLANE_CURVATURE = auto()
    PLANE_SUBDIVISION = auto()

class MaskStream(Enum):
    """Mask property stream identifiers."""

    OUTLINE = auto()
    OPACITY = auto()
    FEATHER = auto()
    EXPANSION = auto()

class StreamFlag(Enum):
    """Flags describing stream capabilities (min/max bounds, spatial)."""

    NONE = auto()
    HAS_MIN = auto()
    HAS_MAX = auto()
    IS_SPATIAL = auto()

class KeyInterp(Enum):
    """Keyframe interpolation type.

    Examples:
        >>> kf_suite = PyFx.KeyframeSuite()
        >>> in_interp, out_interp = kf_suite.GetKeyframeInterpolation(stream, 0)
        >>> kf_suite.SetKeyframeInterpolation(
        ...     stream, 0, PyFx.KeyInterp.BEZIER, PyFx.KeyInterp.BEZIER
        ... )
    """

    NONE = auto()
    LINEAR = auto()
    BEZIER = auto()
    HOLD = auto()

class KeyInterpMask(Enum):
    """Bitmask of valid keyframe interpolation types for a stream."""

    NONE = auto()
    LINEAR = auto()
    BEZIER = auto()
    HOLD = auto()
    CUSTOM = auto()
    ANY = auto()

class StreamType(Enum):
    """Data type of a property stream value.

    Examples:
        >>> stream_suite = PyFx.StreamSuite()
        >>> stream_type = stream_suite.GetStreamType(stream)
        >>> if stream_type == PyFx.StreamType.ThreeD:
        ...     print("Stream holds 3D values")
    """

    NONE = auto()
    ThreeD_SPATIAL = auto()
    ThreeD = auto()
    TwoD_SPATIAL = auto()
    TwoD = auto()
    OneD = auto()
    COLOR = auto()
    ARB = auto()
    MARKER = auto()
    LAYER_ID = auto()
    MASK_ID = auto()
    MASK = auto()
    TEXT_DOCUMENT = auto()

class StreamGroupingType(Enum):
    """Stream hierarchy grouping type (leaf property vs group)."""

    NONE = auto()
    LEAF = auto()
    NAMED_GROUP = auto()
    INDEXED_GROUP = auto()

class DynStreamFlag(Enum):
    """Dynamic stream flags (visibility, active state, etc.)."""

    ACTIVE_EYEBALL = auto()
    HIDDEN = auto()
    DISABLED = auto()
    ELIDED = auto()
    SHOWN_WHEN_EMPTY = auto()
    SKIP_REVEAL_WHEN_UNHIDDEN = auto()

class KeyframeFlag(Enum):
    """Keyframe behavior flags (continuity, auto-bezier, roving)."""

    NONE = auto()
    TEMPORAL_CONTINUOUS = auto()
    TEMPORAL_AUTOBEZIER = auto()
    SPATIAL_CONTINUOUS = auto()
    SPATIAL_AUTOBEZIER = auto()
    ROVING = auto()

class MarkerStringType(Enum):
    """Marker string data type (comment, chapter, URL, etc.)."""

    COMMENT = auto()
    CHAPTER = auto()
    URL = auto()
    FRAME_TARGET = auto()
    CUE_POINT_NAME = auto()

class MarkerFlag(Enum):
    """Marker behavior flags."""

    NONE = auto()
    NAVIGATION = auto()
    PROTECT_REGION = auto()

class EffectFlags(Enum):
    """Effect state flags (active, audio, missing)."""

    NONE = auto()
    ACTIVE = auto()
    AUDIO_ONLY = auto()
    AUDIO_TOO = auto()
    MISSING = auto()

class MaskMode(Enum):
    """Mask blending mode."""

    NONE = auto()
    ADD = auto()
    SUBTRACT = auto()
    INTERSECT = auto()
    LIGHTEN = auto()
    DARKEN = auto()
    DIFF = auto()
    ACCUM = auto()

class MaskMBlur(Enum):
    """Mask motion blur setting."""

    SAME_AS_LAYER = auto()
    OFF = auto()
    ON = auto()

class MaskFeatherFalloff(Enum):
    """Mask feather falloff curve type."""

    SMOOTH = auto()
    LINEAR = auto()

class MaskFeatherInterp(Enum):
    """Mask feather interpolation mode."""

    NORMAL = auto()
    HOLD_CW = auto()

class MaskFeatherType(Enum):
    """Mask feather direction (inner vs outer)."""

    OUTER = auto()
    INNER = auto()

class AlphaFlags(Enum):
    """Alpha channel interpretation flags."""

    PREMUL = auto()
    INVERTED = auto()
    ALPHA_IGNORE = auto()

class PulldownPhase(Enum):
    """3:2 pulldown phase for telecine footage."""

    NO_PULLDOWN = auto()
    WSSWW = auto()
    SSWWW = auto()
    SWWWS = auto()
    WWWSS = auto()
    WWSSW = auto()
    WWWSW = auto()
    WWSWW = auto()
    WSWWW = auto()
    SWWWW = auto()
    WWWWS = auto()

class LayerDrawStyle(Enum):
    """Layer draw style for footage layer keys."""

    LAYER_BOUNDS = auto()
    DOCUMENT_BOUNDS = auto()

class InterpretationStyle(Enum):
    """Footage interpretation dialog behavior on import."""

    NO_DIALOG_GUESS = auto()
    DIALOG_OK = auto()
    NO_DIALOG_NO_GUESS = auto()

class PluginPathType(Enum):
    """Plugin directory path type."""

    PLUGIN = auto()
    USER_PLUGIN = auto()
    ALLUSER_PLUGIN = auto()
    APP = auto()

class RenderQueueState(Enum):
    """Render queue processing state."""

    STOPPED = auto()
    PAUSED = auto()
    RENDERING = auto()

class RenderItemStatus(Enum):
    """Status of a render queue item."""

    NONE = auto()
    WILL_CONTINUE = auto()
    NEEDS_OUTPUT = auto()
    UNQUEUED = auto()
    QUEUED = auto()
    RENDERING = auto()
    USER_STOPPED = auto()
    ERR_STOPPED = auto()
    DONE = auto()

class LogType(Enum):
    """Render queue item logging verbosity level."""

    NONE = auto()
    ERRORS_ONLY = auto()
    PLUS_SETTINGS = auto()
    PER_FRAME_INFO = auto()

class EmbeddingType(Enum):
    """Output module project link embedding option."""

    NONE = auto()
    NOTHING = auto()
    LINK = auto()
    LINK_AND_COPY = auto()

class PostRenderAction(Enum):
    """Action to perform after rendering completes."""

    NONE = auto()
    IMPORT = auto()
    IMPORT_AND_REPLACE_USAGE = auto()
    SET_PROXY = auto()

class OutputTypes(Enum):
    """Output module enabled output types (video, audio, or both)."""

    NONE = auto()
    VIDEO = auto()
    AUDIO = auto()

class VideoChannels(Enum):
    """Output video channel configuration."""

    NONE = auto()
    RGB = auto()
    RGBA = auto()
    ALPHA = auto()

class StretchQuality(Enum):
    """Output stretch (resize) quality."""

    NONE = auto()
    LOW = auto()
    HIGH = auto()

class OutputColorType(Enum):
    """Output alpha color interpretation."""

    STRAIGHT = auto()
    PREMUL = auto()

class WorldType(Enum):
    """Pixel buffer (world) bit depth."""

    NONE = auto()
    W8 = auto()
    W16 = auto()
    W32 = auto()

class MatteMode(Enum):
    """Matte/alpha compositing mode."""

    STRAIGHT = auto()
    PREMUL_BLACK = auto()
    PREMUL_BG_COLOR = auto()

class ChannelOrder(Enum):
    """Pixel channel ordering in memory."""

    ARGB = auto()
    BGRA = auto()

class ItemQuality(Enum):
    """Item render quality (draft vs best)."""

    DRAFT = auto()
    BEST = auto()

class CollectionItemType(Enum):
    """Type of item stored in an AE collection."""

    NONE = auto()
    LAYER = auto()
    MASK = auto()
    EFFECT = auto()
    STREAM = auto()
    KEYFRAME = auto()
    MASK_VERTEX = auto()
    STREAMREF = auto()

class StreamCollectionItemType(Enum):
    """Type of item that owns a stream in a collection."""

    NONE = auto()
    LAYER = auto()
    MASK = auto()
    EFFECT = auto()

class WindowType(Enum):
    """AE application window/panel type."""

    NONE = auto()
    PROJECT = auto()
    COMP = auto()
    TIME_LAYOUT = auto()
    LAYER = auto()
    FOOTAGE = auto()
    RENDER_QUEUE = auto()
    QT = auto()
    DIALOG = auto()
    FLOWCHART = auto()
    EFFECT = auto()
    OTHER = auto()

class MenuID(Enum):
    """AE application menu identifiers."""

    NONE = auto()
    APPLE = auto()
    FILE = auto()
    EDIT = auto()
    COMPOSITION = auto()
    LAYER = auto()
    EFFECT = auto()
    WINDOW = auto()
    FLOATERS = auto()
    KF_ASSIST = auto()
    IMPORT = auto()
    SAVE_FRAME_AS = auto()
    PREFS = auto()
    EXPORT = auto()
    ANIMATION = auto()
    PURGE = auto()
    NEW = auto()

class AEHandle:
    """Base RAII handle wrapper for AE SDK opaque pointers.

    Manages the lifetime of an AE SDK handle with optional custom deleter.
    All typed pointer classes (`ItemPtr`, `LayerPtr`, etc.) inherit from this.

    Args:
        handle: The raw SDK handle.
        deleter: Optional callable to release the handle on destruction.
    """

    def __init__(self, handle: Any, deleter: Any = None):
        self.handle = handle
        self.deleter = deleter

    def __del__(self):
        if self.deleter:
            self.deleter(self.handle)

    def __bool__(self):
        return self.handle is not None

    def get(self):
        """Return the raw handle."""
        return self.handle

    def remove_deleter(self):
        """Detach the deleter without releasing the handle."""
        self.deleter = None

    def reset(self, new_handle=None):
        """Release the current handle and optionally replace it."""
        if self.deleter:
            self.deleter(self.handle)
        self.handle = new_handle

    def swap(self, other):
        """Swap handles and deleters with another `AEHandle`."""
        self.handle, other.handle = other.handle, self.handle
        self.deleter, other.deleter = other.deleter, self.deleter

    def release(self):
        """Release ownership of the handle without calling the deleter."""
        self.handle = None

    def __call__(self):
        return self.handle

class StreamRefPtr(AEHandle):
    """Handle to a property stream (keyframeable parameter)."""

class ProjectPtr(AEHandle):
    """Handle to an AE project."""

class ItemPtr(AEHandle):
    """Handle to a project item (folder, comp, footage, or solid)."""

class CompPtr(AEHandle):
    """Handle to a composition."""

class FootagePtr(AEHandle):
    """Handle to a footage source."""

class LayerPtr(AEHandle):
    """Handle to a layer in a composition."""

class EffectRefPtr(AEHandle):
    """Handle to an effect instance applied to a layer."""

class MaskRefPtr(AEHandle):
    """Handle to a mask on a layer."""

class RenderLayerContextPtr(AEHandle):
    """Handle to a render layer context."""

class PersistentBlobPtr(AEHandle):
    """Handle to a persistent data blob for storing preferences."""

class MaskOutlineValPtr(AEHandle):
    """Handle to a mask outline value (vertices and feathers)."""

class CollectionPtr(AEHandle):
    """Handle to an AE collection of items."""

class Collection2Ptr(AEHandle):
    """Handle to an AE collection (v2) of items."""

class SoundDataPtr(AEHandle):
    """Handle to sound/audio data samples."""

class AddKeyframesInfoPtr(AEHandle):
    """Handle to a batch keyframe addition operation."""

class RenderReceiptPtr(AEHandle):
    """Handle to a render receipt."""

class WorldPtr(AEHandle):
    """Handle to a pixel buffer (world/frame)."""

class RenderOptionsPtr(AEHandle):
    """Handle to render options configuration."""

class LayerRenderOptionsPtr(AEHandle):
    """Handle to layer-specific render options."""

class FrameReceiptPtr(AEHandle):
    """Handle to a rendered frame receipt."""

class RQItemRefPtr(AEHandle):
    """Handle to a render queue item."""

class OutputModuleRefPtr(AEHandle):
    """Handle to an output module attached to a render queue item."""

class TextDocumentPtr(AEHandle):
    """Handle to a text layer's document data."""

class MarkerValPtr(AEHandle):
    """Handle to a marker value."""

class TextOutlinesPtr(AEHandle):
    """Handle to text layer outlines (vector paths)."""

class PlatformWorldPtr(AEHandle):
    """Handle to a platform-native pixel buffer."""

class ItemViewPtr(AEHandle):
    """Handle to an item view (panel showing an item)."""

class ColorProfilePtr(AEHandle):
    """Handle to a mutable color profile."""

class ConstColorProfilePtr(AEHandle):
    """Handle to a read-only color profile."""

class TimeStampPtr(AEHandle):
    """Handle to a timestamp value."""

class MemHandlePtr(AEHandle):
    """Handle to an AE-managed memory block."""

class StreamValue2(AEHandle):
    """Container for a stream property value.

    Wraps a typed value (scalar, 2D, 3D, or color) associated with a
    specific stream. Used to get and set property and keyframe values.

    Args:
        streamref: The stream this value belongs to.
        value: The numeric value (float, 2-tuple, 3-tuple, or 4-tuple).

    Examples:
        >>> stream_suite = PyFx.StreamSuite()
        >>> sv = stream_suite.GetNewStreamValue(
        ...     stream, PyFx.LTimeMode.CompTime, time, False
        ... )
        >>> print(sv.value())
    """

    def __init__(
        self,
        streamref: StreamRefPtr,
        value: Union[
            float,
            Tuple[float, float],
            Tuple[float, float, float],
            Tuple[float, float, float, float],
        ],
    ):
        # actual implementation done on the C++ side
        pass

    def value(
        self,
    ) -> Union[
        float,
        Tuple[float, float],
        Tuple[float, float, float],
        Tuple[float, float, float, float],
    ]:
        """Return the underlying numeric value."""
        pass

class ColorVal:
    """Represents a color value with RGBA components."""

    def __init__(self, r=0, g=0, b=0, a=0):
        self.red = r
        self.green = g
        self.blue = b
        self.alpha = a

    def __init__(self, color: Tuple[float, float, float, float]):
        pass

    def to_tuple(self) -> Tuple[float, float, float, float]:
        """Convert the ColorVal instance to a tuple."""
        pass

class TimeDisplay3:
    """Manages display settings for time formats."""

    def __init__(
        self,
        display_mode=TimeDisplayMode.FRAMES,
        footage_display_mode=SourceTimecodeDisplayMode.ZERO,
        display_dropframe=False,
        use_feet_frames=False,
        timebase="0",
        frames_per_foot="0",
        frames_display_mode=FramesDisplayMode.ONE_BASED,
    ):
        self.display_mode = display_mode
        self.footage_display_mode = footage_display_mode
        self.display_dropframe = display_dropframe
        self.use_feet_frames = use_feet_frames
        self.timebase = timebase
        self.frames_per_foot = frames_per_foot
        self.frames_display_mode = frames_display_mode

    def to_tuple(self) -> Tuple:
        """Convert the TimeDisplay3 instance to a tuple."""
        pass

class SoundDataFormat:
    """Represents sound data format details."""

    def __init__(
        self,
        sample_rate=0.0,
        encoding=SoundEncoding.BEGIN,
        bytes_per_sample=0,
        num_channels=0,
    ):
        self.sample_rate = sample_rate
        self.encoding = encoding
        self.bytes_per_sample = bytes_per_sample
        self.num_channels = num_channels

    def to_tuple(self) -> Tuple:
        """Convert the SoundDataFormat instance to a tuple."""
        pass

class DownsampleFactor:
    """Represents a downsample factor."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __init__(self, factor: Tuple[int, int]):
        pass

    def to_tuple(self) -> Tuple[int, int]:
        """Convert the DownsampleFactor instance to a tuple."""
        pass

class LayerTransferMode:
    """Represents layer transfer mode details."""

    def __init__(
        self,
        mode=0,
        flags=TransferFlags.PRESERVE_ALPHA,
        track_matte=TrackMatte.NO_TRACK_MATTE,
    ):
        self.mode = mode
        self.flags = flags
        self.track_matte = track_matte

    def to_tuple(self) -> Tuple:
        """Convert the LayerTransferMode instance to a tuple."""
        pass

class OneDVal:
    """A single scalar value.

    Args:
        value: The scalar value. Defaults to 0.
    """

    def __init__(self, value=0):
        self.value = value

    def val(self):
        """Return the scalar value."""
        pass

    def to_tuple(self) -> Tuple:
        """Convert to a tuple."""
        pass

class TwoDVal:
    """Represents a 2D value."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __init__(self, value: Tuple[float, float]):
        pass

    def to_tuple(self) -> Tuple[float, float]:
        """Convert the TwoDVal instance to a tuple."""
        pass

class ThreeDVal:
    """Represents a 3D value."""

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __init__(self, value: Tuple[float, float, float]):
        pass

    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert the ThreeDVal instance to a tuple."""
        pass

class KeyframeEase:
    """Represents keyframe ease settings."""

    def __init__(self, speed=0, influence=0):
        self.speed = speed
        self.influence = influence

    def __init__(self, value: Tuple[float, float]):
        pass

    def to_tuple(self) -> Tuple[float, float]:
        """Convert the KeyframeEase instance to a tuple."""
        pass

class MaskFeather:
    """Mask feather settings for a single feather point.

    Args:
        segment: Segment index.
        segment_sF: Segment position (0.0-1.0).
        radiusF: Feather radius.
        ui_corner_angleF: Corner angle in the UI.
        tensionF: Feather tension.
        interp: Feather interpolation mode.
        type: Feather direction (inner or outer).
    """

    def __init__(
        self,
        segment=0,
        segment_sF=0,
        radiusF=0,
        ui_corner_angleF=0,
        tensionF=0,
        interp=MaskFeatherInterp.NORMAL,
        type=MaskFeatherType.OUTER,
    ):
        self.segment = segment
        self.segment_sF = segment_sF
        self.radiusF = radiusF
        self.ui_corner_angleF = ui_corner_angleF
        self.tensionF = tensionF
        self.interp = interp
        self.type = type

    def to_tuple(self) -> Tuple:
        """Convert to a tuple."""
        pass

class MaskVertex:
    """A mask path vertex with position and tangent handles.

    Args:
        x: Vertex X position.
        y: Vertex Y position.
        tan_in_x: Incoming tangent X.
        tan_in_y: Incoming tangent Y.
        tan_out_x: Outgoing tangent X.
        tan_out_y: Outgoing tangent Y.
    """

    def __init__(
        self, x=0, y=0, tan_in_x=0, tan_in_y=0, tan_out_x=0, tan_out_y=0
    ):
        self.x = x
        self.y = y
        self.tan_in_x = tan_in_x
        self.tan_in_y = tan_in_y
        self.tan_out_x = tan_out_x
        self.tan_out_y = tan_out_y

    def to_tuple(self) -> Tuple[float, float, float, float, float, float]:
        """Convert to a tuple of (x, y, tan_in_x, tan_in_y, tan_out_x, tan_out_y)."""
        pass

class LoopBehavior:
    """Loop behavior settings for footage playback.

    Args:
        loops: Number of loops.
        reserved: Reserved field.
    """

    def __init__(self, loops=0, reserved=0):
        self.loops = loops
        self.reserved = reserved

    def to_tuple(self) -> Tuple[int, int]:
        """Convert to a tuple of (loops, reserved)."""
        pass

class FootageLayerKey:
    """Identifies a specific layer within a multi-layer footage source.

    Args:
        layer_idL: Layer ID (-1 for default).
        layer_indexL: Layer index (-1 for default).
        nameAC: Layer name.
        layer_draw_style: Draw style for the layer.
    """

    def __init__(
        self,
        layer_idL=-1,
        layer_indexL=-1,
        nameAC="",
        layer_draw_style=LayerDrawStyle.LAYER_BOUNDS,
    ):
        self.layer_idL = layer_idL
        self.layer_indexL = layer_indexL
        self.nameAC = nameAC
        self.layer_draw_style = layer_draw_style

    def to_tuple(self) -> Tuple[int, int, str, LayerDrawStyle]:
        """Convert to a tuple."""
        pass

    def default():
        """Return a default `FootageLayerKey`."""
        pass

class FileSequenceImportOptions:
    """Options for importing file sequences or stills.

    Args:
        all_in_folderB: Import all files in the folder as a sequence.
        force_alphabeticalB: Force alphabetical ordering.
        start_frameL: Start frame (-1 for auto).
        end_frameL: End frame (-1 for auto).

    Examples:
        >>> opts = PyFx.FileSequenceImportOptions()
        >>> opts.sequence()  # configure for image sequence
        >>> footage = footage_suite.newFootage(
        ...     path, layer_key, opts,
        ...     PyFx.InterpretationStyle.NO_DIALOG_GUESS
        ... )
    """

    def __init__(
        self,
        all_in_folderB=False,
        force_alphabeticalB=False,
        start_frameL=-1,
        end_frameL=-1,
    ):
        self.all_in_folderB = all_in_folderB
        self.force_alphabeticalB = force_alphabeticalB
        self.start_frameL = start_frameL
        self.end_frameL = end_frameL

    def to_tuple(self) -> Tuple[bool, bool, int, int]:
        """Convert to a tuple."""
        pass

    def still(self):
        """Configure for importing a single still image."""
        self.all_in_folderB = False
        return self

    def sequence(self):
        """Configure for importing an image sequence."""
        self.all_in_folderB = True
        self.force_alphabeticalB = True
        return self

class Time:
    """AE time value stored as a rational number (numerator/scale).

    Can be constructed from a tuple, float, or int.

    Args:
        value: Time as (numerator, scale) tuple, seconds float, or frame int.

    Examples:
        >>> t = PyFx.Time(2.5)         # 2.5 seconds
        >>> t = PyFx.Time((75, 30))    # 75/30 = 2.5 seconds at 30fps
        >>> print(t.to_seconds())
    """

    def __init__(self, value=(0, 1)):
        self.value = value

    def __init__(self, value: float):
        pass

    def __init__(self, value: int):
        pass

    def to_seconds(self) -> float:
        """Convert to seconds as a float."""
        pass

    def to_frames(self) -> int:
        """Convert to frame number as an integer."""
        pass

class Ratio:
    """Rational number (numerator/denominator).

    Used for pixel aspect ratios, frame rates, and other fractional values.

    Args:
        num: Numerator.
        den: Denominator (must not be zero).

    Examples:
        >>> ratio = PyFx.Ratio(1, 1)  # square pixels
        >>> ratio = PyFx.Ratio(16, 9)
    """

    def __init__(self, num=0, den=1):
        self.num = num
        self.den = den

    def __init__(self, value: float):
        pass

    def __init__(self, value: int):
        pass

    def to_tuple(self) -> Tuple[int, int]:
        """Convert to a (numerator, denominator) tuple."""
        pass

    def value(self) -> Tuple[int, int]:
        """Return the (numerator, denominator) pair."""
        pass

class FloatPoint:
    """2D floating-point coordinate.

    Args:
        x: X coordinate.
        y: Y coordinate.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def to_tuple(self) -> Tuple[float, float]:
        """Convert to an (x, y) tuple."""
        pass

class FloatPoint3:
    """3D floating-point coordinate.

    Args:
        x: X coordinate.
        y: Y coordinate.
        z: Z coordinate.
    """

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to an (x, y, z) tuple."""
        pass

class FloatRect:
    """Floating-point rectangle defined by edges.

    Args:
        left: Left edge.
        top: Top edge.
        right: Right edge.
        bottom: Bottom edge.
    """

    def __init__(self, left=0, top=0, right=0, bottom=0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def to_tuple(self) -> Tuple[float, float, float, float]:
        """Convert to a (left, top, right, bottom) tuple."""
        pass

class Matrix3:
    """3x3 transformation matrix."""

    def __init__(self, mat=None):
        self.mat = mat

class Matrix4:
    """4x4 transformation matrix (used for 3D layer transforms)."""

    def __init__(self, mat=None):
        self.mat = mat

class LegacyRect:
    """Legacy integer rectangle (top, left, bottom, right order)."""

    def __init__(self, top=0, left=0, bottom=0, right=0):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right

    def to_tuple(self) -> Tuple[int, int, int, int]:
        pass

class LRect:
    """Integer rectangle (left, top, right, bottom order)."""

    def __init__(self, left=0, top=0, right=0, bottom=0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def to_tuple(self) -> Tuple[int, int, int, int]:
        pass

class LPoint:
    """Integer 2D point."""

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def to_tuple(self) -> Tuple[int, int]:
        pass

class FloatPolar:
    """Polar coordinate (radius and angle).

    Args:
        radius: Distance from origin.
        angle: Angle in radians.
    """

    def __init__(self, radius: float, angle: float):
        self.radius = radius
        self.angle = angle

    def to_tuple(self) -> Tuple[float, float]:
        pass

class Marker:
    """High-level wrapper for composition and layer markers.

    Provides methods to read/write marker comments, chapters, URLs,
    cue point parameters, duration, and labels.

    Args:
        markerP: The underlying marker handle.

    Examples:
        >>> marker = PyFx.Marker.createMarker()
        >>> marker.setString(PyFx.MarkerStringType.COMMENT, "Scene 1")
        >>> marker.setDuration(2.0)
    """

    def __init__(self, markerP: MarkerValPtr):
        self.markerP = markerP

    @classmethod
    def createMarker(cls):
        """Create a new empty marker."""
        pass

    def duplicateMarker(self):
        """Create a copy of this marker."""
        pass

    def setFlag(self, flagType: MarkerFlag, valueB: bool):
        """Set a marker flag.

        Args:
            flagType: Which flag to set.
            valueB: Flag value.
        """
        pass

    def getFlag(self, flagType: MarkerFlag) -> bool:
        """Get a marker flag value.

        Args:
            flagType: Which flag to query.

        Returns:
            The flag value.
        """
        pass

    def getString(self, strType: MarkerStringType) -> str:
        """Get a marker string (comment, chapter, URL, etc.).

        Args:
            strType: Which string to retrieve.

        Returns:
            The string value.
        """
        pass

    def setString(self, strType: MarkerStringType, unicodeP: str):
        """Set a marker string.

        Args:
            strType: Which string to set.
            unicodeP: The new string value.
        """
        pass

    def countCuePointParams(self) -> int:
        """Return the number of cue point parameters."""
        pass

    def getIndCuePointParam(self, param_indexL: int) -> Tuple[str, str]:
        """Get a cue point parameter key/value pair by index.

        Args:
            param_indexL: Parameter index.

        Returns:
            A (key, value) tuple.
        """
        pass

    def setIndCuePointParam(
        self, param_indexL: int, unicodeKeyP: str, unicodeValueP: str
    ):
        """Set a cue point parameter key/value pair.

        Args:
            param_indexL: Parameter index.
            unicodeKeyP: Parameter key.
            unicodeValueP: Parameter value.
        """
        pass

    def insertCuePointParam(self, param_indexL: int):
        """Insert a new cue point parameter at the given index.

        Args:
            param_indexL: Insertion index.
        """
        pass

    def deleteIndCuePointParam(self, param_indexL: int):
        """Delete the cue point parameter at the given index.

        Args:
            param_indexL: Parameter index to delete.
        """
        pass

    def setDuration(self, durationD: float):
        """Set the marker duration in seconds.

        Args:
            durationD: Duration in seconds.
        """
        pass

    def getDuration(self) -> float:
        """Get the marker duration in seconds."""
        pass

    def setLabel(self, value: int):
        """Set the marker label color index.

        Args:
            value: Label color index.
        """
        pass

    def getLabel(self) -> int:
        """Get the marker label color index."""
        pass

class MaskOutline:
    """High-level wrapper for mask outline path data.

    Provides access to mask vertices (Bezier control points) and
    per-vertex feather settings.

    Args:
        mask_outlineP: The underlying mask outline handle.

    Examples:
        >>> outline = MaskOutline(mask_outline_ptr)
        >>> for i in range(outline.numSegments()):
        ...     vertex = outline.getVertexInfo(i)
        ...     print(vertex.to_tuple())
    """

    def __init__(self, mask_outlineP: MaskOutlineValPtr):
        self.mask_outlineP = mask_outlineP

    def isOpen(self) -> bool:
        """Check whether the mask path is open (not closed)."""
        pass

    def setOpen(self, openB: bool):
        """Set the mask path open/closed state.

        Args:
            openB: True for open path, False for closed.
        """
        pass

    def numSegments(self) -> int:
        """Return the number of segments (vertices) in the mask path."""
        pass

    def getVertexInfo(self, which_pointL: int) -> MaskVertex:
        """Get vertex position and tangent data by index.

        Args:
            which_pointL: Vertex index.

        Returns:
            The vertex data.
        """
        pass

    def setVertexInfo(self, which_pointL: int, vertexP: MaskVertex):
        """Set vertex position and tangent data.

        Args:
            which_pointL: Vertex index.
            vertexP: New vertex data.
        """
        pass

    def createVertex(self, insert_position):
        """Insert a new vertex at the given position.

        Args:
            insert_position: Index at which to insert.
        """
        pass

    def deleteVertex(self, index: int):
        """Delete a vertex by index.

        Args:
            index: Vertex index to delete.
        """
        pass

    def numFeathers(self) -> int:
        """Return the number of feather points."""
        pass

    def getFeatherInfo(self, which_featherL: int) -> MaskFeather:
        """Get feather settings by index.

        Args:
            which_featherL: Feather index.

        Returns:
            The feather settings.
        """
        pass

    def setFeatherInfo(self, which_featherL: int, featherP: MaskFeather):
        """Set feather settings by index.

        Args:
            which_featherL: Feather index.
            featherP: New feather settings.
        """
        pass

    def createFeather(self, featherP0: MaskFeather) -> int:
        """Create a new feather point.

        Args:
            featherP0: Initial feather settings.

        Returns:
            The index of the new feather.
        """
        pass

    def deleteFeather(self, index: int):
        """Delete a feather point by index.

        Args:
            index: Feather index to delete.
        """
        pass

class TextDocument:
    """High-level wrapper for a text layer's source text document.

    Args:
        text_documentP: The underlying text document handle.

    Examples:
        >>> doc = PyFx.TextDocument(text_doc_ptr)
        >>> print(doc.getText())
        >>> doc.setText("Hello World")
    """

    def __init__(self, text_documentP: TextDocumentPtr):
        self.text_documentP = text_documentP

    def getText(self) -> str:
        """Get the text content of the document."""
        pass

    def setText(self, unicodePS: str):
        """Set the text content of the document.

        Args:
            unicodePS: New text string.
        """
        pass

class ProjSuite:
    """Suite for project-level operations.

    Provides methods to query and modify AE projects, including
    file I/O, time display settings, and bit depth.

    Examples:
        >>> suite = PyFx.ProjSuite()
        >>> project = suite.GetProjectByIndex(0)
        >>> name = suite.GetProjectName(project)
    """

    def __init__(self):
        pass

    def GetNumProjects(self) -> int:
        """Return the number of open projects."""
        pass

    def GetProjectByIndex(self, projIndex: int) -> ProjectPtr:
        """Get a project by index.

        Args:
            projIndex: Zero-based project index.

        Returns:
            Handle to the project.
        """
        pass

    def GetProjectName(self, project: ProjectPtr) -> str:
        """Get the project name.

        Args:
            project: Project handle.

        Returns:
            The project name string.
        """
        pass

    def GetProjectPath(self, project: ProjectPtr) -> str:
        """Get the file path of the project.

        Args:
            project: Project handle.

        Returns:
            The project file path.
        """
        pass

    def GetProjectRootFolder(self, project: ProjectPtr) -> ItemPtr:
        """Get the root folder item of the project.

        Args:
            project: Project handle.

        Returns:
            Handle to the root folder item.
        """
        pass

    def SaveProjectToPath(self, project: ProjectPtr, path: str):
        """Save the project to a file path.

        Args:
            project: Project handle.
            path: Destination file path.
        """
        pass

    def GetProjectTimeDisplay(self, project: ProjectPtr) -> TimeDisplay3:
        """Get the project time display settings.

        Args:
            project: Project handle.

        Returns:
            The time display configuration.
        """
        pass

    def SetProjectTimeDisplay(
        self, project: ProjectPtr, timeDisplay: TimeDisplay3
    ):
        """Set the project time display settings.

        Args:
            project: Project handle.
            timeDisplay: New time display configuration.
        """
        pass

    def ProjectIsDirty(self, project: ProjectPtr) -> bool:
        """Check if the project has unsaved changes.

        Args:
            project: Project handle.

        Returns:
            True if the project has unsaved changes.
        """
        pass

    def SaveProjectAs(self, project: ProjectPtr, path: str):
        """Save the project to a new path (Save As).

        Args:
            project: Project handle.
            path: Destination file path.
        """
        pass

    def NewProject(self) -> ProjectPtr:
        """Create a new empty project.

        Returns:
            Handle to the new project.
        """
        pass

    def OpenProjectFromPath(self, path: str) -> ProjectPtr:
        """Open a project from a file path.

        Args:
            path: Path to the .aep file.

        Returns:
            Handle to the opened project.
        """
        pass

    def GetProjectBitDepth(self, project: ProjectPtr) -> ProjBitDepth:
        """Get the project color bit depth.

        Args:
            project: Project handle.

        Returns:
            The project bit depth.
        """
        pass

    def SetProjectBitDepth(self, project: ProjectPtr, bitDepth: ProjBitDepth):
        """Set the project color bit depth.

        Args:
            project: Project handle.
            bitDepth: New bit depth.
        """
        pass

class ItemSuite:
    """Suite for project item operations.

    Provides methods to query, modify, and manage project items
    (folders, compositions, footage, and solids).

    Examples:
        >>> suite = PyFx.ItemSuite()
        >>> item = suite.GetActiveItem()
        >>> name = suite.GetItemName(item)
    """

    def __init__(self):
        pass

    def GetFirstProjItem(self, project: ProjectPtr) -> ItemPtr:
        """Get the first item in the project.

        Args:
            project: Project handle.

        Returns:
            Handle to the first item.
        """
        pass

    def GetNextProjItem(self, project: ProjectPtr, item: ItemPtr) -> ItemPtr:
        """Get the next item after the given item.

        Args:
            project: Project handle.
            item: Current item handle.

        Returns:
            Handle to the next item, or None if at end.
        """
        pass

    def GetActiveItem(self) -> ItemPtr:
        """Get the currently active (selected) item.

        Returns:
            Handle to the active item.
        """
        pass

    def IsItemSelected(self, item: ItemPtr) -> bool:
        """Check if an item is selected.

        Args:
            item: Item handle.

        Returns:
            True if the item is selected.
        """
        pass

    def SelectItem(self, item: ItemPtr, select: bool, deselectOthers: bool):
        """Select or deselect an item.

        Args:
            item: Item handle.
            select: True to select, False to deselect.
            deselectOthers: True to deselect all other items first.
        """
        pass

    def GetItemType(self, item: ItemPtr) -> ItemType:
        """Get the type of a project item.

        Args:
            item: Item handle.

        Returns:
            The item type.
        """
        pass

    def GetTypeName(self, itemType: ItemType) -> str:
        """Get the display name for an item type.

        Args:
            itemType: The item type enum.

        Returns:
            The human-readable type name.
        """
        pass

    def GetItemName(self, item: ItemPtr) -> str:
        """Get the name of an item.

        Args:
            item: Item handle.

        Returns:
            The item name.
        """
        pass

    def SetItemName(self, item: ItemPtr, name: str):
        """Set the name of an item.

        Args:
            item: Item handle.
            name: New name.
        """
        pass

    def GetItemID(self, item: ItemPtr) -> int:
        """Get the unique ID of an item.

        Args:
            item: Item handle.

        Returns:
            The item ID.
        """
        pass

    def GetItemFlags(self, item: ItemPtr) -> ItemFlag:
        """Get the flags of an item.

        Args:
            item: Item handle.

        Returns:
            The item flags.
        """
        pass

    def SetItemUseProxy(self, item: ItemPtr, useProxy: bool):
        """Set whether an item uses its proxy.

        Args:
            item: Item handle.
            useProxy: True to use proxy.
        """
        pass

    def GetItemParentFolder(self, item: ItemPtr) -> ItemPtr:
        """Get the parent folder of an item.

        Args:
            item: Item handle.

        Returns:
            Handle to the parent folder item.
        """
        pass

    def SetItemParentFolder(self, item: ItemPtr, parentFolder: ItemPtr):
        """Move an item to a different folder.

        Args:
            item: Item handle.
            parentFolder: Destination folder handle.
        """
        pass

    def GetItemDuration(self, item: ItemPtr) -> Time:
        """Get the duration of an item.

        Args:
            item: Item handle.

        Returns:
            The item duration.
        """
        pass

    def GetItemCurrentTime(self, item: ItemPtr) -> Time:
        """Get the current time indicator position for an item.

        Args:
            item: Item handle.

        Returns:
            The current time.
        """
        pass

    def GetItemDimensions(self, item: ItemPtr) -> Tuple[int, int]:
        """Get the pixel dimensions of an item.

        Args:
            item: Item handle.

        Returns:
            A (width, height) tuple.
        """
        pass

    def GetItemPixelAspectRatio(self, item: ItemPtr) -> Ratio:
        """Get the pixel aspect ratio of an item.

        Args:
            item: Item handle.

        Returns:
            The pixel aspect ratio.
        """
        pass

    def DeleteItem(self, item: ItemPtr):
        """Delete an item from the project.

        Args:
            item: Item handle.
        """
        pass

    def CreateNewFolder(self, name: str, parentFolder: ItemPtr) -> ItemPtr:
        """Create a new folder in the project.

        Args:
            name: Folder name.
            parentFolder: Parent folder handle.

        Returns:
            Handle to the new folder item.
        """
        pass

    def SetItemCurrentTime(self, item: ItemPtr, newTime: Time):
        """Set the current time indicator for an item.

        Args:
            item: Item handle.
            newTime: New time value.
        """
        pass

    def GetItemComment(self, item: ItemPtr) -> str:
        """Get the comment of an item.

        Args:
            item: Item handle.

        Returns:
            The comment string.
        """
        pass

    def SetItemComment(self, item: ItemPtr, comment: str):
        """Set the comment of an item.

        Args:
            item: Item handle.
            comment: New comment string.
        """
        pass

    def GetItemLabel(self, item: ItemPtr) -> Label:
        """Get the label color of an item.

        Args:
            item: Item handle.

        Returns:
            The label color.
        """
        pass

    def SetItemLabel(self, item: ItemPtr, label: Label):
        """Set the label color of an item.

        Args:
            item: Item handle.
            label: New label color.
        """
        pass

    def GetItemMRUView(self, item: ItemPtr) -> ItemViewPtr:
        """Get the most recently used view for an item.

        Args:
            item: Item handle.

        Returns:
            Handle to the item view.
        """
        pass

    def GetItemViewPlaybackTime(
        self, itemView: ItemViewPtr
    ) -> Tuple[Time, bool]:
        """Get the playback time of an item view.

        Args:
            itemView: Item view handle.

        Returns:
            A (time, is_valid) tuple.
        """
        pass

class SoundDataSuite:
    """Suite for working with audio/sound data.

    Provides methods to create and inspect sound data buffers.

    Examples:
        >>> suite = PyFx.SoundDataSuite()
        >>> fmt = PyFx.SoundDataFormat(44100.0, PyFx.SoundEncoding.FLOAT, 4, 2)
        >>> sound = suite.NewSoundData(fmt)
    """

    def __init__(self):
        pass

    def NewSoundData(self, soundFormat: SoundDataFormat) -> SoundDataPtr:
        """Create a new sound data buffer.

        Args:
            soundFormat: Audio format specification.

        Returns:
            Handle to the new sound data.
        """
        pass

    def GetSoundDataFormat(self, soundData: SoundDataPtr) -> SoundDataFormat:
        """Get the format of a sound data buffer.

        Args:
            soundData: Sound data handle.

        Returns:
            The sound data format.
        """
        pass

    def LockSoundDataSamples(self, soundData: SoundDataPtr) -> Tuple:
        """Lock sound data samples for direct access.

        Args:
            soundData: Sound data handle.

        Returns:
            The locked sample data.
        """
        pass

    def UnlockSoundDataSamples(self, soundData: SoundDataPtr):
        """Unlock previously locked sound data samples.

        Args:
            soundData: Sound data handle.
        """
        pass

    def GetNumSamples(self, soundData: SoundDataPtr) -> int:
        """Get the number of audio samples.

        Args:
            soundData: Sound data handle.

        Returns:
            The number of samples.
        """
        pass

class CompSuite:
    """Suite for composition operations.

    Provides methods to create, query, and modify compositions,
    including creating layers, managing work areas, and setting
    rendering options.

    Examples:
        >>> suite = PyFx.CompSuite()
        >>> comp = suite.GetMostRecentlyUsedComp()
        >>> fps = suite.GetCompFramerate(comp)
    """

    def __init__(self):
        pass

    def GetCompFromItem(self, item: ItemPtr) -> CompPtr:
        """Get the composition handle from an item.

        Args:
            item: Item handle (must be a comp item).

        Returns:
            The composition handle.
        """
        pass

    def GetItemFromComp(self, comp: CompPtr) -> ItemPtr:
        """Get the project item for a composition.

        Args:
            comp: Composition handle.

        Returns:
            The item handle.
        """
        pass

    def GetCompDownsampleFactor(self, comp: CompPtr) -> DownsampleFactor:
        """Get the composition downsample factor.

        Args:
            comp: Composition handle.

        Returns:
            The downsample factor.
        """
        pass

    def SetCompDownsampleFactor(self, comp: CompPtr, factor: DownsampleFactor):
        """Set the composition downsample factor.

        Args:
            comp: Composition handle.
            factor: New downsample factor.
        """
        pass

    def GetCompBGColor(self, comp: CompPtr) -> ColorVal:
        """Get the composition background color.

        Args:
            comp: Composition handle.

        Returns:
            The background color.
        """
        pass

    def SetCompBGColor(self, comp: CompPtr, color: ColorVal):
        """Set the composition background color.

        Args:
            comp: Composition handle.
            color: New background color.
        """
        pass

    def GetCompFlags(self, comp: CompPtr) -> CompFlag:
        """Get the composition flags.

        Args:
            comp: Composition handle.

        Returns:
            The composition flags.
        """
        pass

    def GetShowLayerNameOrSourceName(self, comp: CompPtr) -> bool:
        """Check if comp shows layer names or source names.

        Args:
            comp: Composition handle.

        Returns:
            True if showing layer names.
        """
        pass

    def SetShowLayerNameOrSourceName(self, comp: CompPtr, showLayerName: bool):
        """Set whether to show layer names or source names.

        Args:
            comp: Composition handle.
            showLayerName: True for layer names, False for source names.
        """
        pass

    def GetShowBlendModes(self, comp: CompPtr) -> bool:
        """Check if blend modes column is visible.

        Args:
            comp: Composition handle.

        Returns:
            True if blend modes are shown.
        """
        pass

    def SetShowBlendModes(self, comp: CompPtr, showBlendModes: bool):
        """Set blend modes column visibility.

        Args:
            comp: Composition handle.
            showBlendModes: True to show blend modes.
        """
        pass

    def GetCompFramerate(self, comp: CompPtr) -> float:
        """Get the composition frame rate.

        Args:
            comp: Composition handle.

        Returns:
            Frames per second.
        """
        pass

    def SetCompFrameRate(self, comp: CompPtr, fps: float):
        """Set the composition frame rate.

        Args:
            comp: Composition handle.
            fps: New frame rate.
        """
        pass

    def GetCompShutterAnglePhase(self, comp: CompPtr) -> Tuple[Ratio, Ratio]:
        """Get the shutter angle and phase for motion blur.

        Args:
            comp: Composition handle.

        Returns:
            A (shutter_angle, shutter_phase) tuple of ratios.
        """
        pass

    def GetCompShutterFrameRange(
        self, comp: CompPtr, compTime: Time
    ) -> Tuple[Time, Time]:
        """Get the shutter frame range at a given time.

        Args:
            comp: Composition handle.
            compTime: Time to query.

        Returns:
            A (start, end) time tuple.
        """
        pass

    def GetCompSuggestedMotionBlurSamples(self, comp: CompPtr) -> int:
        """Get the suggested motion blur sample count.

        Args:
            comp: Composition handle.

        Returns:
            Number of samples.
        """
        pass

    def SetCompSuggestedMotionBlurSamples(self, comp: CompPtr, samples: int):
        """Set the suggested motion blur sample count.

        Args:
            comp: Composition handle.
            samples: Number of samples.
        """
        pass

    def GetCompMotionBlurAdaptiveSampleLimit(self, comp: CompPtr) -> int:
        """Get the adaptive motion blur sample limit.

        Args:
            comp: Composition handle.

        Returns:
            Maximum number of samples.
        """
        pass

    def SetCompMotionBlurAdaptiveSampleLimit(self, comp: CompPtr, samples: int):
        """Set the adaptive motion blur sample limit.

        Args:
            comp: Composition handle.
            samples: Maximum number of samples.
        """
        pass

    def GetCompWorkAreaStart(self, comp: CompPtr) -> Time:
        """Get the work area start time.

        Args:
            comp: Composition handle.

        Returns:
            Work area start time.
        """
        pass

    def GetCompWorkAreaDuration(self, comp: CompPtr) -> Time:
        """Get the work area duration.

        Args:
            comp: Composition handle.

        Returns:
            Work area duration.
        """
        pass

    def SetCompWorkAreaStartAndDuration(
        self, comp: CompPtr, workAreaStart: Time, workAreaDuration: Time
    ):
        """Set the work area start time and duration.

        Args:
            comp: Composition handle.
            workAreaStart: Start time.
            workAreaDuration: Duration.
        """
        pass

    def CreateSolidInComp(
        self,
        comp: CompPtr,
        name: str,
        width: int,
        height: int,
        color: ColorVal,
        duration: Time,
    ) -> LayerPtr:
        """Create a solid layer in a composition.

        Args:
            comp: Composition handle.
            name: Layer name.
            width: Solid width in pixels.
            height: Solid height in pixels.
            color: Solid color.
            duration: Layer duration.

        Returns:
            Handle to the new layer.
        """
        pass

    def CreateCameraInComp(
        self, comp: CompPtr, name: str, centerPoint: FloatPoint
    ) -> LayerPtr:
        """Create a camera layer in a composition.

        Args:
            comp: Composition handle.
            name: Camera name.
            centerPoint: Initial center position.

        Returns:
            Handle to the new camera layer.
        """
        pass

    def CreateLightInComp(
        self, comp: CompPtr, name: str, centerPoint: FloatPoint
    ) -> LayerPtr:
        """Create a light layer in a composition.

        Args:
            comp: Composition handle.
            name: Light name.
            centerPoint: Initial center position.

        Returns:
            Handle to the new light layer.
        """
        pass

    def CreateComp(
        self,
        parentFolder: ItemPtr,
        name: str,
        width: int,
        height: int,
        pixelAspectRatio: Ratio,
        duration: Time,
        framerate: Ratio,
    ) -> CompPtr:
        """Create a new composition.

        Args:
            parentFolder: Folder to create the comp in.
            name: Composition name.
            width: Width in pixels.
            height: Height in pixels.
            pixelAspectRatio: Pixel aspect ratio.
            duration: Composition duration.
            framerate: Frame rate as a ratio.

        Returns:
            Handle to the new composition.
        """
        pass

    def GetCompDisplayStartTime(self, comp: CompPtr) -> Time:
        """Get the composition display start time.

        Args:
            comp: Composition handle.

        Returns:
            The display start time.
        """
        pass

    def SetCompDisplayStartTime(self, comp: CompPtr, startTime: Time):
        """Set the composition display start time.

        Args:
            comp: Composition handle.
            startTime: New display start time.
        """
        pass

    def SetCompDuration(self, comp: CompPtr, duration: Time):
        """Set the composition duration.

        Args:
            comp: Composition handle.
            duration: New duration.
        """
        pass

    def SetCompDimensions(self, comp: CompPtr, width: int, height: int):
        """Set the composition dimensions.

        Args:
            comp: Composition handle.
            width: New width in pixels.
            height: New height in pixels.
        """
        pass

    def SetCompPixelAspectRatio(self, comp: CompPtr, pixelAspectRatio: Ratio):
        """Set the composition pixel aspect ratio.

        Args:
            comp: Composition handle.
            pixelAspectRatio: New pixel aspect ratio.
        """
        pass

    def CreateTextLayerInComp(
        self, comp: CompPtr, newLayer: bool = True
    ) -> LayerPtr:
        """Create a point text layer in a composition.

        Args:
            comp: Composition handle.
            newLayer: Whether to create a new layer.

        Returns:
            Handle to the new text layer.
        """
        pass

    def CreateBoxTextLayerInComp(
        self, comp: CompPtr, boxDimensions: FloatPoint, newLayer: bool = True
    ) -> LayerPtr:
        """Create a box (paragraph) text layer in a composition.

        Args:
            comp: Composition handle.
            boxDimensions: Box width and height.
            newLayer: Whether to create a new layer.

        Returns:
            Handle to the new text layer.
        """
        pass

    def CreateNullInComp(
        self, comp: CompPtr, name: str, duration: Time
    ) -> LayerPtr:
        """Create a null object layer in a composition.

        Args:
            comp: Composition handle.
            name: Null layer name.
            duration: Layer duration.

        Returns:
            Handle to the new null layer.
        """
        pass

    def DuplicateComp(self, comp: CompPtr) -> CompPtr:
        """Duplicate a composition.

        Args:
            comp: Composition handle.

        Returns:
            Handle to the duplicate composition.
        """
        pass

    def GetCompFrameDuration(self, comp: CompPtr) -> Time:
        """Get the duration of a single frame.

        Args:
            comp: Composition handle.

        Returns:
            The frame duration.
        """
        pass

    def GetMostRecentlyUsedComp(self) -> CompPtr:
        """Get the most recently used (active) composition.

        Returns:
            Handle to the MRU composition.
        """
        pass

    def CreateVectorLayerInComp(self, comp: CompPtr) -> LayerPtr:
        """Create a shape (vector) layer in a composition.

        Args:
            comp: Composition handle.

        Returns:
            Handle to the new shape layer.
        """
        pass

    def GetNewCompMarkerStream(self, parentComp: CompPtr) -> StreamRefPtr:
        """Get the marker stream for a composition.

        Args:
            parentComp: Composition handle.

        Returns:
            Handle to the comp marker stream.
        """
        pass

    def GetCompDisplayDropFrame(self, comp: CompPtr) -> bool:
        """Check if the composition uses drop-frame timecode.

        Args:
            comp: Composition handle.

        Returns:
            True if using drop-frame.
        """
        pass

    def SetCompDisplayDropFrame(self, comp: CompPtr, dropFrame: bool):
        """Set whether the composition uses drop-frame timecode.

        Args:
            comp: Composition handle.
            dropFrame: True for drop-frame.
        """
        pass

class LayerSuite:
    """Suite for layer operations.

    Provides methods to query, modify, create, and delete layers in
    compositions, including timing, flags, transforms, and parenting.

    Examples:
        >>> suite = PyFx.LayerSuite()
        >>> count = suite.GetCompNumLayers(comp)
        >>> layer = suite.GetCompLayerByIndex(comp, 0)
        >>> name, source_name = suite.GetLayerName(layer)
    """

    def __init__(self):
        pass

    def GetCompNumLayers(self, comp: CompPtr) -> int:
        """Get the number of layers in a composition.

        Args:
            comp: Composition handle.

        Returns:
            The layer count.
        """
        pass

    def GetCompLayerByIndex(self, comp: CompPtr, layerIndex: int) -> LayerPtr:
        """Get a layer by its index in the composition.

        Args:
            comp: Composition handle.
            layerIndex: Zero-based layer index.

        Returns:
            Handle to the layer.
        """
        pass

    def GetActiveLayer(self) -> LayerPtr:
        """Get the currently active (selected) layer.

        Returns:
            Handle to the active layer.
        """
        pass

    def GetLayerIndex(self, layer: LayerPtr) -> int:
        """Get the index of a layer in its composition.

        Args:
            layer: Layer handle.

        Returns:
            The zero-based layer index.
        """
        pass

    def GetLayerSourceItem(self, layer: LayerPtr) -> ItemPtr:
        """Get the source item of a layer.

        Args:
            layer: Layer handle.

        Returns:
            Handle to the source item.
        """
        pass

    def GetLayerSourceItemID(self, layer: LayerPtr) -> int:
        """Get the source item ID of a layer.

        Args:
            layer: Layer handle.

        Returns:
            The source item ID.
        """
        pass

    def GetLayerParentComp(self, layer: LayerPtr) -> CompPtr:
        """Get the parent composition of a layer.

        Args:
            layer: Layer handle.

        Returns:
            Handle to the parent composition.
        """
        pass

    def GetLayerName(self, layer: LayerPtr) -> Tuple[str, str]:
        """Get the layer name and source name.

        Args:
            layer: Layer handle.

        Returns:
            A (layer_name, source_name) tuple.
        """
        pass

    def GetLayerQuality(self, layer: LayerPtr) -> LayerQual:
        """Get the render quality of a layer.

        Args:
            layer: Layer handle.

        Returns:
            The layer quality setting.
        """
        pass

    def SetLayerQuality(self, layer: LayerPtr, quality: LayerQual):
        """Set the render quality of a layer.

        Args:
            layer: Layer handle.
            quality: New quality setting.
        """
        pass

    def GetLayerFlags(self, layer: LayerPtr) -> LayerFlag:
        """Get all flags for a layer.

        Args:
            layer: Layer handle.

        Returns:
            The layer flags.
        """
        pass

    def SetLayerFlag(self, layer: LayerPtr, singleFlag: LayerFlag, value: bool):
        """Set a single flag on a layer.

        Args:
            layer: Layer handle.
            singleFlag: Which flag to set.
            value: Flag value.
        """
        pass

    def IsLayerVideoReallyOn(self, layer: LayerPtr) -> bool:
        """Check if the layer video is actually rendering.

        Args:
            layer: Layer handle.

        Returns:
            True if video is active.
        """
        pass

    def IsLayerAudioReallyOn(self, layer: LayerPtr) -> bool:
        """Check if the layer audio is actually active.

        Args:
            layer: Layer handle.

        Returns:
            True if audio is active.
        """
        pass

    def GetLayerCurrentTime(self, layer: LayerPtr, timeMode: LTimeMode) -> Time:
        """Get the current time of a layer.

        Args:
            layer: Layer handle.
            timeMode: Layer time or comp time.

        Returns:
            The current time.
        """
        pass

    def GetLayerInPoint(self, layer: LayerPtr, timeMode: LTimeMode) -> Time:
        """Get the in point of a layer.

        Args:
            layer: Layer handle.
            timeMode: Layer time or comp time.

        Returns:
            The in point time.
        """
        pass

    def GetLayerDuration(self, layer: LayerPtr, timeMode: LTimeMode) -> Time:
        """Get the duration of a layer.

        Args:
            layer: Layer handle.
            timeMode: Layer time or comp time.

        Returns:
            The layer duration.
        """
        pass

    def SetLayerInPointAndDuration(
        self,
        layer: LayerPtr,
        timeMode: LTimeMode,
        inPoint: Time,
        duration: Time,
    ):
        """Set the in point and duration of a layer.

        Args:
            layer: Layer handle.
            timeMode: Layer time or comp time.
            inPoint: New in point.
            duration: New duration.
        """
        pass

    def GetLayerOffset(self, layer: LayerPtr) -> Time:
        """Get the layer start time offset.

        Args:
            layer: Layer handle.

        Returns:
            The time offset.
        """
        pass

    def SetLayerOffset(self, layer: LayerPtr, offset: Time):
        """Set the layer start time offset.

        Args:
            layer: Layer handle.
            offset: New time offset.
        """
        pass

    def GetLayerStretch(self, layer: LayerPtr) -> Ratio:
        """Get the layer time stretch factor.

        Args:
            layer: Layer handle.

        Returns:
            The stretch ratio.
        """
        pass

    def SetLayerStretch(self, layer: LayerPtr, stretch: Ratio):
        """Set the layer time stretch factor.

        Args:
            layer: Layer handle.
            stretch: New stretch ratio.
        """
        pass

    def GetLayerTransferMode(
        self, layer: LayerPtr
    ) -> Tuple[TransferFlags, TrackMatte]:
        """Get the layer blending mode and track matte settings.

        Args:
            layer: Layer handle.

        Returns:
            A (transfer_flags, track_matte) tuple.
        """
        pass

    def SetLayerTransferMode(
        self, layer: LayerPtr, flags: TransferFlags, trackMatte: TrackMatte
    ):
        """Set the layer blending mode and track matte.

        Args:
            layer: Layer handle.
            flags: Transfer flags.
            trackMatte: Track matte mode.
        """
        pass

    def IsAddLayerValid(self, itemToAdd: ItemPtr, intoComp: CompPtr) -> bool:
        """Check if adding an item as a layer is valid.

        Args:
            itemToAdd: Item handle to add.
            intoComp: Target composition handle.

        Returns:
            True if the operation is valid.
        """
        pass

    def AddLayer(self, itemToAdd: ItemPtr, intoComp: CompPtr) -> LayerPtr:
        """Add an item as a new layer in a composition.

        Args:
            itemToAdd: Item handle to add.
            intoComp: Target composition handle.

        Returns:
            Handle to the new layer.
        """
        pass

    def ReorderLayer(self, layer: LayerPtr, layerIndex: int):
        """Move a layer to a new index in the layer stack.

        Args:
            layer: Layer handle.
            layerIndex: New zero-based index.
        """
        pass

    def GetLayerMaskedBounds(
        self, layer: LayerPtr, timeMode: LTimeMode, time: Time
    ) -> FloatRect:
        """Get the masked bounding rectangle of a layer.

        Args:
            layer: Layer handle.
            timeMode: Layer time or comp time.
            time: Time to evaluate.

        Returns:
            The bounding rectangle.
        """
        pass

    def GetLayerObjectType(self, layer: LayerPtr) -> ObjectType:
        """Get the object type of a layer.

        Args:
            layer: Layer handle.

        Returns:
            The layer object type (AV, camera, light, text, vector).
        """
        pass

    def IsLayer3D(self, layer: LayerPtr) -> bool:
        """Check if a layer is 3D.

        Args:
            layer: Layer handle.

        Returns:
            True if the layer is 3D.
        """
        pass

    def IsLayer2D(self, layer: LayerPtr) -> bool:
        """Check if a layer is 2D.

        Args:
            layer: Layer handle.

        Returns:
            True if the layer is 2D.
        """
        pass

    def IsVideoActive(
        self, layer: LayerPtr, timeMode: LTimeMode, time: Time
    ) -> bool:
        """Check if a layer's video is active at a given time.

        Args:
            layer: Layer handle.
            timeMode: Layer time or comp time.
            time: Time to check.

        Returns:
            True if video is active.
        """
        pass

    def IsLayerUsedAsTrackMatte(
        self, layer: LayerPtr, fillMustBeActive: bool
    ) -> bool:
        """Check if a layer is used as a track matte.

        Args:
            layer: Layer handle.
            fillMustBeActive: Whether the fill layer must be active.

        Returns:
            True if used as track matte.
        """
        pass

    def DoesLayerHaveTrackMatte(self, layer: LayerPtr) -> bool:
        """Check if a layer has a track matte.

        Args:
            layer: Layer handle.

        Returns:
            True if the layer has a track matte.
        """
        pass

    def ConvertCompToLayerTime(self, layer: LayerPtr, compTime: Time) -> Time:
        """Convert composition time to layer time.

        Args:
            layer: Layer handle.
            compTime: Time in composition coordinates.

        Returns:
            The equivalent layer time.
        """
        pass

    def ConvertLayerToCompTime(self, layer: LayerPtr, layerTime: Time) -> Time:
        """Convert layer time to composition time.

        Args:
            layer: Layer handle.
            layerTime: Time in layer coordinates.

        Returns:
            The equivalent composition time.
        """
        pass

    def GetLayerDancingRandValue(self, layer: LayerPtr, compTime: Time) -> int:
        """Get the randomized value for the layer (for dancing dissolve).

        Args:
            layer: Layer handle.
            compTime: Time to query.

        Returns:
            The random value.
        """
        pass

    def GetLayerID(self, layer: LayerPtr) -> int:
        """Get the unique ID of a layer.

        Args:
            layer: Layer handle.

        Returns:
            The layer ID.
        """
        pass

    def GetLayerToWorldXform(self, layer: LayerPtr, compTime: Time) -> Matrix4:
        """Get the layer-to-world transformation matrix.

        Args:
            layer: Layer handle.
            compTime: Time to evaluate.

        Returns:
            The 4x4 transformation matrix.
        """
        pass

    def GetLayerToWorldXformFromView(
        self, layer: LayerPtr, viewTime: Time, compTime: Time
    ) -> Matrix4:
        """Get the layer-to-world transform from a specific view.

        Args:
            layer: Layer handle.
            viewTime: View time.
            compTime: Composition time.

        Returns:
            The 4x4 transformation matrix.
        """
        pass

    def SetLayerName(self, layer: LayerPtr, newName: str):
        """Set the display name of a layer.

        Args:
            layer: Layer handle.
            newName: New layer name.
        """
        pass

    def GetLayerParent(self, layer: LayerPtr) -> LayerPtr:
        """Get the parent layer.

        Args:
            layer: Layer handle.

        Returns:
            Handle to the parent layer.
        """
        pass

    def SetLayerParent(self, layer: LayerPtr, parentLayer: LayerPtr):
        """Set the parent layer.

        Args:
            layer: Layer handle.
            parentLayer: Parent layer handle.
        """
        pass

    def DeleteLayer(self, layer: LayerPtr):
        """Delete a layer from its composition.

        Args:
            layer: Layer handle.
        """
        pass

    def DuplicateLayer(self, origLayer: LayerPtr) -> LayerPtr:
        """Duplicate a layer.

        Args:
            origLayer: Layer handle to duplicate.

        Returns:
            Handle to the new layer.
        """
        pass

    def GetLayerFromLayerID(self, parentComp: CompPtr, id: int) -> LayerPtr:
        """Get a layer by its ID within a composition.

        Args:
            parentComp: Composition handle.
            id: Layer ID.

        Returns:
            Handle to the layer.
        """
        pass

    def GetLayerLabel(self, layer: LayerPtr) -> Label:
        """Get the label color of a layer.

        Args:
            layer: Layer handle.

        Returns:
            The label color.
        """
        pass

    def SetLayerLabel(self, layer: LayerPtr, label: Label):
        """Set the label color of a layer.

        Args:
            layer: Layer handle.
            label: New label color.
        """
        pass

    def GetLayerSamplingQuality(self, layer: LayerPtr) -> LayerSamplingQual:
        """Get the sampling quality of a layer.

        Args:
            layer: Layer handle.

        Returns:
            The sampling quality.
        """
        pass

    def SetLayerSamplingQuality(
        self, layer: LayerPtr, quality: LayerSamplingQual
    ):
        """Set the sampling quality of a layer.

        Args:
            layer: Layer handle.
            quality: New sampling quality.
        """
        pass

    def GetTrackMatteLayer(self, layer: LayerPtr) -> LayerPtr:
        """Get the track matte layer for a layer.

        Args:
            layer: Layer handle.

        Returns:
            Handle to the track matte layer.
        """
        pass

    def SetTrackMatte(
        self,
        layer: LayerPtr,
        trackMatteLayer: LayerPtr,
        trackMatteType: TrackMatte,
    ):
        """Set the track matte for a layer.

        Args:
            layer: Layer handle.
            trackMatteLayer: Track matte layer handle.
            trackMatteType: Track matte type.
        """
        pass

    def RemoveTrackMatte(self, layer: LayerPtr):
        """Remove the track matte from a layer.

        Args:
            layer: Layer handle.
        """
        pass

class StreamSuite:
    """Suite for property stream operations.

    Provides methods to access layer and effect property streams,
    get/set stream values, and query stream metadata.

    Examples:
        >>> suite = PyFx.StreamSuite()
        >>> stream = suite.GetNewLayerStream(layer, PyFx.LayerStream.POSITION)
        >>> value = suite.GetNewStreamValue(
        ...     stream, PyFx.LTimeMode.CompTime, time, False
        ... )
    """

    def __init__(self):
        pass

    def IsStreamLegal(self, layer: LayerPtr, whichStream: LayerStream) -> bool:
        """Check if a stream type is valid for a layer.

        Args:
            layer: Layer handle.
            whichStream: Stream identifier.

        Returns:
            True if the stream is legal for this layer.
        """
        pass

    def CanVaryOverTime(self, stream: StreamRefPtr) -> bool:
        """Check if a stream can be keyframed.

        Args:
            stream: Stream handle.

        Returns:
            True if the stream supports keyframes.
        """
        pass

    def GetValidInterpolations(self, stream: StreamRefPtr) -> KeyInterpMask:
        """Get the valid interpolation types for a stream.

        Args:
            stream: Stream handle.

        Returns:
            Bitmask of valid interpolation types.
        """
        pass

    def GetNewLayerStream(
        self, layer: LayerPtr, whichStream: LayerStream
    ) -> StreamRefPtr:
        """Get a built-in layer property stream.

        Args:
            layer: Layer handle.
            whichStream: Stream identifier.

        Returns:
            Handle to the stream.
        """
        pass

    def GetEffectNumParamStreams(self, effectRef: EffectRefPtr) -> int:
        """Get the number of parameter streams on an effect.

        Args:
            effectRef: Effect handle.

        Returns:
            The parameter count.
        """
        pass

    def GetNewEffectStreamByIndex(
        self, effectRef: EffectRefPtr, paramIndex: int
    ) -> StreamRefPtr:
        """Get an effect parameter stream by index.

        Args:
            effectRef: Effect handle.
            paramIndex: Zero-based parameter index.

        Returns:
            Handle to the parameter stream.
        """
        pass

    def GetNewMaskStream(
        self, maskRef: MaskRefPtr, whichStream: MaskStream
    ) -> StreamRefPtr:
        """Get a mask property stream.

        Args:
            maskRef: Mask handle.
            whichStream: Mask stream identifier.

        Returns:
            Handle to the stream.
        """
        pass

    def GetStreamName(self, stream: StreamRefPtr, forceEnglish: bool) -> str:
        """Get the display name of a stream.

        Args:
            stream: Stream handle.
            forceEnglish: True to get the English name.

        Returns:
            The stream name.
        """
        pass

    def GetStreamUnitsText(
        self, stream: StreamRefPtr, forceEnglish: bool
    ) -> str:
        """Get the units text for a stream (e.g., "pixels").

        Args:
            stream: Stream handle.
            forceEnglish: True to get English units.

        Returns:
            The units string.
        """
        pass

    def GetStreamProperties(
        self, stream: StreamRefPtr
    ) -> Tuple[StreamFlag, float, float]:
        """Get stream properties (flags, min, max).

        Args:
            stream: Stream handle.

        Returns:
            A (flags, min_value, max_value) tuple.
        """
        pass

    def IsStreamTimevarying(self, stream: StreamRefPtr) -> bool:
        """Check if a stream has keyframes.

        Args:
            stream: Stream handle.

        Returns:
            True if the stream varies over time.
        """
        pass

    def GetStreamType(self, stream: StreamRefPtr) -> StreamType:
        """Get the data type of a stream.

        Args:
            stream: Stream handle.

        Returns:
            The stream type.
        """
        pass

    def GetNewStreamValue(
        self,
        stream: StreamRefPtr,
        timeMode: LTimeMode,
        time: Time,
        preExpression: bool,
    ) -> StreamValue2:
        """Get the value of a stream at a given time.

        Args:
            stream: Stream handle.
            timeMode: Layer time or comp time.
            time: Time to evaluate.
            preExpression: True to get value before expressions.

        Returns:
            The stream value.
        """
        pass

    def SetStreamValue(self, stream: StreamRefPtr, value: StreamValue2):
        """Set the static value of a stream.

        Args:
            stream: Stream handle.
            value: New stream value.
        """
        pass

    def DuplicateStreamRef(self, stream: StreamRefPtr) -> StreamRefPtr:
        """Duplicate a stream reference.

        Args:
            stream: Stream handle.

        Returns:
            A new handle to the same stream.
        """
        pass

    def GetUniqueStreamID(self, stream: StreamRefPtr) -> int:
        """Get the unique ID of a stream.

        Args:
            stream: Stream handle.

        Returns:
            The stream ID.
        """
        pass

class DynamicStreamSuite:
    """Suite for navigating and manipulating the property hierarchy.

    Provides methods to traverse the stream tree, access groups and
    children by index or match name, and manage dimension separation.

    Examples:
        >>> suite = PyFx.DynamicStreamSuite()
        >>> root = suite.GetNewStreamRefForLayer(layer)
        >>> count = suite.GetNumStreamsInGroup(root)
        >>> child = suite.GetNewStreamRefByIndex(root, 0)
    """

    def __init__(self):
        pass

    def GetNewStreamRefForLayer(self, layer: LayerPtr) -> StreamRefPtr:
        """Get the root stream group for a layer.

        Args:
            layer: Layer handle.

        Returns:
            Handle to the root stream.
        """
        pass

    def GetNewStreamRefForMask(self, mask: MaskRefPtr) -> StreamRefPtr:
        """Get the root stream group for a mask.

        Args:
            mask: Mask handle.

        Returns:
            Handle to the root stream.
        """
        pass

    def GetStreamDepth(self, stream: StreamRefPtr) -> int:
        """Get the nesting depth of a stream in the hierarchy.

        Args:
            stream: Stream handle.

        Returns:
            The depth level (0 = root).
        """
        pass

    def GetStreamGroupingType(self, stream: StreamRefPtr) -> StreamGroupingType:
        """Get the grouping type of a stream.

        Args:
            stream: Stream handle.

        Returns:
            The grouping type (leaf, named group, or indexed group).
        """
        pass

    def GetNumStreamsInGroup(self, stream: StreamRefPtr) -> int:
        """Get the number of child streams in a group.

        Args:
            stream: Stream group handle.

        Returns:
            The child count.
        """
        pass

    def GetDynamicStreamFlags(self, stream: StreamRefPtr) -> DynStreamFlag:
        """Get the dynamic flags of a stream.

        Args:
            stream: Stream handle.

        Returns:
            The dynamic stream flags.
        """
        pass

    def SetDynamicStreamFlag(
        self,
        stream: StreamRefPtr,
        oneFlag: DynStreamFlag,
        undoable: bool,
        set: bool,
    ):
        """Set a dynamic stream flag.

        Args:
            stream: Stream handle.
            oneFlag: Which flag to set.
            undoable: Whether the change is undoable.
            set: Flag value.
        """
        pass

    def GetNewStreamRefByIndex(
        self, parentGroup: StreamRefPtr, index: int
    ) -> StreamRefPtr:
        """Get a child stream by index within a group.

        Args:
            parentGroup: Parent stream group handle.
            index: Zero-based child index.

        Returns:
            Handle to the child stream.
        """
        pass

    def GetNewStreamRefByMatchname(
        self, parentGroup: StreamRefPtr, matchName: str
    ) -> StreamRefPtr:
        """Get a child stream by match name within a group.

        Args:
            parentGroup: Parent stream group handle.
            matchName: The match name string.

        Returns:
            Handle to the child stream.
        """
        pass

    def DeleteStream(self, stream: StreamRefPtr):
        """Delete a stream from its parent group.

        Args:
            stream: Stream handle to delete.
        """
        pass

    def ReorderStream(self, stream: StreamRefPtr, newIndex: int):
        """Move a stream to a new index within its group.

        Args:
            stream: Stream handle.
            newIndex: New zero-based index.
        """
        pass

    def DuplicateStream(self, stream: StreamRefPtr) -> int:
        """Duplicate a stream.

        Args:
            stream: Stream handle.

        Returns:
            The index of the new stream.
        """
        pass

    def SetStreamName(self, stream: StreamRefPtr, newName: str):
        """Set the display name of a stream.

        Args:
            stream: Stream handle.
            newName: New display name.
        """
        pass

    def CanAddStream(self, parentGroup: StreamRefPtr, matchName: str) -> bool:
        """Check if a stream can be added to a group.

        Args:
            parentGroup: Parent stream group handle.
            matchName: Match name of the stream to add.

        Returns:
            True if the stream can be added.
        """
        pass

    def AddStream(
        self, parentGroup: StreamRefPtr, matchName: str
    ) -> StreamRefPtr:
        """Add a new stream to a group.

        Args:
            parentGroup: Parent stream group handle.
            matchName: Match name of the stream to add.

        Returns:
            Handle to the new stream.
        """
        pass

    def GetMatchname(self, stream: StreamRefPtr) -> str:
        """Get the match name of a stream.

        Args:
            stream: Stream handle.

        Returns:
            The match name string.
        """
        pass

    def GetNewParentStreamRef(self, stream: StreamRefPtr) -> StreamRefPtr:
        """Get the parent stream of a stream.

        Args:
            stream: Stream handle.

        Returns:
            Handle to the parent stream.
        """
        pass

    def GetStreamIsModified(self, stream: StreamRefPtr) -> bool:
        """Check if a stream has been modified from its default.

        Args:
            stream: Stream handle.

        Returns:
            True if modified.
        """
        pass

    def IsSeparationLeader(self, stream: StreamRefPtr) -> bool:
        """Check if a stream is a dimension separation leader.

        Args:
            stream: Stream handle.

        Returns:
            True if it is a separation leader.
        """
        pass

    def AreDimensionsSeparated(self, leaderStream: StreamRefPtr) -> bool:
        """Check if dimensions are separated on a leader stream.

        Args:
            leaderStream: Leader stream handle.

        Returns:
            True if dimensions are separated.
        """
        pass

    def SetDimensionsSeparated(
        self, leaderStream: StreamRefPtr, separated: bool
    ):
        """Set dimension separation on a leader stream.

        Args:
            leaderStream: Leader stream handle.
            separated: True to separate dimensions.
        """
        pass

    def GetSeparationFollower(
        self, dimension: int, leaderStream: StreamRefPtr
    ) -> StreamRefPtr:
        """Get a separation follower stream for a specific dimension.

        Args:
            dimension: Dimension index.
            leaderStream: Leader stream handle.

        Returns:
            Handle to the follower stream.
        """
        pass

    def IsSeparationFollower(self, stream: StreamRefPtr) -> bool:
        """Check if a stream is a dimension separation follower.

        Args:
            stream: Stream handle.

        Returns:
            True if it is a separation follower.
        """
        pass

    def GetSeparationLeader(self, followerStream: StreamRefPtr) -> StreamRefPtr:
        """Get the leader stream for a separation follower.

        Args:
            followerStream: Follower stream handle.

        Returns:
            Handle to the leader stream.
        """
        pass

    def GetSeparationDimension(self, stream: StreamRefPtr) -> int:
        """Get the dimension index of a separation follower.

        Args:
            stream: Follower stream handle.

        Returns:
            The dimension index.
        """
        pass

class KeyframeSuite:
    """Suite for keyframe operations.

    Provides methods to add, remove, query, and modify keyframes on
    property streams, including interpolation and temporal ease.

    Examples:
        >>> suite = PyFx.KeyframeSuite()
        >>> count = suite.GetStreamNumKFs(stream)
        >>> key_idx = suite.InsertKeyframe(
        ...     stream, PyFx.LTimeMode.CompTime, time
        ... )
    """

    def __init__(self):
        pass

    def GetStreamNumKFs(self, stream: StreamRefPtr) -> int:
        """Get the number of keyframes on a stream.

        Args:
            stream: Stream handle.

        Returns:
            The keyframe count.
        """
        pass

    def GetKeyframeTime(
        self, stream: StreamRefPtr, keyIndex: int, timeMode: LTimeMode
    ) -> Time:
        """Get the time of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            timeMode: Layer time or comp time.

        Returns:
            The keyframe time.
        """
        pass

    def InsertKeyframe(
        self, stream: StreamRefPtr, timeMode: LTimeMode, time: Time
    ) -> int:
        """Insert a new keyframe at a given time.

        Args:
            stream: Stream handle.
            timeMode: Layer time or comp time.
            time: Time for the new keyframe.

        Returns:
            The index of the new keyframe.
        """
        pass

    def DeleteKeyframe(self, stream: StreamRefPtr, keyIndex: int):
        """Delete a keyframe by index.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index to delete.
        """
        pass

    def GetNewKeyframeValue(
        self, stream: StreamRefPtr, keyIndex: int
    ) -> StreamValue2:
        """Get the value of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.

        Returns:
            The keyframe value.
        """
        pass

    def SetKeyframeValue(
        self, stream: StreamRefPtr, keyIndex: int, value: StreamValue2
    ):
        """Set the value of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            value: New keyframe value.
        """
        pass

    def GetStreamValueDimensionality(self, stream: StreamRefPtr) -> int:
        """Get the number of value dimensions of a stream.

        Args:
            stream: Stream handle.

        Returns:
            The dimensionality (1 for scalar, 2 for 2D, 3 for 3D).
        """
        pass

    def GetStreamTemporalDimensionality(self, stream: StreamRefPtr) -> int:
        """Get the temporal dimensionality of a stream.

        Args:
            stream: Stream handle.

        Returns:
            The temporal dimensionality.
        """
        pass

    def GetNewKeyframeSpatialTangents(
        self, stream: StreamRefPtr, keyIndex: int
    ) -> Tuple[StreamValue2, StreamValue2]:
        """Get the spatial tangents of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.

        Returns:
            A (in_tangent, out_tangent) tuple.
        """
        pass

    def SetKeyframeSpatialTangents(
        self,
        stream: StreamRefPtr,
        keyIndex: int,
        inTan: StreamValue2,
        outTan: StreamValue2,
    ):
        """Set the spatial tangents of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            inTan: Incoming spatial tangent.
            outTan: Outgoing spatial tangent.
        """
        pass

    def GetKeyframeTemporalEase(
        self, stream: StreamRefPtr, keyIndex: int, dimension: int
    ) -> Tuple[KeyframeEase, KeyframeEase]:
        """Get the temporal ease of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            dimension: Dimension index.

        Returns:
            A (in_ease, out_ease) tuple.
        """
        pass

    def SetKeyframeTemporalEase(
        self,
        stream: StreamRefPtr,
        keyIndex: int,
        dimension: int,
        inEase: KeyframeEase,
        outEase: KeyframeEase,
    ):
        """Set the temporal ease of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            dimension: Dimension index.
            inEase: Incoming ease.
            outEase: Outgoing ease.
        """
        pass

    def GetKeyframeFlags(
        self, stream: StreamRefPtr, keyIndex: int
    ) -> KeyframeFlag:
        """Get the flags of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.

        Returns:
            The keyframe flags.
        """
        pass

    def SetKeyframeFlag(
        self,
        stream: StreamRefPtr,
        keyIndex: int,
        flag: KeyframeFlag,
        value: bool,
    ):
        """Set a single flag on a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            flag: Which flag to set.
            value: Flag value.
        """
        pass

    def GetKeyframeInterpolation(
        self, stream: StreamRefPtr, keyIndex: int
    ) -> Tuple[KeyInterp, KeyInterp]:
        """Get the interpolation type of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.

        Returns:
            A (in_interp, out_interp) tuple.
        """
        pass

    def SetKeyframeInterpolation(
        self,
        stream: StreamRefPtr,
        keyIndex: int,
        inInterp: KeyInterp,
        outInterp: KeyInterp,
    ):
        """Set the interpolation type of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            inInterp: Incoming interpolation.
            outInterp: Outgoing interpolation.
        """
        pass

    def StartAddKeyframes(self, stream: StreamRefPtr) -> AddKeyframesInfoPtr:
        """Begin a batch keyframe addition operation.

        Args:
            stream: Stream handle.

        Returns:
            Handle to the batch operation.
        """
        pass

    def AddKeyframes(
        self, akH: AddKeyframesInfoPtr, timeMode: LTimeMode, time: Time
    ) -> int:
        """Add a keyframe in a batch operation.

        Args:
            akH: Batch operation handle.
            timeMode: Layer time or comp time.
            time: Keyframe time.

        Returns:
            The index of the new keyframe.
        """
        pass

    def SetAddKeyframe(
        self, akH: AddKeyframesInfoPtr, keyIndex: int, value: StreamValue2
    ):
        """Set the value of a keyframe in a batch operation.

        Args:
            akH: Batch operation handle.
            keyIndex: Keyframe index.
            value: Keyframe value.
        """
        pass

    def EndAddKeyframes(self, akH: AddKeyframesInfoPtr):
        """Finish a batch keyframe addition operation.

        Args:
            akH: Batch operation handle.
        """
        pass

    def GetKeyframeLabelColorIndex(
        self, stream: StreamRefPtr, keyIndex: int
    ) -> int:
        """Get the label color index of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.

        Returns:
            The label color index.
        """
        pass

    def SetKeyframeLabelColorIndex(
        self, stream: StreamRefPtr, keyIndex: int, keyLabel: int
    ):
        """Set the label color index of a keyframe.

        Args:
            stream: Stream handle.
            keyIndex: Keyframe index.
            keyLabel: New label color index.
        """
        pass

class TextDocumentSuite:
    """Suite for text document operations.

    Provides low-level methods to get and set text content on
    text document handles.

    Examples:
        >>> suite = PyFx.TextDocumentSuite()
        >>> text = suite.getNewText(text_doc_ptr)
        >>> suite.setText(text_doc_ptr, "New text")
    """

    def __init__(self):
        pass

    def getNewText(self, text_documentP: TextDocumentPtr) -> str:
        """Get the text content from a text document.

        Args:
            text_documentP: Text document handle.

        Returns:
            The text string.
        """
        pass

    def setText(self, text_documentP: TextDocumentPtr, unicodePS: str):
        """Set the text content of a text document.

        Args:
            text_documentP: Text document handle.
            unicodePS: New text string.
        """
        pass

class MarkerSuite:
    """Suite for marker operations.

    Provides low-level methods to create and manipulate markers,
    including strings, flags, cue points, duration, and labels.

    Examples:
        >>> suite = PyFx.MarkerSuite()
        >>> marker = suite.getNewMarker()
        >>> suite.setMarkerString(
        ...     marker, PyFx.MarkerStringType.COMMENT, "My marker"
        ... )
    """

    def __init__(self):
        pass

    def getNewMarker(self) -> MarkerValPtr:
        """Create a new empty marker.

        Returns:
            Handle to the new marker.
        """
        pass

    def duplicateMarker(self, markerP: MarkerValPtr) -> MarkerValPtr:
        """Duplicate a marker.

        Args:
            markerP: Marker handle.

        Returns:
            Handle to the duplicate marker.
        """
        pass

    def setMarkerFlag(
        self, markerP: MarkerValPtr, flagType: MarkerFlag, valueB: bool
    ):
        """Set a marker flag.

        Args:
            markerP: Marker handle.
            flagType: Which flag to set.
            valueB: Flag value.
        """
        pass

    def getMarkerFlag(
        self, markerP: MarkerValPtr, flagType: MarkerFlag
    ) -> bool:
        """Get a marker flag value.

        Args:
            markerP: Marker handle.
            flagType: Which flag to query.

        Returns:
            The flag value.
        """
        pass

    def getMarkerString(
        self, markerP: MarkerValPtr, strType: MarkerStringType
    ) -> str:
        """Get a marker string by type.

        Args:
            markerP: Marker handle.
            strType: Which string to retrieve.

        Returns:
            The string value.
        """
        pass

    def setMarkerString(
        self, markerP: MarkerValPtr, strType: MarkerStringType, unicodeP: str
    ):
        """Set a marker string by type.

        Args:
            markerP: Marker handle.
            strType: Which string to set.
            unicodeP: New string value.
        """
        pass

    def countCuePointParams(self, markerP: MarkerValPtr) -> int:
        """Count cue point parameters on a marker.

        Args:
            markerP: Marker handle.

        Returns:
            The parameter count.
        """
        pass

    def getIndCuePointParam(
        self, markerP: MarkerValPtr, param_indexL: int
    ) -> Tuple[str, str]:
        """Get a cue point parameter by index.

        Args:
            markerP: Marker handle.
            param_indexL: Parameter index.

        Returns:
            A (key, value) tuple.
        """
        pass

    def setIndCuePointParam(
        self,
        markerP: MarkerValPtr,
        param_indexL: int,
        unicodeKeyP: str,
        unicodeValueP: str,
    ):
        """Set a cue point parameter by index.

        Args:
            markerP: Marker handle.
            param_indexL: Parameter index.
            unicodeKeyP: Parameter key.
            unicodeValueP: Parameter value.
        """
        pass

    def insertCuePointParam(self, markerP: MarkerValPtr, param_indexL: int):
        """Insert a new cue point parameter.

        Args:
            markerP: Marker handle.
            param_indexL: Insertion index.
        """
        pass

    def deleteIndCuePointParam(self, markerP: MarkerValPtr, param_indexL: int):
        """Delete a cue point parameter by index.

        Args:
            markerP: Marker handle.
            param_indexL: Parameter index.
        """
        pass

    def setMarkerDuration(self, markerP: MarkerValPtr, durationPT: Time):
        """Set the marker duration.

        Args:
            markerP: Marker handle.
            durationPT: Duration time.
        """
        pass

    def getMarkerDuration(self, markerP: MarkerValPtr) -> Time:
        """Get the marker duration.

        Args:
            markerP: Marker handle.

        Returns:
            The duration time.
        """
        pass

    def setMarkerLabel(self, markerP: MarkerValPtr, value: int):
        """Set the marker label color index.

        Args:
            markerP: Marker handle.
            value: Label color index.
        """
        pass

    def getMarkerLabel(self, markerP: MarkerValPtr) -> int:
        """Get the marker label color index.

        Args:
            markerP: Marker handle.

        Returns:
            The label color index.
        """
        pass

class TextLayerSuite:
    """Suite for text layer outline operations.

    Provides methods to get text outlines (vector paths) from text layers.

    Examples:
        >>> suite = PyFx.TextLayerSuite()
        >>> outlines = suite.getNewTextOutlines(layer, time)
        >>> count = suite.getNumTextOutlines(outlines)
    """

    def __init__(self):
        pass

    def getNewTextOutlines(
        self, layer: LayerPtr, layer_time: Time
    ) -> TextOutlinesPtr:
        """Get the text outlines for a layer at a given time.

        Args:
            layer: Layer handle.
            layer_time: Time to evaluate.

        Returns:
            Handle to the text outlines.
        """
        pass

    def getNumTextOutlines(self, outlines: TextOutlinesPtr) -> int:
        """Get the number of outline paths.

        Args:
            outlines: Text outlines handle.

        Returns:
            The number of outlines.
        """
        pass
    # def getIndexedTextOutline(self, outlines: TextOutlinesPtr, path_index: int) -> PF_PathOutlinePtr:
    # pass

class EffectSuite:
    """Suite for effect operations.

    Provides methods to apply, remove, query, and manipulate effects
    on layers, including effect masks and installed effect lookup.

    Examples:
        >>> suite = PyFx.EffectSuite()
        >>> count = suite.getLayerNumEffects(layer)
        >>> effect = suite.getLayerEffectByIndex(layer, 0)
        >>> name = suite.getEffectName(
        ...     suite.getInstalledKeyFromLayerEffect(effect)
        ... )
    """

    def __init__(self):
        pass

    def getLayerNumEffects(self, layer: LayerPtr) -> int:
        """Get the number of effects on a layer.

        Args:
            layer: Layer handle.

        Returns:
            The effect count.
        """
        pass

    def getLayerEffectByIndex(
        self, layer: LayerPtr, layer_effect_index: int
    ) -> EffectRefPtr:
        """Get an effect by index on a layer.

        Args:
            layer: Layer handle.
            layer_effect_index: Zero-based effect index.

        Returns:
            Handle to the effect.
        """
        pass

    def getInstalledKeyFromLayerEffect(self, effect_ref: EffectRefPtr) -> int:
        """Get the installed effect key for a layer effect.

        Args:
            effect_ref: Effect handle.

        Returns:
            The installed effect key.
        """
        pass
    # def getEffectParamUnionByIndex(self, effect_ref: EffectRefPtr, param_index: int) -> Tuple[PF_ParamType, PF_ParamDefUnion]:
    #  pass

    def getEffectFlags(self, effect_ref: EffectRefPtr) -> EffectFlags:
        """Get the flags of an effect.

        Args:
            effect_ref: Effect handle.

        Returns:
            The effect flags.
        """
        pass

    def setEffectFlags(
        self,
        effect_ref: EffectRefPtr,
        effect_flags_set_mask: EffectFlags,
        effect_flags: EffectFlags,
    ):
        """Set flags on an effect.

        Args:
            effect_ref: Effect handle.
            effect_flags_set_mask: Bitmask of flags to modify.
            effect_flags: New flag values.
        """
        pass

    def reorderEffect(self, effect_ref: EffectRefPtr, effect_index: int):
        """Move an effect to a new index.

        Args:
            effect_ref: Effect handle.
            effect_index: New zero-based index.
        """
        pass
    # def effectCallGeneric(self, effect_ref: EffectRefPtr, timePT: Time, effect_cmd: PF_Cmd, effect_extraPV):
    #    pass

    def applyEffect(
        self, layer: LayerPtr, installed_effect_key: int
    ) -> EffectRefPtr:
        """Apply an installed effect to a layer.

        Args:
            layer: Layer handle.
            installed_effect_key: Effect key from `getNextInstalledEffect`.

        Returns:
            Handle to the new effect instance.
        """
        pass

    def deleteLayerEffect(self, effect_ref: EffectRefPtr):
        """Delete an effect from a layer.

        Args:
            effect_ref: Effect handle.
        """
        pass

    def getNumInstalledEffects(self) -> int:
        """Get the total number of installed effects.

        Returns:
            The installed effect count.
        """
        pass

    def getNextInstalledEffect(self, installed_effect_key: int) -> int:
        """Get the next installed effect key.

        Args:
            installed_effect_key: Current effect key (-1 to start).

        Returns:
            The next installed effect key.
        """
        pass

    def getEffectName(self, installed_effect_key: int) -> str:
        """Get the display name of an installed effect.

        Args:
            installed_effect_key: Effect key.

        Returns:
            The effect name.
        """
        pass

    def getEffectMatchName(self, installed_effect_key: int) -> str:
        """Get the match name of an installed effect.

        Args:
            installed_effect_key: Effect key.

        Returns:
            The match name string.
        """
        pass

    def getEffectCategory(self, installed_effect_key: int) -> str:
        """Get the category of an installed effect.

        Args:
            installed_effect_key: Effect key.

        Returns:
            The category string.
        """
        pass

    def duplicateEffect(
        self, original_effect_ref: EffectRefPtr
    ) -> EffectRefPtr:
        """Duplicate an effect.

        Args:
            original_effect_ref: Effect handle to duplicate.

        Returns:
            Handle to the duplicate effect.
        """
        pass

    def numEffectMask(self, effect_ref: EffectRefPtr) -> int:
        """Get the number of effect masks.

        Args:
            effect_ref: Effect handle.

        Returns:
            The mask count.
        """
        pass

    def getEffectMaskID(
        self, effect_ref: EffectRefPtr, mask_indexL: int
    ) -> int:
        """Get the mask ID for an effect mask by index.

        Args:
            effect_ref: Effect handle.
            mask_indexL: Mask index.

        Returns:
            The mask ID.
        """
        pass

    def addEffectMask(
        self, effect_ref: EffectRefPtr, id_val: int
    ) -> StreamRefPtr:
        """Add a mask to an effect.

        Args:
            effect_ref: Effect handle.
            id_val: Mask ID to add.

        Returns:
            Handle to the mask stream.
        """
        pass

    def removeEffectMask(self, effect_ref: EffectRefPtr, id_val: int):
        """Remove a mask from an effect.

        Args:
            effect_ref: Effect handle.
            id_val: Mask ID to remove.
        """
        pass

    def setEffectMask(
        self, effect_ref: EffectRefPtr, mask_indexL: int, id_val: int
    ) -> StreamRefPtr:
        """Set a mask on an effect by index.

        Args:
            effect_ref: Effect handle.
            mask_indexL: Mask index.
            id_val: New mask ID.

        Returns:
            Handle to the mask stream.
        """
        pass

class MaskSuite:
    """Suite for mask operations on layers.

    Provides methods to create, delete, query, and modify masks,
    including mode, invert, motion blur, feather, and color.

    Examples:
        >>> suite = PyFx.MaskSuite()
        >>> count = suite.getLayerNumMasks(layer)
        >>> mask = suite.getLayerMaskByIndex(layer, 0)
        >>> mode = suite.getMaskMode(mask)
    """

    def __init__(self):
        pass

    def getLayerNumMasks(self, layer: LayerPtr) -> int:
        """Get the number of masks on a layer.

        Args:
            layer: Layer handle.

        Returns:
            The mask count.
        """
        pass

    def getLayerMaskByIndex(
        self, layer: LayerPtr, mask_indexL: int
    ) -> MaskRefPtr:
        """Get a mask by index.

        Args:
            layer: Layer handle.
            mask_indexL: Zero-based mask index.

        Returns:
            Handle to the mask.
        """
        pass

    def getMaskInvert(self, mask_ref: MaskRefPtr) -> bool:
        """Check if a mask is inverted.

        Args:
            mask_ref: Mask handle.

        Returns:
            True if the mask is inverted.
        """
        pass

    def setMaskInvert(self, mask_ref: MaskRefPtr, invertB: bool):
        """Set the invert state of a mask.

        Args:
            mask_ref: Mask handle.
            invertB: True to invert.
        """
        pass

    def getMaskMode(self, mask_ref: MaskRefPtr) -> MaskMode:
        """Get the blending mode of a mask.

        Args:
            mask_ref: Mask handle.

        Returns:
            The mask mode.
        """
        pass

    def setMaskMode(self, maskH: MaskRefPtr, mode: MaskMode):
        """Set the blending mode of a mask.

        Args:
            maskH: Mask handle.
            mode: New mask mode.
        """
        pass

    def getMaskMotionBlurState(self, mask_ref: MaskRefPtr) -> MaskMBlur:
        """Get the motion blur state of a mask.

        Args:
            mask_ref: Mask handle.

        Returns:
            The motion blur state.
        """
        pass

    def setMaskMotionBlurState(
        self, mask_ref: MaskRefPtr, blur_state: MaskMBlur
    ):
        """Set the motion blur state of a mask.

        Args:
            mask_ref: Mask handle.
            blur_state: New motion blur state.
        """
        pass

    def getMaskFeatherFalloff(self, mask_ref: MaskRefPtr) -> MaskFeatherFalloff:
        """Get the feather falloff type of a mask.

        Args:
            mask_ref: Mask handle.

        Returns:
            The feather falloff type.
        """
        pass

    def setMaskFeatherFalloff(
        self, mask_ref: MaskRefPtr, feather_falloffP: MaskFeatherFalloff
    ):
        """Set the feather falloff type of a mask.

        Args:
            mask_ref: Mask handle.
            feather_falloffP: New feather falloff type.
        """
        pass

    def getMaskID(self, mask_ref: MaskRefPtr) -> int:
        """Get the unique ID of a mask.

        Args:
            mask_ref: Mask handle.

        Returns:
            The mask ID.
        """
        pass

    def createNewMask(self, layerH: LayerPtr, mask_indexPL0: int) -> MaskRefPtr:
        """Create a new mask on a layer.

        Args:
            layerH: Layer handle.
            mask_indexPL0: Index for the new mask.

        Returns:
            Handle to the new mask.
        """
        pass

    def deleteMaskFromLayer(self, mask_ref: MaskRefPtr):
        """Delete a mask from a layer.

        Args:
            mask_ref: Mask handle.
        """
        pass

    def getMaskColor(self, mask_ref: MaskRefPtr) -> ColorVal:
        """Get the display color of a mask.

        Args:
            mask_ref: Mask handle.

        Returns:
            The mask color.
        """
        pass

    def setMaskColor(self, mask_ref: MaskRefPtr, colorP: ColorVal):
        """Set the display color of a mask.

        Args:
            mask_ref: Mask handle.
            colorP: New mask color.
        """
        pass

    def getMaskLockState(self, mask_ref: MaskRefPtr) -> bool:
        """Check if a mask is locked.

        Args:
            mask_ref: Mask handle.

        Returns:
            True if locked.
        """
        pass

    def setMaskLockState(self, mask_ref: MaskRefPtr, lockB: bool):
        """Set the lock state of a mask.

        Args:
            mask_ref: Mask handle.
            lockB: True to lock.
        """
        pass

    def getMaskIsRotoBezier(self, mask_ref: MaskRefPtr) -> bool:
        """Check if a mask uses RotoBezier mode.

        Args:
            mask_ref: Mask handle.

        Returns:
            True if RotoBezier.
        """
        pass

    def setMaskIsRotoBezier(self, mask_ref: MaskRefPtr, is_roto_bezierB: bool):
        """Set the RotoBezier mode of a mask.

        Args:
            mask_ref: Mask handle.
            is_roto_bezierB: True for RotoBezier.
        """
        pass

    def duplicateMask(self, orig_mask_refH: MaskRefPtr) -> MaskRefPtr:
        """Duplicate a mask.

        Args:
            orig_mask_refH: Mask handle to duplicate.

        Returns:
            Handle to the duplicate mask.
        """
        pass

class MaskOutlineSuite:
    """Suite for mask outline (path) operations.

    Provides low-level methods to manipulate mask path vertices and
    feathers via `MaskOutlineValPtr` handles.

    Examples:
        >>> suite = PyFx.MaskOutlineSuite()
        >>> is_open = suite.isMaskOutlineOpen(outline)
        >>> num_pts = suite.getMaskOutlineNumSegments(outline)
    """

    def __init__(self):
        pass

    def isMaskOutlineOpen(self, mask_outlineH: MaskOutlineValPtr) -> bool:
        """Check if a mask outline is open.

        Args:
            mask_outlineH: Mask outline handle.

        Returns:
            True if the outline is open.
        """
        pass

    def setMaskOutlineOpen(self, mask_outlineH: MaskOutlineValPtr, openB: bool):
        """Set the open/closed state of a mask outline.

        Args:
            mask_outlineH: Mask outline handle.
            openB: True for open.
        """
        pass

    def getMaskOutlineNumSegments(
        self, mask_outlineH: MaskOutlineValPtr
    ) -> int:
        """Get the number of segments in a mask outline.

        Args:
            mask_outlineH: Mask outline handle.

        Returns:
            The segment count.
        """
        pass

    def getMaskOutlineVertexInfo(
        self, mask_outlineH: MaskOutlineValPtr, which_pointL: int
    ) -> MaskVertex:
        """Get vertex info at a specific index.

        Args:
            mask_outlineH: Mask outline handle.
            which_pointL: Vertex index.

        Returns:
            The vertex data.
        """
        pass

    def setMaskOutlineVertexInfo(
        self,
        mask_outlineH: MaskOutlineValPtr,
        which_pointL: int,
        vertexP: MaskVertex,
    ):
        """Set vertex info at a specific index.

        Args:
            mask_outlineH: Mask outline handle.
            which_pointL: Vertex index.
            vertexP: New vertex data.
        """
        pass

    def createVertex(
        self, mask_outlineH: MaskOutlineValPtr, insert_position: int
    ):
        """Insert a new vertex at a position.

        Args:
            mask_outlineH: Mask outline handle.
            insert_position: Index for the new vertex.
        """
        pass

    def deleteVertex(self, mask_outlineH: MaskOutlineValPtr, index: int):
        """Delete a vertex by index.

        Args:
            mask_outlineH: Mask outline handle.
            index: Vertex index.
        """
        pass

    def getMaskOutlineNumFeathers(
        self, mask_outlineH: MaskOutlineValPtr
    ) -> int:
        """Get the number of feather points.

        Args:
            mask_outlineH: Mask outline handle.

        Returns:
            The feather count.
        """
        pass

    def getMaskOutlineFeatherInfo(
        self, mask_outlineH: MaskOutlineValPtr, which_featherL: int
    ) -> MaskFeather:
        """Get feather info at a specific index.

        Args:
            mask_outlineH: Mask outline handle.
            which_featherL: Feather index.

        Returns:
            The feather settings.
        """
        pass

    def setMaskOutlineFeatherInfo(
        self,
        mask_outlineH: MaskOutlineValPtr,
        which_featherL: int,
        featherP: MaskFeather,
    ):
        """Set feather info at a specific index.

        Args:
            mask_outlineH: Mask outline handle.
            which_featherL: Feather index.
            featherP: New feather settings.
        """
        pass

    def createMaskOutlineFeather(
        self, mask_outlineH: MaskOutlineValPtr, featherP0: MaskFeather
    ) -> int:
        """Create a new feather point.

        Args:
            mask_outlineH: Mask outline handle.
            featherP0: Initial feather settings.

        Returns:
            The index of the new feather.
        """
        pass

    def deleteMaskOutlineFeather(
        self, mask_outlineH: MaskOutlineValPtr, index: int
    ):
        """Delete a feather point by index.

        Args:
            mask_outlineH: Mask outline handle.
            index: Feather index.
        """
        pass

class FootageSuite:
    """Suite for footage operations.

    Provides methods to import, create, query, and replace footage
    sources, including file-based, solid, and placeholder footage.

    Examples:
        >>> suite = PyFx.FootageSuite()
        >>> footage = suite.getMainFootageFromItem(item)
        >>> path = suite.getFootagePath(footage, 0, 0)
    """

    def __init__(self):
        pass

    def getMainFootageFromItem(self, itemH: ItemPtr) -> FootagePtr:
        """Get the main footage from an item.

        Args:
            itemH: Item handle.

        Returns:
            Handle to the main footage.
        """
        pass

    def getProxyFootageFromItem(self, itemH: ItemPtr) -> FootagePtr:
        """Get the proxy footage from an item.

        Args:
            itemH: Item handle.

        Returns:
            Handle to the proxy footage.
        """
        pass

    def getFootageNumFiles(self, footageH: FootagePtr) -> Tuple[int, int]:
        """Get the number of files in a footage source.

        Args:
            footageH: Footage handle.

        Returns:
            A (num_main_files, num_per_frame_files) tuple.
        """
        pass

    def getFootagePath(
        self, footageH: FootagePtr, frame_numL: int, file_indexL: int
    ) -> str:
        """Get the file path of a footage source.

        Args:
            footageH: Footage handle.
            frame_numL: Frame number.
            file_indexL: File index.

        Returns:
            The file path string.
        """
        pass

    def getFootageSignature(self, footageH: FootagePtr) -> FootageSignature:
        """Get the signature type of footage.

        Args:
            footageH: Footage handle.

        Returns:
            The footage signature.
        """
        pass

    def newFootage(
        self,
        pathZ: str,
        layer_infoP0: FootageLayerKey,
        sequence_optionsP0: FileSequenceImportOptions,
        interp_style: InterpretationStyle,
    ) -> FootagePtr:
        """Create new footage from a file path.

        Args:
            pathZ: File path.
            layer_infoP0: Layer key for multi-layer files.
            sequence_optionsP0: Sequence import options.
            interp_style: Interpretation dialog behavior.

        Returns:
            Handle to the new footage.
        """
        pass

    def addFootageToProject(
        self, footageH: FootagePtr, folderH: ItemPtr
    ) -> ItemPtr:
        """Add footage to the project.

        Args:
            footageH: Footage handle.
            folderH: Destination folder handle.

        Returns:
            Handle to the new project item.
        """
        pass

    def setItemProxyFootage(self, footageH: FootagePtr, itemH: ItemPtr):
        """Set footage as a proxy for an item.

        Args:
            footageH: Footage handle.
            itemH: Item handle.
        """
        pass

    def replaceItemMainFootage(self, footageH: FootagePtr, itemH: ItemPtr):
        """Replace an item's main footage.

        Args:
            footageH: New footage handle.
            itemH: Item handle.
        """
        pass
    # def getFootageInterpretation(self, itemH: ItemPtr, proxyB: bool) -> FootageInterp:
    #    pass

    # def setFootageInterpretation(self, itemH: ItemPtr, proxyB: bool, interpP: AEGP_FootageInterp):
    #    pass

    def getFootageLayerKey(self, footageH: FootagePtr) -> FootageLayerKey:
        """Get the layer key of footage.

        Args:
            footageH: Footage handle.

        Returns:
            The footage layer key.
        """
        pass

    def newPlaceholderFootage(
        self, nameZ: str, width: int, height: int, durationPT: Time
    ) -> FootagePtr:
        """Create placeholder footage.

        Args:
            nameZ: Placeholder name.
            width: Width in pixels.
            height: Height in pixels.
            durationPT: Duration.

        Returns:
            Handle to the placeholder footage.
        """
        pass
    # def newPlaceholderFootageWithPath(self, pathZ: str, path_platform: Platform, file_type: AEIO_FileType, widthL: int, heightL: int, durationPT: Time) -> FootagePtr:
    #    pass

    def newSolidFootage(
        self, nameZ: str, width: int, height: int, colorP: ColorVal
    ) -> FootagePtr:
        """Create a new solid footage item.

        Args:
            nameZ: Display name for the solid.
            width: Width in pixels.
            height: Height in pixels.
            colorP: Solid color as `ColorVal`.

        Returns:
            `FootagePtr` for the new solid.
        """
        pass

    def getSolidFootageColor(self, itemH: ItemPtr, proxyB: bool) -> ColorVal:
        """Get the color of a solid footage item.

        Args:
            itemH: `ItemPtr` for the solid item.
            proxyB: True to query the proxy, False for the main footage.

        Returns:
            `ColorVal` representing the solid color.
        """
        pass

    def setSolidFootageColor(
        self, itemH: ItemPtr, proxyB: bool, colorP: ColorVal
    ) -> None:
        """Set the color of a solid footage item.

        Args:
            itemH: `ItemPtr` for the solid item.
            proxyB: True to set on the proxy, False for the main footage.
            colorP: New color as `ColorVal`.
        """
        pass

    def setSolidFootageDimensions(
        self, itemH: ItemPtr, proxyB: bool, widthL: int, heightL: int
    ) -> None:
        """Set the dimensions of a solid footage item.

        Args:
            itemH: `ItemPtr` for the solid item.
            proxyB: True to set on the proxy, False for the main footage.
            widthL: New width in pixels.
            heightL: New height in pixels.
        """
        pass

    def getFootageSoundDataFormat(
        self, footageH: FootagePtr
    ) -> SoundDataFormat:
        """Get the sound data format for footage.

        Args:
            footageH: `FootagePtr` to query.

        Returns:
            `SoundDataFormat` describing the audio format.
        """
        pass

    def getFootageSequenceImportOptions(
        self, footageH: FootagePtr
    ) -> FileSequenceImportOptions:
        """Get the file-sequence import options for footage.

        Args:
            footageH: `FootagePtr` to query.

        Returns:
            `FileSequenceImportOptions` for the footage.
        """
        pass

class UtilitySuite:
    """General-purpose helper functions for AE plugin development.

    Provides UI utilities, undo grouping, error suppression, color-palette
    access, numeric conversions, and debug logging.

    Examples:
        >>> util = PyFx.UtilitySuite()
        >>> util.startUndoGroup("My Edit")
        >>> # ... make changes ...
        >>> util.endUndoGroup()
    """

    def __init__(self):
        pass

    def reportInfo(self, info_string: str):
        """Display an information dialog to the user.

        Args:
            info_string: Message text to display.
        """
        pass

    def reportInfoUnicode(self, info_string: str):
        """Display a Unicode information dialog to the user.

        Args:
            info_string: Unicode message text to display.
        """
        pass

    def getDriverPluginInitFuncVersion(self) -> Tuple[int, int]:
        """Get the driver plug-in initialisation function version.

        Returns:
            Tuple of (major, minor) version numbers.
        """
        pass

    def getDriverImplementationVersion(self) -> Tuple[int, int]:
        """Get the driver implementation version.

        Returns:
            Tuple of (major, minor) version numbers.
        """
        pass

    def startQuietErrors(self):
        """Begin suppressing error dialogs.

        Pair with `endQuietErrors` to restore normal error reporting.
        """
        pass

    def endQuietErrors(self, report_quieted_errorsB: bool):
        """End error suppression started by `startQuietErrors`.

        Args:
            report_quieted_errorsB: True to report any errors that were suppressed.
        """
        pass

    def getLastErrorMessage(self, buffer_size: int) -> str:
        """Retrieve the most recent error message.

        Args:
            buffer_size: Maximum number of characters to return.

        Returns:
            The last error message string.
        """
        pass

    def startUndoGroup(self, undo_name: str):
        """Begin an undoable group of operations.

        Args:
            undo_name: Name shown in the Edit > Undo menu.
        """
        pass

    def endUndoGroup(self):
        """End the current undo group opened by `startUndoGroup`."""
        pass

    def getMainHWND(self):
        """Get the main application window handle (Windows only)."""
        pass

    def showHideAllFloaters(self, include_tool_palB: bool):
        """Show or hide all floating palettes.

        Args:
            include_tool_palB: True to also toggle the tool palette.
        """
        pass

    def getPaintPalForeColor(self) -> ColorVal:
        """Get the current paint-palette foreground color.

        Returns:
            `ColorVal` of the foreground color.
        """
        pass

    def getPaintPalBackColor(self) -> ColorVal:
        """Get the current paint-palette background color.

        Returns:
            `ColorVal` of the background color.
        """
        pass

    def setPaintPalForeColor(self, fore_color: ColorVal):
        """Set the paint-palette foreground color.

        Args:
            fore_color: New foreground `ColorVal`.
        """
        pass

    def setPaintPalBackColor(self, back_color: ColorVal):
        """Set the paint-palette background color.

        Args:
            back_color: New background `ColorVal`.
        """
        pass

    def getCharPalFillColor(self) -> Tuple[bool, ColorVal]:
        """Get the character-palette fill color.

        Returns:
            Tuple of (is_defined, `ColorVal`). `is_defined` is True when
            a fill color is active.
        """
        pass

    def getCharPalStrokeColor(self) -> Tuple[bool, ColorVal]:
        """Get the character-palette stroke color.

        Returns:
            Tuple of (is_defined, `ColorVal`). `is_defined` is True when
            a stroke color is active.
        """
        pass

    def setCharPalFillColor(self, fill_color: ColorVal):
        """Set the character-palette fill color.

        Args:
            fill_color: New fill `ColorVal`.
        """
        pass

    def setCharPalStrokeColor(self, stroke_color: ColorVal):
        """Set the character-palette stroke color.

        Args:
            stroke_color: New stroke `ColorVal`.
        """
        pass

    def charPalIsFillColorUIFrontmost(self) -> bool:
        """Check whether fill (not stroke) is frontmost in the character palette.

        Returns:
            True if the fill color chip is in front.
        """
        pass

    def convertFpLongToHSFRatio(self, numberF: float) -> Ratio:
        """Convert a floating-point value to an `Ratio`.

        Args:
            numberF: Floating-point number to convert.

        Returns:
            Equivalent `Ratio`.
        """
        pass

    def convertHSFRatioToFpLong(self, ratioR: Ratio) -> float:
        """Convert an `Ratio` to a floating-point value.

        Args:
            ratioR: `Ratio` to convert.

        Returns:
            Equivalent float.
        """
        pass

    def causeIdleRoutinesToBeCalled(self):
        """Request that AE call idle-time routines as soon as possible."""
        pass

    def getSuppressInteractiveUI(self) -> bool:
        """Check whether interactive UI is currently suppressed.

        Returns:
            True if interactive UI is suppressed (e.g., during rendering).
        """
        pass

    def writeToOSConsole(self, text: str):
        """Write a message to the operating-system console.

        Args:
            text: Text to write.
        """
        pass

    def writeToDebugLog(self, subsystem: str, eventType: str, text: str):
        """Write an entry to the AE debug log.

        Args:
            subsystem: Log subsystem identifier.
            eventType: Event-type identifier.
            text: Log message text.
        """
        pass

    def getPluginPath(self, path_type: PluginPathType) -> str:
        """Get a file-system path related to the plugin.

        Args:
            path_type: `PluginPathType` specifying which path to retrieve.

        Returns:
            Absolute path string.
        """
        pass

class RenderQueueSuite:
    """Manage the After Effects render queue.

    Add compositions to the queue and control the overall queue state
    (stopped, paused, rendering).

    Examples:
        >>> rq = PyFx.RenderQueueSuite()
        >>> rq.addCompToRenderQueue(comp, r"C:\\output\\render.mov")
        >>> rq.setRenderQueueState(PyFx.RenderQueueState.RENDERING)
    """

    def __init__(self):
        pass

    def addCompToRenderQueue(self, comp: CompPtr, path: str):
        """Add a composition to the render queue with an output path.

        Args:
            comp: `CompPtr` of the composition to enqueue.
            path: File-system path for the rendered output.
        """
        pass

    def setRenderQueueState(self, state: RenderQueueState):
        """Set the render queue state.

        Args:
            state: Desired `RenderQueueState` (e.g., stopped, paused, rendering).
        """
        pass

    def getRenderQueueState(self) -> RenderQueueState:
        """Get the current render queue state.

        Returns:
            Current `RenderQueueState`.
        """
        pass

class RenderQueueItemSuite:
    """Inspect and control individual render-queue items (RQItems).

    Each RQItem represents one composition queued for rendering. Use this
    suite to read/write status, timing, logging, comments, and output modules.

    Examples:
        >>> rqi = PyFx.RenderQueueItemSuite()
        >>> count = rqi.getNumRQItems()
        >>> item = rqi.getRQItemByIndex(0)
        >>> rqi.setRenderState(item, PyFx.RenderItemStatus.QUEUED)
    """

    def __init__(self):
        pass

    def getNumRQItems(self) -> int:
        """Get the total number of items in the render queue.

        Returns:
            Number of render-queue items.
        """
        pass

    def getRQItemByIndex(self, rq_item_index: int) -> RQItemRefPtr:
        """Get a render-queue item by its index.

        Args:
            rq_item_index: Zero-based index into the render queue.

        Returns:
            `RQItemRefPtr` for the item.
        """
        pass

    def getNextRQItem(self, current_rq_item: RQItemRefPtr) -> RQItemRefPtr:
        """Get the next render-queue item after the given one.

        Args:
            current_rq_item: `RQItemRefPtr` of the current item.

        Returns:
            `RQItemRefPtr` for the next item.
        """
        pass

    def getNumOutputModulesForRQItem(self, rq_item: RQItemRefPtr) -> int:
        """Get the number of output modules attached to a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` to query.

        Returns:
            Number of output modules.
        """
        pass

    def getRenderState(self, rq_item: RQItemRefPtr) -> RenderItemStatus:
        """Get the render status of a queue item.

        Args:
            rq_item: `RQItemRefPtr` to query.

        Returns:
            Current `RenderItemStatus`.
        """
        pass

    def setRenderState(self, rq_item: RQItemRefPtr, status: RenderItemStatus):
        """Set the render status of a queue item.

        Args:
            rq_item: `RQItemRefPtr` to modify.
            status: Desired `RenderItemStatus`.
        """
        pass

    def getStartedTime(self, rq_item: RQItemRefPtr) -> Time:
        """Get the time at which rendering started for an item.

        Args:
            rq_item: `RQItemRefPtr` to query.

        Returns:
            `Time` when rendering began.
        """
        pass

    def getElapsedTime(self, rq_item: RQItemRefPtr) -> Time:
        """Get the elapsed render time for an item.

        Args:
            rq_item: `RQItemRefPtr` to query.

        Returns:
            `Time` representing elapsed rendering duration.
        """
        pass

    def getLogType(self, rq_item: RQItemRefPtr) -> LogType:
        """Get the log-output type for a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` to query.

        Returns:
            Current `LogType`.
        """
        pass

    def setLogType(self, rq_item: RQItemRefPtr, logtype: LogType):
        """Set the log-output type for a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` to modify.
            logtype: Desired `LogType`.
        """
        pass

    def removeOutputModule(
        self, rq_item: RQItemRefPtr, outmod: OutputModuleRefPtr
    ):
        """Remove an output module from a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` owning the output module.
            outmod: `OutputModuleRefPtr` to remove.
        """
        pass

    def getComment(self, rq_item: RQItemRefPtr) -> str:
        """Get the user comment for a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` to query.

        Returns:
            Comment string.
        """
        pass

    def setComment(self, rq_item: RQItemRefPtr, comment: str):
        """Set the user comment for a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` to modify.
            comment: New comment string.
        """
        pass

    def getCompFromRQItem(self, rq_item: RQItemRefPtr) -> CompPtr:
        """Get the composition associated with a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` to query.

        Returns:
            `CompPtr` for the associated composition.
        """
        pass

    def deleteRQItem(self, rq_item: RQItemRefPtr):
        """Delete a render-queue item.

        Args:
            rq_item: `RQItemRefPtr` to delete.
        """
        pass

class OutputModuleSuite:
    """Configure output modules attached to render-queue items.

    Controls file format, embedding, post-render actions, output channels,
    stretch/crop settings, sound format, and file paths.

    Examples:
        >>> om = PyFx.OutputModuleSuite()
        >>> outmod = om.getOutputModuleByIndex(rq_item, 0)
        >>> om.setOutputFilePath(rq_item, outmod, r"C:\\output\\render.mov")
    """

    def __init__(self):
        pass

    def getOutputModuleByIndex(
        self, rq_itemH: RQItemRefPtr, outmod_indexL: int
    ) -> OutputModuleRefPtr:
        """Get an output module by index from a render-queue item.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output modules.
            outmod_indexL: Zero-based index.

        Returns:
            `OutputModuleRefPtr` for the output module.
        """
        pass

    def getEmbedOptions(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> EmbeddingType:
        """Get the embedding options for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Current `EmbeddingType`.
        """
        pass

    def setEmbedOptions(
        self,
        rq_itemH: RQItemRefPtr,
        outmodH: OutputModuleRefPtr,
        embed_options: EmbeddingType,
    ):
        """Set the embedding options for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            embed_options: Desired `EmbeddingType`.
        """
        pass

    def getPostRenderAction(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> PostRenderAction:
        """Get the post-render action for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Current `PostRenderAction`.
        """
        pass

    def setPostRenderAction(
        self,
        rq_itemH: RQItemRefPtr,
        outmodH: OutputModuleRefPtr,
        post_render_action: PostRenderAction,
    ):
        """Set the post-render action for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            post_render_action: Desired `PostRenderAction`.
        """
        pass

    def getEnabledOutputs(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> OutputTypes:
        """Get which output types are enabled (video, audio, etc.).

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            `OutputTypes` flags indicating enabled outputs.
        """
        pass

    def setEnabledOutputs(
        self,
        rq_itemH: RQItemRefPtr,
        outmodH: OutputModuleRefPtr,
        enabled_types: OutputTypes,
    ):
        """Set which output types are enabled (video, audio, etc.).

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            enabled_types: `OutputTypes` flags to enable.
        """
        pass

    def getOutputChannels(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> VideoChannels:
        """Get the video channel configuration for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Current `VideoChannels` setting.
        """
        pass

    def setOutputChannels(
        self,
        rq_itemH: RQItemRefPtr,
        outmodH: OutputModuleRefPtr,
        output_channels: VideoChannels,
    ):
        """Set the video channel configuration for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            output_channels: Desired `VideoChannels` setting.
        """
        pass

    def getStretchInfo(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> Tuple[bool, StretchQuality, bool]:
        """Get the stretch settings for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Tuple of (is_enabled, `StretchQuality`, lock_aspect_ratio).
        """
        pass

    def setStretchInfo(
        self,
        rq_itemH: RQItemRefPtr,
        outmodH: OutputModuleRefPtr,
        is_enabledB: bool,
        stretch_quality: StretchQuality,
    ):
        """Set the stretch settings for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            is_enabledB: True to enable stretching.
            stretch_quality: Desired `StretchQuality`.
        """
        pass

    def getCropInfo(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> Tuple[bool, LRect]:
        """Get the crop settings for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Tuple of (is_enabled, `LRect` crop rectangle).
        """
        pass

    def setCropInfo(
        self,
        rq_itemH: RQItemRefPtr,
        outmodH: OutputModuleRefPtr,
        enableB: bool,
        crop_rect: LRect,
    ):
        """Set the crop settings for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            enableB: True to enable cropping.
            crop_rect: `LRect` defining the crop region.
        """
        pass

    def getSoundFormatInfo(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> Tuple[SoundDataFormat, bool]:
        """Get the sound format settings for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Tuple of (`SoundDataFormat`, audio_enabled).
        """
        pass

    def setSoundFormatInfo(
        self,
        rq_itemH: RQItemRefPtr,
        outmodH: OutputModuleRefPtr,
        sound_format_info: SoundDataFormat,
        audio_enabledB: bool,
    ):
        """Set the sound format settings for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            sound_format_info: Desired `SoundDataFormat`.
            audio_enabledB: True to enable audio output.
        """
        pass

    def getOutputFilePath(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> str:
        """Get the output file path for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Absolute file path string.
        """
        pass

    def setOutputFilePath(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr, path: str
    ):
        """Set the output file path for an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to modify.
            path: Absolute file path for the output.
        """
        pass

    def addDefaultOutputModule(
        self, rq_itemH: RQItemRefPtr
    ) -> OutputModuleRefPtr:
        """Add a default output module to a render-queue item.

        Args:
            rq_itemH: `RQItemRefPtr` to add the output module to.

        Returns:
            `OutputModuleRefPtr` for the newly added module.
        """
        pass

    def getExtraOutputModuleInfo(
        self, rq_itemH: RQItemRefPtr, outmodH: OutputModuleRefPtr
    ) -> Tuple[str, str, bool, bool]:
        """Get extra information about an output module.

        Args:
            rq_itemH: `RQItemRefPtr` owning the output module.
            outmodH: `OutputModuleRefPtr` to query.

        Returns:
            Tuple of (format_name, format_extension, is_sequence, is_multi_frame).
        """
        pass
