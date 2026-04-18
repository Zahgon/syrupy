import collections
import inspect
from abc import ABC, abstractmethod
from collections import OrderedDict
from collections.abc import Callable, Generator, Iterable
from types import (
    FunctionType,
    GeneratorType,
    MappingProxyType,
)
from typing import (
    TYPE_CHECKING,
    Any,
    NamedTuple,
    Optional,
)

from syrupy.constants import (
    SYMBOL_ELLIPSIS,
    TEXT_ENCODING,
)
from syrupy.data import (
    Snapshot,
    SnapshotCollection,
)

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        PropertyName,
        PropertyPath,
        SerializableData,
    )

    PropertyValueFilter = Callable[["PropertyName"], bool]
    PropertyValueGetter = Callable[
        ["SerializableData", "PropertyName"], "SerializableData"
    ]
    IterableEntries = tuple[
        Iterable["PropertyName"],
        "PropertyValueGetter",
        "PropertyValueFilter | None",
    ]


class Repr:
    def __init__(self, _repr: str):
        self._repr = _repr

    def __repr__(self) -> str:
        return self._repr


def attr_getter(o: "SerializableData", p: "PropertyName") -> "SerializableData":
    return getattr(o, str(p))


def item_getter(o: "SerializableData", p: "PropertyName") -> "SerializableData":
    pass


class MalformedAmberFile(Exception):
    """
    The Amber file is malformed. It should be deleted and regenerated.
    """


class MissingVersionError(Exception):
    """
    Missing Amber version marker.
    """


def removesuffix(string: str, suffix: str) -> str:
    """
    Can be replaced with str.removesuffix once Py3.8 support is dropped.
    """
    pass


class AmberDataSerializerPlugin(ABC):
    """
    A Syrupy plugin for extending Amber serialization.
    """

    @classmethod
    @abstractmethod
    def is_data_serializable(cls, data: "SerializableData") -> bool:
        """
        Determine if this plugin can serialize the given data.
        """
        pass

    @classmethod
    @abstractmethod
    def serialize(cls, data: "SerializableData", **kwargs: Any) -> str:
        """
        Return the serialization method for the given data.
        """
        pass


class AmberDataSerializer:
    """
    If extending the serializer, change the VERSION property to some unique value
    for your iteration of the serializer so as to force invalidation of existing
    snapshots.
    """

    VERSION = "1"

    serializer_plugins: Iterable[type["AmberDataSerializerPlugin"]] | None = None

    _indent: str = "  "
    _max_depth: int = 99
    _marker_prefix = "# "

    class Marker:
        Version = "serializer version"
        Name = "name"
        Divider = "---"

    @classmethod
    def snapshot_sort_key(cls, snapshot: "Snapshot") -> Any:
        pass

    @classmethod
    def write_file(
        cls, snapshot_collection: "SnapshotCollection", merge: bool = False
    ) -> None:
        """
        Writes the snapshot data into the snapshot file that can be read later.
        """
        pass

    @classmethod
    def __read_file_with_markers(
        cls, filepath: str
    ) -> Generator["Snapshot", None, None]:
        pass

    @classmethod
    def read_file(cls, filepath: str) -> "SnapshotCollection":
        """
        Read the raw snapshot data (str) from the snapshot file into a dict
        of snapshot name to raw data. This does not attempt any deserialization
        of the snapshot data.
        """
        pass

    @classmethod
    def serialize(
        cls,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> str:
        """
        After serializing, new line control characters are normalised. This is needed
        for interoperablity of snapshot matching between systems that do not use the
        same new line control characters. Example snapshots generated on windows os
        should not break when running the tests on a unix based system and vice versa.
        """
        pass

    @classmethod
    def _serialize(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
        path: "PropertyPath" = (),
        visited: set[Any] | None = None,
    ) -> str:
        pass

    @classmethod
    def _assign_serialize_method(cls, data: "SerializableData") -> Callable[..., str]:
        pass

    @classmethod
    def serialize_number(
        cls, data: int | float, *, depth: int = 0, **kwargs: Any
    ) -> str:
        pass

    @classmethod
    def serialize_string(cls, data: str, *, depth: int = 0, **kwargs: Any) -> str:
        pass

    @classmethod
    def serialize_iterable(
        cls, data: Iterable["SerializableData"], **kwargs: Any
    ) -> str:
        pass

    @classmethod
    def serialize_set(cls, data: set["SerializableData"], **kwargs: Any) -> str:
        pass

    @classmethod
    def serialize_namedtuple(cls, data: NamedTuple, **kwargs: Any) -> str:
        pass

    @classmethod
    def serialize_dict(
        cls, data: dict["PropertyName", "SerializableData"], **kwargs: Any
    ) -> str:
        pass

    @classmethod
    def serialize_function(
        cls, data: FunctionType, *, depth: int = 0, **kwargs: Any
    ) -> str:
        pass

    @classmethod
    def serialize_unknown(cls, data: Any, *, depth: int = 0, **kwargs: Any) -> str:
        pass

    @classmethod
    def object_attrs(cls, data: Any) -> "Iterable[str]":
        pass

    @classmethod
    def object_as_named_tuple(cls, data: Any) -> "tuple[Any, ...]":
        pass

    @classmethod
    def with_indent(cls, string: str, depth: int) -> str:
        pass

    @classmethod
    def sort(cls, iterable: Iterable[Any]) -> Iterable[Any]:
        pass

    @classmethod
    def object_type(cls, data: "SerializableData") -> str:
        return f"{data.__class__.__name__}"

    @classmethod
    def __is_namedtuple(cls, obj: Any) -> bool:
        pass

    @classmethod
    def __serialize_plain(
        cls,
        *,
        data: "SerializableData",
        depth: int = 0,
    ) -> str:
        pass

    @classmethod
    def serialize_custom_iterable(
        cls,
        *,
        data: "SerializableData",
        resolve_entries: "IterableEntries",
        open_paren: str | None = None,
        close_paren: str | None = None,
        depth: int = 0,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        path: "PropertyPath" = (),
        separator: str | None = None,
        serialize_key: bool = False,
        **kwargs: Any,
    ) -> str:
        """
        Utility to serialize a custom iterable.
        """
        pass

    @classmethod
    def __serialize_lines(
        cls,
        *,
        data: "SerializableData",
        lines: Iterable[str],
        open_tag: str,
        close_tag: str,
        depth: int = 0,
        include_type: bool = True,
        ends: str = "\n",
    ) -> str:
        pass


class AmberDataSerializerSorted(AmberDataSerializer):
    """
    This is an experimental serializer with known performance issues.
    """

    VERSION = f"{AmberDataSerializer.VERSION}-sorted"

    @classmethod
    def __maybe_int(cls, part: str) -> tuple[int, str | int]:
        pass

    @classmethod
    def snapshot_sort_key(cls, snapshot: "Snapshot") -> Any:
        pass
