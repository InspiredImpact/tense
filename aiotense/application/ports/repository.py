# Copyright 2022 Animatea
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Interfaces that are implemented in aiotense.adapters."""
from __future__ import annotations

__all__ = ["AbstractTenseRepository"]

import abc
from typing import TypedDict, TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from aiotense.domain import units

    class _VirtualUnitDict(TypedDict):
        duration: int
        aliases: list[str]


class AbstractTenseRepository(abc.ABC):
    """`Add` operations allows fluent-style."""
    def __init__(self, config: Optional[dict[str, Any]] = None, /) -> None:
        self._config = config

    def __getitem__(self, item: Any) -> Any:
        if not isinstance(item, str):
            return NotImplemented
        return self._config[item]

    def __setitem__(self, key: Any, value: Any) -> Any:
        if not isinstance(key, str) or not isinstance(value, str):
            return NotImplemented
        if key not in self._config:
            raise KeyError(
                f"Key {key} does not exist in config. New keys cannot be added."
            )
        self._config[key] = value

    @property
    def config(self) -> Optional[dict[str, Any]]:
        return self._config

    @abc.abstractmethod
    def get_config(self) -> dict[str, Any]:
        """Returns deepcopy of current config."""
        ...

    @abc.abstractmethod
    def get_setting(self, path: str, setting: str, /) -> Any:
        ...

    @abc.abstractmethod
    def add_virtual_unit(self, unit: units.VirtualUnit) -> AbstractTenseRepository:
        """Adds custom unit of time. Allows fluent-style."""
        ...

    @abc.abstractmethod
    def add_virtual_unit_dict(self, unit_dict: _VirtualUnitDict) -> AbstractTenseRepository:
        """Adds custom unit of time. Allows fluent-style."""
        ...

    @abc.abstractmethod
    def add_aliases_to(self, unit: Type[units.Unit], aliases: list[str]) -> AbstractTenseRepository:
        """Adds aliases to unit of time. Allows fluent-style."""
        ...
