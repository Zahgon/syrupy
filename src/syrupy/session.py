from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)
from enum import Enum
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    Optional,
)

import pytest

from .constants import EXIT_STATUS_FAIL_UNUSED
from .data import SnapshotCollections
from .location import PyTestLocation
from .report import SnapshotReport
from .types import (
    SerializedData,
    SnapshotIndex,
)
from .utils import (
    is_xdist_controller,
    is_xdist_worker,
)

if TYPE_CHECKING:
    from .assertion import SnapshotAssertion
    from .extensions.base import AbstractSyrupyExtension


class ItemStatus(Enum):
    NOT_RUN = False
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


_QueuedWriteExtensionKey = tuple[type["AbstractSyrupyExtension"], str]
_QueuedWriteTestLocationKey = tuple["PyTestLocation", "SnapshotIndex"]


@dataclass
class SnapshotSession:
    pytest_session: "pytest.Session"

    # List of file extensions to ignore during discovery/processing
    ignore_file_extensions: list[str] | None = None

    # Snapshot report generated on finish
    report: Optional["SnapshotReport"] = None
    # All the collected test items
    _collected_items: set["pytest.Item"] = field(default_factory=set)
    # All the selected test items. Will be set to False until the test item is run.
    _selected_items: dict[str, ItemStatus] = field(default_factory=dict)
    _assertions: list["SnapshotAssertion"] = field(default_factory=list)
    _extensions: dict[str, "AbstractSyrupyExtension"] = field(default_factory=dict)

    _locations_discovered: defaultdict[str, set[Any]] = field(
        default_factory=lambda: defaultdict(set)
    )

    # For performance, we buffer snapshot writes in memory before flushing them to disk. In
    # particular, we want to be able to write to a file on disk only once, rather than having to
    # repeatedly rewrite it.
    #
    # That batching leads to using two layers of dicts here: the outer layer represents the
    # extension/file-location pair that will be written, and the inner layer represents the
    # snapshots within that, "indexed" to allow efficient recall.
    _queued_snapshot_writes: defaultdict[
        _QueuedWriteExtensionKey,
        dict[_QueuedWriteTestLocationKey, "SerializedData"],
    ] = field(default_factory=lambda: defaultdict(dict))

    def _snapshot_write_queue_keys(
        self,
        extension: "AbstractSyrupyExtension",
        test_location: "PyTestLocation",
        index: "SnapshotIndex",
    ) -> tuple[_QueuedWriteExtensionKey, _QueuedWriteTestLocationKey]:
        pass

    def queue_snapshot_write(
        self,
        extension: "AbstractSyrupyExtension",
        test_location: "PyTestLocation",
        data: "SerializedData",
        index: "SnapshotIndex",
    ) -> None:
        pass

    def flush_snapshot_write_queue(self) -> None:
        pass

    def recall_snapshot(
        self,
        extension: "AbstractSyrupyExtension",
        test_location: "PyTestLocation",
        index: "SnapshotIndex",
    ) -> Optional["SerializedData"]:
        """Find the current value of the snapshot, for this session, either a pending write or the actual snapshot."""
        pass

    @property
    def update_snapshots(self) -> bool:
        pass

    @property
    def warn_unused_snapshots(self) -> bool:
        pass

    def collect_items(self, items: list["pytest.Item"]) -> None:
        pass

    def select_items(self, items: list["pytest.Item"]) -> None:
        pass

    def start(self) -> None:
        pass

    def ran_item(
        self, nodeid: str, outcome: Literal["passed", "skipped", "failed"]
    ) -> None:
        pass

    def finish(self) -> int:
        pass

    def register_request(self, assertion: "SnapshotAssertion") -> None:
        pass

    def remove_unused_snapshots(
        self,
        unused_snapshot_collections: "SnapshotCollections",
        used_snapshot_collections: "SnapshotCollections",
    ) -> None:
        """
        Remove all unused snapshots using the registed extension for the collection file
        If there is not registered extension and the location is unused delete the file
        """
        pass

    @staticmethod
    def filter_valid_items(items: list["pytest.Item"]) -> Iterable["pytest.Item"]:
        pass
