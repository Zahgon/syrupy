"""Dataclass plugin for Syrupy Amber serializer."""

import dataclasses
from typing import Any

from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
    AmberDataSerializerPlugin,
    attr_getter,
)
from syrupy.types import SerializableData


class DataclassPlugin(AmberDataSerializerPlugin):
    """A Syrupy extension that serializes dataclass instances using Amber format."""

    @classmethod
    def is_data_serializable(cls, data: "SerializableData") -> bool:
        """Check if the data is a dataclass instance.

        Note: Excludes dataclass types themselves, which also yield True for is_dataclass.
        """
        pass

    @classmethod
    def serialize(cls, data: "SerializableData", **kwargs: Any) -> str:
        """Serialize a dataclass instance into Amber format."""
        pass
