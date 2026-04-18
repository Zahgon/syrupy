from enum import Enum
from gettext import gettext
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Optional,
)
from unicodedata import category

from syrupy.constants import TEXT_ENCODING
from syrupy.data import (
    Snapshot,
    SnapshotCollection,
)
from syrupy.exceptions import TaintedSnapshotError
from syrupy.extensions.amber.serializer import AmberDataSerializer
from syrupy.location import PyTestLocation
from syrupy.types import PropertyFilter, PropertyMatcher, SerializableData

from .base import AbstractSyrupyExtension

if TYPE_CHECKING:
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        SerializableData,
        SerializedData,
        SnapshotIndex,
    )


class WriteMode(Enum):
    BINARY = "b"
    TEXT = "t"

    def __str__(self) -> str:
        return self.value


class SingleFileSnapshotExtension(AbstractSyrupyExtension):
    _text_encoding = TEXT_ENCODING
    _write_mode = WriteMode.BINARY
    file_extension = "raw"

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        pass

    @classmethod
    def get_snapshot_name(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex" = 0
    ) -> str:
        pass

    def delete_snapshots(
        self, *, snapshot_location: str, snapshot_names: set[str]
    ) -> None:
        pass

    @classmethod
    def get_file_basename(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex"
    ) -> str:
        pass

    @classmethod
    def dirname(cls, *, test_location: "PyTestLocation") -> str:
        pass

    def read_snapshot_collection(
        self, *, snapshot_location: str
    ) -> "SnapshotCollection":
        pass

    def read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str, session_id: str
    ) -> Optional["SerializableData"]:
        pass

    @classmethod
    def get_supported_dataclass(cls) -> type[str] | type[bytes]:
        pass

    @classmethod
    def get_write_encoding(cls) -> str | None:
        pass

    @classmethod
    def write_snapshot_collection(
        cls, *, snapshot_collection: "SnapshotCollection"
    ) -> None:
        pass

    @classmethod
    def __clean_filename(cls, filename: str) -> str:
        pass


class SingleFileAmberSnapshotExtension(SingleFileSnapshotExtension):
    file_extension = "ambr"
    _write_mode = WriteMode.TEXT

    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        pass

    def read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str, session_id: str
    ) -> Optional["SerializableData"]:
        pass

    @classmethod
    def write_snapshot_collection(
        cls, *, snapshot_collection: "SnapshotCollection"
    ) -> None:
        pass
