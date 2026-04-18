"""Attrs plugin for Syrupy Amber serializer."""

from typing import Any

import attr

from syrupy.extensions.amber.serializer import (
    AmberDataSerializer,
    AmberDataSerializerPlugin,
    attr_getter,
)
from syrupy.types import SerializableData


class AttrsPlugin(AmberDataSerializerPlugin):
    """A Syrupy extension that serializes attrs class instances using Amber format."""

    @classmethod
    def is_data_serializable(cls, data: "SerializableData") -> bool:
        """Check if the data is an attrs class instance."""
        pass

    @classmethod
    def serialize(cls, data: "SerializableData", **kwargs: Any) -> str:
        """Serialize an attrs class instance into Amber format."""
        pass
