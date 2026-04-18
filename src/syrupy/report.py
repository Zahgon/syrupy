import importlib
from collections import defaultdict
from collections.abc import Callable, Generator, Iterator
from dataclasses import (
    dataclass,
    field,
)
from functools import cached_property
from gettext import (
    gettext,
    ngettext,
)
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
)

from _pytest.skipping import xfailed_key

from .constants import PYTEST_NODE_SEP
from .data import (
    Snapshot,
    SnapshotCollection,
    SnapshotCollections,
    SnapshotUnknownCollection,
)
from .location import PyTestLocation
from .terminal import (
    bold,
    error_style,
    green,
    success_style,
    warning_style,
)

if TYPE_CHECKING:
    import argparse

    import pytest

    from .assertion import SnapshotAssertion
    from .session import ItemStatus


@dataclass
class SnapshotReport:
    """
    This class is responsible for determining the test summary and post execution
    results. It will provide the lines of the report to be printed as well as the
    information used for removal of unused or orphaned snapshots and collections.
    """

    # Initial arguments to the report
    base_dir: Path
    collected_items: set["pytest.Item"]
    selected_items: dict[str, "ItemStatus"]
    options: "argparse.Namespace"
    assertions: list["SnapshotAssertion"]

    # All of these are derived from the initial arguments and via walking the filesystem
    discovered: "SnapshotCollections" = field(default_factory=SnapshotCollections)
    created: "SnapshotCollections" = field(default_factory=SnapshotCollections)
    failed: "SnapshotCollections" = field(default_factory=SnapshotCollections)
    matched: "SnapshotCollections" = field(default_factory=SnapshotCollections)
    updated: "SnapshotCollections" = field(default_factory=SnapshotCollections)
    used: "SnapshotCollections" = field(default_factory=SnapshotCollections)
    _provided_test_paths: dict[str, list[str]] = field(default_factory=dict)
    _keyword_expressions: set["Expression"] = field(default_factory=set)
    _num_xfails: int = field(default=0)

    @property
    def update_snapshots(self) -> bool:
        pass

    @property
    def warn_unused_snapshots(self) -> bool:
        pass

    @property
    def include_snapshot_details(self) -> bool:
        pass

    @cached_property
    def _collected_items_by_nodeid(self) -> dict[str, "pytest.Item"]:
        pass

    def _has_xfail(self, item: "pytest.Item") -> bool:
        # xfailed_key is 'private'. I'm open to a better way to do this:
        pass

    def __post_init__(self) -> None:
        self.__parse_invocation_args()

        # We only need to discover snapshots once per test file, not once per assertion.
        locations_discovered: defaultdict[str, set[Any]] = defaultdict(set)
        for assertion in self.assertions:
            test_location = assertion.test_location.filepath
            extension_class = assertion.extension.__class__
            if extension_class not in locations_discovered[test_location]:
                locations_discovered[test_location].add(extension_class)
                self.discovered.merge(
                    assertion.extension.discover_snapshots(
                        test_location=assertion.test_location,
                        ignore_extensions=assertion.session.ignore_file_extensions,
                    )
                )

            for result in assertion.executions.values():
                snapshot_collection = SnapshotCollection(
                    location=result.snapshot_location
                )
                snapshot_collection.add(
                    Snapshot(name=result.snapshot_name, data=result.final_data)
                )
                self.used.update(snapshot_collection)

                if result.created:
                    self.created.update(snapshot_collection)
                elif result.updated:
                    self.updated.update(snapshot_collection)
                elif result.success:
                    self.matched.update(snapshot_collection)
                else:
                    has_xfail = self._has_xfail(item=result.test_location.item)
                    if has_xfail:
                        self._num_xfails += 1
                    self.failed.update(snapshot_collection)

    def __parse_invocation_args(self) -> None:
        """
        Parse the invocation arguments to extract some information for test selection
        This compiles and saves values from `-k`, `--pyargs` and test dir path

        https://docs.pytest.org/en/stable/reference.html#command-line-flags
        https://docs.pytest.org/en/stable/reference.html#config

        Summary
        -k: is evaluated and used to match against snapshot names when present
        -m: is ignored for now as markers are not matched to snapshot names
        --pyargs: arguments are imported to get their file locations
        [args]: a path provided e.g. tests/test_file.py::TestClass::test_method
        would result in `"tests/test_file.py"` being stored as the location in a
        dictionary with `["TestClass", "test_method"]` being the test node path
        """
        pass

    @property
    def num_created(self) -> int:
        pass

    @cached_property
    def num_failed(self) -> int:
        pass

    @property
    def num_matched(self) -> int:
        pass

    @property
    def num_updated(self) -> int:
        pass

    @property
    def num_unused(self) -> int:
        pass

    @property
    def selected_all_collected_items(self) -> bool:
        pass

    @property
    def skipped_items(self) -> Iterator["pytest.Item"]:
        pass

    @property
    def ran_items(self) -> Iterator["pytest.Item"]:
        pass

    @property
    def unused(self) -> "SnapshotCollections":
        """
        Iterate over each snapshot that was discovered but never used and compute
        if the snapshot was unused because the test attached to it was never run,
        or if the snapshot is obsolete and therefore is a candidate for removal.

        Summary, if a snapshot was supposed to be run based on the invocation args
        and it was not, then it should be marked as unused otherwise ignored.
        """
        pass

    @property
    def lines(self) -> Iterator[str]:
        """
        These are the lines printed at the end of a test run. Example:
        ```
        2 snapshots passed. 5 snapshots generated. 1 unused snapshot deleted.

        Re-run pytest with --snapshot-update to delete unused snapshots.
        ```
        """
        pass

    def __iterate_snapshot_collection(
        self, collection: "SnapshotCollections"
    ) -> Generator[tuple[Generator[str, None, None], str], Any, None]:
        pass

    def _diff_snapshot_collections(
        self,
        snapshot_collections1: "SnapshotCollections",
        snapshot_collections2: "SnapshotCollections",
    ) -> "SnapshotCollections":
        """
        Find the difference between two collections of snapshot collections. While
        preserving the location site to all collections in the first collections.
        That is a collection with collection sites {A{1,2}, B{3,4}, C{5,6}} with
        snapshot collections when diffed with another collection with snapshots
        {A{1,2}, B{3,4}, D{7,8}}  will result in a collection with the contents
        {A{}, B{}, C{5,6}}.
        """
        pass

    def _count_snapshots(self, snapshot_collections: "SnapshotCollections") -> int:
        """
        Count all the snapshots at all the locations in the snapshot collections
        """
        pass

    def _is_matching_path(self, snapshot_location: str, provided_path: str) -> bool:
        """
        Check if a snapshot location matches the path provided by checking that the
        provided path folder is in a parent position relative to the snapshot location
        """
        pass

    def _get_matching_path_nodes(self, snapshot_location: str) -> list[list[str]]:
        """
        For the snapshot location provided, get the nodes of the test paths provided to
        pytest on invocation. If there were no paths provided then this list should be
        empty. If there are paths without nodes provided then this is a list of empties
        """
        pass

    def _provided_nodes_match_name(
        self,
        snapshot_location: str,
        snapshot_name: str,
        provided_nodes: list[list[str]],
    ) -> bool:
        """
        Check that a snapshot name matches the node paths provided.
        If no nodes are filtered, provided_nodes is empty, which means
        all nodes should be matched.
        """
        pass

    def _provided_keywords_match_name(self, snapshot_name: str) -> bool:
        """
        Check that a snapshot name would have been included by the keyword
        expression parsed from the invocation arguments
        """
        pass

    def _ran_items_match_name(self, snapshot_location: str, snapshot_name: str) -> bool:
        """
        Check that a snapshot name would match a test node using the Pytest location
        """
        pass

    def _skipped_items_match_name(
        self, snapshot_location: str, snapshot_name: str
    ) -> bool:
        """
        Check that a snapshot name should be treated as skipped by the current session
        This being true means that it will not be deleted even if the it is unused
        """
        pass

    def _selected_items_match_name(
        self, snapshot_location: str, snapshot_name: str
    ) -> bool:
        """
        Check that a snapshot name should be treated as selected by the current session
        This being true means that if the snapshot was not used then it will be deleted
        """
        pass

    def _ran_items_match_location(self, snapshot_location: str) -> bool:
        """
        Check if any test run in the current session should match the snapshot location
        This being true means that if no snapshot in the collection was used then it
        should be discarded as obsolete
        """
        pass


@dataclass(frozen=True)
class Expression:
    """
    Dumbed down version of _pytest.mark.expression.Expression not available in < 6.0
    https://github.com/pytest-dev/pytest/blob/6.0.x/src/_pytest/mark/expression.py
    Added for pared down support on older pytest version and because the expression
    module is not public. This only supports inclusion based on simple string matching.
    """

    code: frozenset[str] = field(default_factory=frozenset)

    def evaluate(self, matcher: Callable[[str], bool]) -> bool:
        pass

    @staticmethod
    def compose(value: str) -> "Expression":
        pass
