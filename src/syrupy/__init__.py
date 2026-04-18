import argparse
import contextlib
import sys
from collections.abc import Iterator
from functools import lru_cache
from gettext import gettext
from typing import (
    Any,
    Optional,
)

import pytest

from syrupy.extensions.base import SnapshotCollectionStorage

from .assertion import DiffMode, SnapshotAssertion
from .constants import DISABLE_COLOR_ENV_VAR
from .exceptions import FailedToLoadModuleMember
from .extensions import DEFAULT_EXTENSION
from .location import PyTestLocation
from .patches.pycharm_diff import patch_pycharm_diff
from .session import SnapshotSession
from .terminal import (
    received_style,
    reset,
    snapshot_style,
)
from .utils import (
    env_context,
    import_module_member,
    is_xdist_worker,
)

# Global to have access to the session in `pytest_runtest_logfinish` hook
_syrupy: Optional["SnapshotSession"] = None


@lru_cache(maxsize=1)
def __import_extension(value: str | None) -> Any:
    pass


def pytest_addoption(parser: "pytest.Parser") -> None:
    """
    Exposes snapshot plugin configuration to pytest.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_addoption
    """
    pass


def __terminal_color(
    config: "pytest.Config",
) -> "contextlib.AbstractContextManager[None]":
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_assertrepr_compare(
    config: "pytest.Config", op: str, left: Any, right: Any
) -> list[str] | None:
    """
    Return explanation for comparisons in failing assert expressions.
    https://docs.pytest.org/en/latest/reference.html#pytest.hookspec.pytest_assertrepr_compare
    """
    pass


def pytest_sessionstart(session: Any) -> None:
    """
    Initialize snapshot session before tests are collected and ran.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart
    """
    pass


def pytest_collection_modifyitems(
    session: Any, config: Any, items: list["pytest.Item"]
) -> None:
    """
    After tests are collected and before any modification is performed.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_modifyitems
    """
    pass


def pytest_collection_finish(session: Any) -> None:
    """
    After collection has been performed and modified.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_collection_finish
    """
    pass


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """
    After each of the setup, call and teardown runtest phases of an item.
    https://docs.pytest.org/en/8.0.x/reference/reference.html#pytest.hookspec.pytest_runtest_logreport
    """
    pass


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session: "pytest.Session", exitstatus: int) -> None:
    """
    Finish session run and set exit status.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionfinish
    """
    pass


def pytest_terminal_summary(
    terminalreporter: Any, exitstatus: int, config: Any
) -> None:
    """
    Add syrupy report to pytest.
    https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_terminal_summary
    """
    pass


@pytest.fixture
def snapshot(request: "pytest.FixtureRequest") -> "SnapshotAssertion":
    pass


@pytest.fixture(scope="session", autouse=True)
def _syrupy_apply_ide_patches(request: "pytest.FixtureRequest") -> Iterator[None]:
    pass
