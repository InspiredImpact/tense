from __future__ import annotations

import abc
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from aiotense.domain import units


class AbstractTenseRepository(abc.ABC):
    def __init__(self, source: Optional[dict[str, Any]] = None, /) -> None:
        self.source = source

    @abc.abstractmethod
    def get_config(self) -> dict[str, Any]:
        ...

    @abc.abstractmethod
    def get_setting(self, setting: str, /) -> Any:
        ...

    @abc.abstractmethod
    def add_setting(self, setting: str, value: Any, /) -> None:
        ...

    @abc.abstractmethod
    def add_virtual_unit(self, unit: units.VirtualUnit) -> None:
        ...

    @abc.abstractmethod
    def add_virtual_unit_dict(self, unit_dict: dict[str, Any]) -> None:
        ...
