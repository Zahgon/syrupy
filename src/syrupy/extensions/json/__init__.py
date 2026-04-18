# noqa: A005
import datetime
import inspect
import json
from collections import OrderedDict
from collections.abc import Iterable
from types import (
    FunctionType,
    GeneratorType,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from syrupy.constants import SYMBOL_ELLIPSIS
from syrupy.extensions.amber.serializer import Repr
from syrupy.extensions.single_file import (
    SingleFileSnapshotExtension,
    WriteMode,
)

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        PropertyPath,
        SerializableData,
        SerializedData,
    )


class JSONSnapshotExtension(SingleFileSnapshotExtension):
    _max_depth: int = 99
    _write_mode = WriteMode.TEXT
    file_extension = "json"

    @classmethod
    def sort(cls, iterable: Iterable[Any]) -> Iterable[Any]:
        pass

    @classmethod
    def __is_namedtuple(cls, obj: Any) -> bool:
        pass

    @classmethod
    def _filter(
        cls,
        data: "SerializableData",
        *,
        depth: int = 0,
        path: "PropertyPath",
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
        visited: set[Any] | None = None,
    ) -> "SerializableData":
        pass

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        pass
