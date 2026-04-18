import warnings
from collections.abc import Iterator
from contextlib import contextmanager
from functools import wraps
from inspect import signature
from typing import (
    Any,
)

from syrupy.assertion import SnapshotAssertion


@contextmanager
def patch_pycharm_diff() -> Iterator[None]:
    """
    Applies PyCharm diff patch to add Syrupy snapshot support.
    See: https://github.com/syrupy-project/syrupy/issues/675
    """

    try:
        from teamcity.diff_tools import EqualsAssertionError  # type: ignore
    except ImportError:
        warnings.warn(
            "Failed to patch PyCharm's diff tools. Skipping patch.",
            stacklevel=2,
        )
        yield
        return

    old_init = EqualsAssertionError.__init__
    old_init_signature = signature(old_init)

    @wraps(old_init)
    def new_init(self: "EqualsAssertionError", *args: Any, **kwargs: Any) -> None:
        # Extract the __init__ arguments as originally passed in order to
        # process them later
        pass

    try:
        EqualsAssertionError.__init__ = new_init
        yield
    finally:
        EqualsAssertionError.__init__ = old_init
