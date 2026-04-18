import traceback
from collections import namedtuple
from collections.abc import Callable
from dataclasses import (
    dataclass,
    field,
)
from enum import Enum
from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from .exceptions import (
    SnapshotDoesNotExist,
    TaintedSnapshotError,
)
from .extensions.amber.serializer import Repr

if TYPE_CHECKING:
    from .extensions.base import AbstractSyrupyExtension
    from .location import PyTestLocation
    from .session import SnapshotSession
    from .types import (
        PropertyFilter,
        PropertyMatcher,
        SerializableData,
        SerializedData,
        SnapshotIndex,
    )


class DiffMode(Enum):
    DETAILED = "detailed"
    DISABLED = "disabled"

    def __str__(self) -> str:
        return self.value


@dataclass
class AssertionResult:
    snapshot_location: str
    snapshot_name: str
    asserted_data: Optional["SerializedData"]
    recalled_data: Optional["SerializedData"]
    created: bool
    updated: bool
    success: bool
    exception: Exception | None
    test_location: "PyTestLocation"

    @property
    def final_data(self) -> Optional["SerializedData"]:
        pass


@dataclass(eq=False, order=False, repr=False)
class SnapshotAssertion:
    session: "SnapshotSession"
    extension_class: type["AbstractSyrupyExtension"]
    test_location: "PyTestLocation"
    update_snapshots: bool
    include: Optional["PropertyFilter"] = None
    exclude: Optional["PropertyFilter"] = None
    matcher: Optional["PropertyMatcher"] = None

    _exclude: Optional["PropertyFilter"] = field(
        init=False,
        default=None,
    )
    _include: Optional["PropertyFilter"] = field(
        init=False,
        default=None,
    )
    _custom_index: str | None = field(
        init=False,
        default=None,
    )
    _extension: Optional["AbstractSyrupyExtension"] = field(
        init=False,
        default=None,
    )
    _executions: int = field(
        init=False,
        default=0,
    )
    _execution_results: dict[int, "AssertionResult"] = field(
        init=False,
        default_factory=dict,
    )
    _execution_name_index: dict["SnapshotIndex", int] = field(
        init=False, default_factory=dict
    )
    _matcher: Optional["PropertyMatcher"] = field(
        init=False,
        default=None,
    )
    _post_assert_actions: list[Callable[..., None]] = field(
        init=False,
        default_factory=list,
    )

    def __post_init__(self) -> None:
        self.session.register_request(self)
        self._include = self.include
        self._exclude = self.exclude
        self._matcher = self.matcher

    def __init_extension(
        self, extension_class: type["AbstractSyrupyExtension"]
    ) -> "AbstractSyrupyExtension":
        pass

    @property
    def extension(self) -> "AbstractSyrupyExtension":
        pass

    @property
    def num_executions(self) -> int:
        pass

    @property
    def executions(self) -> dict[int, "AssertionResult"]:
        pass

    @property
    def index(self) -> "SnapshotIndex":
        pass

    @property
    def name(self) -> str:
        pass

    @property
    def __repr(self) -> "SerializableData":
        pass

    @property
    def __matcher(self) -> "PropertyMatcher":
        """
        Get matcher that replaces `SnapshotAssertion` with one that can be serialized
        """
        pass

    def with_defaults(
        self,
        *,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        matcher: Optional["PropertyMatcher"] = None,
        extension_class: type["AbstractSyrupyExtension"] | None = None,
    ) -> "SnapshotAssertion":
        """
        Create new snapshot assertion fixture with provided values. This preserves
        provided values between assertions.
        """
        pass

    def use_extension(
        self, extension_class: type["AbstractSyrupyExtension"] | None = None
    ) -> "SnapshotAssertion":
        """
        Create new snapshot assertion fixture with the same options but using
        specified extension class. This does not preserve assertion index or state.
        """
        pass

    def assert_match(self, data: "SerializableData") -> None:
        pass

    def _serialize(self, data: "SerializableData") -> "SerializedData":
        pass

    def get_assert_diff(
        self, *, diff_mode: "DiffMode" = DiffMode.DETAILED
    ) -> list[str]:
        pass

    def __with_prop(self, prop_name: str, prop_value: Any) -> None:
        pass

    def __call__(
        self,
        *,
        diff: Optional["SnapshotIndex"] = None,
        exclude: Optional["PropertyFilter"] = None,
        include: Optional["PropertyFilter"] = None,
        extension_class: type["AbstractSyrupyExtension"] | None = None,
        matcher: Optional["PropertyMatcher"] = None,
        name: Optional["SnapshotIndex"] = None,
    ) -> "SnapshotAssertion":
        """
        Modifies assertion instance options
        """
        if exclude:
            self.__with_prop("_exclude", exclude)
        if include:
            self.__with_prop("_include", include)
        if extension_class:
            self.__with_prop("_extension", self.__init_extension(extension_class))
        if matcher:
            self.__with_prop("_matcher", matcher)
        if name:
            self.__with_prop("_custom_index", name)
        if diff is not None:
            self.__with_prop("_snapshot_diff", diff)
        return self

    def __repr__(self) -> str:
        return str(self.__repr)

    def __eq__(self, other: "SerializableData") -> bool:
        return self._assert(other)

    def _assert(self, data: "SerializableData") -> bool:
        pass

    def _post_assert(self) -> None:
        """
        Restores assertion instance options
        """
        pass

    def _recall_data(
        self, index: "SnapshotIndex"
    ) -> tuple[Optional["SerializableData"], bool]:
        pass
