from functools import lru_cache
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from syrupy.data import SnapshotCollection
from syrupy.exceptions import TaintedSnapshotError
from syrupy.extensions.base import AbstractSyrupyExtension

from .serializer import (  # noqa: F401
    AmberDataSerializer,
    AmberDataSerializerPlugin,
    AmberDataSerializerSorted,  # re-exported
)

if TYPE_CHECKING:
    from syrupy.types import SerializableData


class AmberSnapshotExtension(AbstractSyrupyExtension):
    """
    An amber snapshot file stores data in the following format:
    """

    file_extension = "ambr"

    serializer_class: type["AmberDataSerializer"] = AmberDataSerializer

    def serialize(self, data: "SerializableData", **kwargs: Any) -> str:
        """
        Returns the serialized form of 'data' to be compared
        with the snapshot data written to disk.
        """
        pass

    def delete_snapshots(
        self, snapshot_location: str, snapshot_names: set[str]
    ) -> None:
        pass

    def read_snapshot_collection(self, snapshot_location: str) -> "SnapshotCollection":
        pass

    @classmethod
    @lru_cache
    def __cacheable_read_snapshot(
        cls, snapshot_location: str, cache_key: str
    ) -> "SnapshotCollection":
        pass

    def read_snapshot_data_from_location(
        self, snapshot_location: str, snapshot_name: str, session_id: str
    ) -> Optional["SerializableData"]:
        pass

    @classmethod
    def write_snapshot_collection(
        cls, *, snapshot_collection: "SnapshotCollection"
    ) -> None:
        pass


__all__ = ["AmberSnapshotExtension", "AmberDataSerializer", "AmberDataSerializerPlugin"]
