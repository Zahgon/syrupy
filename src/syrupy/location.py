from collections.abc import Iterator
from dataclasses import (
    dataclass,
    field,
)
from pathlib import Path

import pytest

from syrupy.constants import PYTEST_NODE_SEP


@dataclass(frozen=True)
class PyTestLocation:
    item: "pytest.Item"
    nodename: str | None = field(init=False)
    testname: str = field(init=False)
    methodname: str = field(init=False)
    modulename: str = field(init=False)
    filepath: str = field(init=False)

    def __post_init__(self) -> None:
        # NB. we're in a frozen dataclass, but need to transform the values that the caller
        # supplied... we do so by (ab)using object.__setattr__ to forcibly set the attributes. (See
        # rejected PEP-0712 for an example of a better way to handle this.)
        #
        # This is safe because this all happens during initialization: `self` hasn't been hashed
        # (or, e.g., stored in a dict), so the mutation won't be noticed.
        if self.is_doctest:
            return self.__attrs_post_init_doc__()
        self.__attrs_post_init_def__()

    def __attrs_post_init_def__(self) -> None:
        node_path: Path = getattr(self.item, "path")  # noqa: B009
        # See __post_init__ for discussion of object.__setattr__
        object.__setattr__(self, "filepath", str(node_path.absolute()))
        obj = getattr(self.item, "obj")  # noqa: B009
        object.__setattr__(self, "modulename", obj.__module__)
        object.__setattr__(self, "methodname", obj.__name__)
        object.__setattr__(self, "nodename", getattr(self.item, "name", None))
        object.__setattr__(self, "testname", self.nodename or self.methodname)

    def __attrs_post_init_doc__(self) -> None:
        doctest = getattr(self.item, "dtest")  # noqa: B009
        # See __post_init__ for discussion of object.__setattr__
        object.__setattr__(self, "filepath", doctest.filename)
        test_relfile, test_node = self.nodeid.split(PYTEST_NODE_SEP)
        test_relpath = Path(test_relfile)
        object.__setattr__(
            self,
            "modulename",
            ".".join([*test_relpath.parent.parts, test_relpath.stem]),
        )
        object.__setattr__(self, "methodname", None)
        object.__setattr__(
            self, "nodename", test_node.replace(f"{self.modulename}.", "")
        )
        object.__setattr__(self, "testname", self.nodename or self.methodname)

    @property
    def is_item_parametrized(self) -> bool:
        pass

    @property
    def classname(self) -> str | None:
        pass

    @property
    def nodeid(self) -> str:
        """
        Pytest node names contain file path and module members delimited by `::`

        Examples:
        - tests/grouping/test_file.py::TestClass::TestSubClass::test_method
        - tests/grouping/test_file.py::DocTestClass.doc_test_method
        - tests/grouping/test_file.py::doctestfile.txt

        :raises: `AttributeError` if node has no node id
        :return: test node id
        """
        pass

    @property
    def basename(self) -> str:
        pass

    @property
    def snapshot_name(self) -> str:
        pass

    @property
    def snapshot_name_parametrized(self) -> str:
        pass

    @property
    def is_doctest(self) -> bool:
        pass

    def __is_doctest(self, node: "pytest.Item") -> bool:
        pass

    def __valid_id(self, name: str) -> str:
        """
        Take characters from the name while the result would be a valid python
        identified. Example: "test_2[A]" returns "test_2" while "1_a" would return ""
        """
        pass

    def __valid_ids(self, name: str) -> Iterator[str]:
        """
        Break a name path into valid name parts stopping at the first non valid name.
        Example "TestClass.test_method_[1]" would yield ("TestClass", "test_method_")
        """
        pass

    def __parse(self, name: str) -> str:
        pass

    def matches_snapshot_name(self, snapshot_name: str) -> bool:
        pass

    def matches_snapshot_location(self, snapshot_location: str) -> bool:
        pass
