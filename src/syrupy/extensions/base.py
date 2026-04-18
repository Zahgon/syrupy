import warnings
from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Callable, Iterator
from gettext import gettext
from itertools import zip_longest
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Optional,
)

from syrupy.constants import (
    DISABLE_COLOR_ENV_VAR,
    SYMBOL_CARRIAGE,
    SYMBOL_ELLIPSIS,
    SYMBOL_NEW_LINE,
)
from syrupy.data import (
    DiffedLine,
    Snapshot,
    SnapshotCollection,
    SnapshotCollections,
    SnapshotEmptyCollection,
)
from syrupy.exceptions import SnapshotDoesNotExist
from syrupy.terminal import (
    context_style,
    received_diff_style,
    received_style,
    reset,
    snapshot_diff_style,
    snapshot_style,
)
from syrupy.utils import (
    env_context,
    obj_attrs,
    qdiff,
    walk_snapshot_dir,
)

if TYPE_CHECKING:
    from syrupy.location import PyTestLocation
    from syrupy.types import (
        PropertyFilter,
        PropertyMatcher,
        SerializableData,
        SerializedData,
        SnapshotIndex,
    )


class SnapshotSerializer(ABC):
    @abstractmethod
    def serialize(
        self,
        data: "SerializableData",
        *,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
    ) -> "SerializedData":
        """
        Serializes a python object / data structure into a string
        to be used for comparison with snapshot data from disk.
        """
        raise NotImplementedError


class SnapshotCollectionStorage(ABC):
    snapshot_dirname: str | Path = "__snapshots__"
    file_extension = ""

    @classmethod
    def get_snapshot_name(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex" = 0
    ) -> str:
        """Get the snapshot name for the assertion index in a test location"""
        pass

    @classmethod
    def get_location(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex"
    ) -> str:
        """Returns full filepath where snapshot data is stored."""
        pass

    def is_snapshot_location(self, *, location: str) -> bool:
        """Checks if supplied location is valid for this snapshot extension"""
        pass

    def discover_snapshots(
        self,
        *,
        test_location: "PyTestLocation",
        ignore_extensions: list[str] | None = None,
    ) -> "SnapshotCollections":
        """
        Returns all snapshot collections in test site
        """
        pass

    def read_snapshot(
        self,
        *,
        test_location: "PyTestLocation",
        index: "SnapshotIndex",
        session_id: str,
    ) -> "SerializedData":
        """
        This method is _final_, do not override. You can override
        `read_snapshot_data_from_location` in a subclass to change behaviour.
        """
        pass

    @classmethod
    def write_snapshot(
        cls,
        *,
        snapshot_location: str,
        snapshots: list[tuple["SerializedData", "PyTestLocation", "SnapshotIndex"]],
    ) -> None:
        """
        This method is _final_, do not override. You can override
        `write_snapshot_collection` in a subclass to change behaviour.
        """
        pass

    @abstractmethod
    def delete_snapshots(
        self, *, snapshot_location: str, snapshot_names: set[str]
    ) -> None:
        """
        Remove snapshots from a snapshot file.
        If the snapshot file will be empty remove the entire file.
        """
        raise NotImplementedError

    @abstractmethod
    def read_snapshot_collection(
        self, *, snapshot_location: str
    ) -> "SnapshotCollection":
        """
        Read the snapshot location and construct a snapshot collection object
        """
        raise NotImplementedError

    @abstractmethod
    def read_snapshot_data_from_location(
        self, *, snapshot_location: str, snapshot_name: str, session_id: str
    ) -> Optional["SerializedData"]:
        """
        Get only the snapshot data from location for assertion
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def write_snapshot_collection(
        cls, *, snapshot_collection: "SnapshotCollection"
    ) -> None:
        """
        Adds the snapshot data to the snapshots in collection location
        """
        raise NotImplementedError

    @classmethod
    def dirname(cls, *, test_location: "PyTestLocation") -> str:
        pass

    @classmethod
    def get_file_basename(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex"
    ) -> str:
        """Returns file basename without extension. Used to create full filepath."""
        pass


def _count_leading_whitespace(s: str) -> int:
    pass


class SnapshotReporter:
    _context_line_count = 1

    def diff_snapshots(
        self, serialized_data: "SerializedData", snapshot_data: "SerializedData"
    ) -> "SerializedData":
        pass

    def diff_lines(
        self, serialized_data: "SerializedData", snapshot_data: "SerializedData"
    ) -> Iterator[str]:
        pass

    @property
    def _ends(self) -> dict[str, str]:
        pass

    @property
    def _context_line_max(self) -> int:
        pass

    @property
    def _marker_context_max(self) -> str:
        pass

    @property
    def _marker_new_line(self) -> str:
        pass

    @property
    def _marker_carriage(self) -> str:
        pass

    def __diff_lines(self, a: str, b: str) -> Iterator[str]:
        pass

    def __diffed_lines(self, a: str, b: str) -> Iterator["DiffedLine"]:
        pass

    def __format_line(
        self,
        line: str,
        diff_markers: str,
        line_style: Callable[[str], str],
        diff_style: Callable[[str], str],
        show_ends: bool,
    ) -> str:
        pass

    def __limit_context(self, lines: list[str]) -> Iterator[str]:
        pass

    def __strip_ends(self, line: str) -> str:
        pass


class SnapshotComparator:
    def matches(
        self,
        *,
        serialized_data: "SerializableData",
        snapshot_data: "SerializableData",
    ) -> bool:
        """
        Compares serialized data and snapshot data and returns
        whether they match.
        """
        pass


class AbstractSyrupyExtension(
    SnapshotSerializer, SnapshotCollectionStorage, SnapshotReporter, SnapshotComparator
):
    pass
